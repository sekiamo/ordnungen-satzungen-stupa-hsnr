#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft Querverweise zwischen Paragraphen/Absaetzen und schlaegt Alarm.

Grundlage sind die Einzelparagraphen (satzung/<dok>/pNN-*.md, ordnungen/<dok>/...).
Der erzeugte Gesamttext (satzung/<dok>.md) wird ignoriert, denn er ist abgeleitet.
Zusaetzlich werden Dateien direkt unter satzung/ und ordnungen/ gelesen, die keinen
Einzelparagraphen-Ordner haben (z.B. lokale Geschaeftsordnungen aus der .gitignore).
Sie werden nur lokal gefunden; auf GitHub gibt es sie nicht.

Aufruf:

    python tools/check_verweise.py                     # gegen origin/main pruefen
    python tools/check_verweise.py --base HEAD~1       # gegen einen anderen Stand
    python tools/check_verweise.py --base none         # nur den Ist-Zustand pruefen
    python tools/check_verweise.py --write-liste       # VERWEISE.md neu schreiben

Was geprueft wird (Ist-Zustand, ohne --base):
  FEHLER   Verweis-Link zeigt auf einen Anker oder eine Datei, die es nicht gibt.
  FEHLER   Dieselbe Anker-ID kommt in einem Dokument mehrfach vor.
  HINWEIS  Absatz-Anker passt nicht zur ID des Paragraphen (p10a-1 statt p11-1).

Zusaetzlich im Vergleich mit dem Stand --base:
  FEHLER   Ein Anker, auf den verwiesen wurde, ist verschwunden oder umbenannt.
  ALARM    Der Text eines Paragraphen/Absatzes, auf den verwiesen wird, wurde
           geaendert. Die Verweisenden werden aufgelistet und muessen geprueft werden.
  HINWEIS  Ein Verweis im Fliesstext ("§ 5 Abs. 2") meint eine Nummer, die sich
           verschoben hat. Fliesstext-Verweise sind nur eine Heuristik.
  HINWEIS  Anker verschwunden, der nirgends verlinkt war (evtl. umbenannt).

Nummern in "§ N" zaehlen beim Vergleich nicht als Textaenderung, damit eine
Umnummerierung keinen falschen Alarm ausloest.

Exit-Code: 0 = alles in Ordnung, 1 = Fehler, 3 = nur Alarm (Verweise pruefen).
"""
import argparse
import hashlib
import os
import posixpath
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NL = '\n'
SCAN_DIRS = ('satzung', 'ordnungen')

ANCHOR = re.compile(r'<a id="([^"]+)"></a>')
PAR_ID = re.compile(r'^p\d+[a-z]*$')
ABS_ID = re.compile(r'^(p\d+[a-z]*)-(\d+)$')
LINK = re.compile(r'(?<!!)\[([^\]]*)\]\(([^)\s]+)\)')
NUM = re.compile(r'§\s*(\d+[a-z]?)')
PLAIN = re.compile(r'§\s*(\d+[a-z]?)(?:\s*(?:Abs\.|Absatz)\s*(\d+))?')
EXTERNAL = re.compile(r'\s*(?:Nr\.\s*\d+[\s,]*)*([A-ZÄÖÜ]{2,})\b')
DOC_HINT = re.compile(r'\b(Satzung|Finanzordnung|Fachschaftsrahmenordnung|FSRO|Geschäftsordnung|GO)\b')
HINT_STEM = {'satzung': 'satzung', 'finanzordnung': 'finanzordnung',
             'fachschaftsrahmenordnung': 'fachschaftsrahmenordnung',
             'fsro': 'fachschaftsrahmenordnung', 'geschäftsordnung': 'geschaeftsordnung',
             'go': 'geschaeftsordnung'}


def norm_text(text):
    t = ANCHOR.sub('', text)
    t = LINK.sub(lambda m: m.group(1), t)
    t = NUM.sub('§ #', t)
    return re.sub(r'\s+', ' ', t).strip()


def sha(text):
    return hashlib.sha1(norm_text(text).encode('utf-8')).hexdigest()[:12]


def decode(b):
    return b.decode('utf-8').replace('\r\n', NL)


def git(*args):
    r = subprocess.run(['git', '-c', 'core.quotepath=off', *args], cwd=ROOT, capture_output=True)
    return r.returncode, r.stdout


def files_current(only_tracked):
    tracked = None
    if only_tracked:
        rc, out = git('ls-files', '--', *SCAN_DIRS)
        if rc != 0:
            sys.exit('git ls-files fehlgeschlagen - VERWEISE.md nur in einem Git-Checkout erzeugen.')
        tracked = set(decode(out).split(NL))
    files = {}
    for d in SCAN_DIRS:
        for p in sorted((ROOT / d).rglob('*.md')):
            rel = p.relative_to(ROOT).as_posix()
            if tracked is not None and rel not in tracked:
                continue
            files[rel] = decode(p.read_bytes())
    return files


def files_at(ref):
    rc, out = git('ls-tree', '-r', '--name-only', ref, '--', *SCAN_DIRS)
    if rc != 0:
        return None
    files = {}
    for rel in decode(out).split(NL):
        if rel.endswith('.md'):
            rc, data = git('show', f'{ref}:{rel}')
            if rc == 0:
                files[rel] = decode(data)
    return files


class Anchor:
    def __init__(self, doc, aid, kind, rel, line, number, digest, excerpt):
        self.doc, self.id, self.kind, self.rel, self.line = doc, aid, kind, rel, line
        self.number, self.digest, self.excerpt = number, digest, excerpt


class Model:
    """Anker, Verweise und Fliesstext-Verweise eines Dateibestands."""

    def __init__(self, files):
        self.files = files
        self.docs = {}       # Dokumentname -> [Dateien]
        self.owner = {}      # Datei -> Dokumentname
        self.derived = set()  # erzeugte Gesamttexte
        self.anchors = {}    # (doc, id) -> Anchor
        self.dups = []       # (Anchor, Anchor)
        self.mismatch = []   # Anchor
        self.raw_refs = []   # (doc, rel, line, text, target, ctx_id)
        self.plain = []      # (doc, rel, line, text, num, abs, hint, ctx_id)
        self.file_par = {}   # Datei -> Paragraphen-Anker
        self.numbers = {}    # doc -> {Anker: Nummer}
        self.refs = []       # aufgeloeste Verweise (dict)
        self.broken = []     # (Verweis, Grund)
        self._build()

    def _build(self):
        dirs = {Path(r).parent.as_posix(): Path(r).parent.name
                for r in self.files if r.endswith('/aufbau.md')}
        for d, name in dirs.items():
            self.docs[name] = []
            self.derived.add(f'{Path(d).parent.as_posix()}/{name}.md')
        for rel in sorted(self.files):
            parent = Path(rel).parent.as_posix()
            if parent in dirs:
                self.owner[rel] = dirs[parent]
                if not rel.endswith('/aufbau.md'):
                    self.docs[dirs[parent]].append(rel)
            elif rel in self.derived:
                self.owner[rel] = Path(rel).stem
            elif len(Path(rel).parts) == 2:
                self.owner[rel] = Path(rel).stem
                self.docs[Path(rel).stem] = [rel]
        for doc, rels in self.docs.items():
            self.numbers[doc] = {}
            for rel in rels:
                self._parse(doc, rel, self.files[rel])
        for raw in self.raw_refs:
            self._resolve(*raw)

    def _parse(self, doc, rel, text):
        lines = text.split(NL)
        starts = [i for i, l in enumerate(lines) if l.startswith('### ')]
        bounds = starts if starts and starts[0] == 0 else [0] + starts
        for s, e in zip(bounds, bounds[1:] + [len(lines)]):
            block = NL.join(lines[s:e])
            head = lines[s] if lines[s].startswith('### ') else None
            par_id = number = None
            if head:
                hm = re.match(r'### § (\d+[a-z]?)', head)
                number = hm.group(1) if hm else None
                am = ANCHOR.search(head)
                if am and PAR_ID.match(am.group(1)):
                    par_id = am.group(1)
                    self.file_par.setdefault(rel, par_id)
                    if number:
                        self.numbers[doc][par_id] = number
            matches = list(ANCHOR.finditer(block))
            for i, m in enumerate(matches):
                aid = m.group(1)
                in_head = head is not None and m.start() < len(head)
                if in_head and aid == par_id:
                    kind, seg = 'par', block
                else:
                    end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
                    seg = re.sub(r'\s*\d+\)\s*$', '', block[m.start():end])
                    kind = 'abs' if ABS_ID.match(aid) else 'other'
                line = s + 1 + block.count(NL, 0, m.start())
                excerpt = norm_text(seg)[:90]
                a = Anchor(doc, aid, kind, rel, line, number, sha(seg), excerpt)
                if (doc, aid) in self.anchors:
                    self.dups.append((self.anchors[(doc, aid)], a))
                else:
                    self.anchors[(doc, aid)] = a
                mm = ABS_ID.match(aid)
                if kind == 'abs' and par_id and mm and mm.group(1) != par_id:
                    self.mismatch.append(a)

            def ctx_at(pos):
                before = [m for m in matches if m.start() <= pos]
                return before[-1].group(1) if before else None

            for m in LINK.finditer(block):
                target = m.group(2)
                if re.match(r'^(https?:|mailto:|<)', target):
                    continue
                line = s + 1 + block.count(NL, 0, m.start())
                self.raw_refs.append((doc, rel, line, m.group(1), target, ctx_at(m.start())))
            mask = ANCHOR.sub(lambda m: ' ' * len(m.group(0)), block)
            mask = LINK.sub(lambda m: ' ' * len(m.group(0)), mask)
            if head:
                mask = ' ' * len(head) + mask[len(head):]
            for m in PLAIN.finditer(mask):
                tail = mask[m.end():m.end() + 40]
                ext = EXTERNAL.match(tail)
                if ext and ext.group(1) not in ('GO',):
                    continue
                hm = DOC_HINT.search(tail)
                hint = None
                if hm:
                    key = HINT_STEM[hm.group(1).lower()]
                    hint = next((d for d in self.docs if d.startswith(key)), None)
                line = s + 1 + block.count(NL, 0, m.start())
                self.plain.append((doc, rel, line, m.group(0).strip(), m.group(1), m.group(2),
                                   hint, ctx_at(m.start())))

    def _resolve(self, doc, rel, line, text, target, ctx):
        path, _, frag = target.partition('#')
        ref = {'doc': doc, 'rel': rel, 'line': line, 'text': text, 'target': target,
               'ctx': ctx, 'to_doc': None, 'to_id': None}
        if path == '':
            to_rel = rel
        else:
            to_rel = posixpath.normpath(posixpath.join(posixpath.dirname(rel), path))
            if not to_rel.endswith('.md') or to_rel.split('/')[0] not in SCAN_DIRS:
                return
            if to_rel.endswith('/aufbau.md'):
                return
            if to_rel not in self.files:
                self.refs.append(ref)
                self.broken.append((ref, f'Datei nicht gefunden: {to_rel}'))
                return
        to_doc = self.owner.get(to_rel)
        if to_doc is None:
            return
        anchor = frag or self.file_par.get(to_rel)
        ref['to_doc'], ref['to_id'] = to_doc, anchor
        self.refs.append(ref)
        if anchor and (to_doc, anchor) not in self.anchors:
            self.broken.append((ref, f'Anker "{anchor}" gibt es in {to_doc} nicht'))

    def label(self, doc, aid):
        a = self.anchors.get((doc, aid))
        if a is None:
            return f'{doc} #{aid}'
        s = f'{doc} § {a.number}' if a.number else f'{doc} #{aid}'
        m = ABS_ID.match(aid)
        if a.kind == 'abs' and m:
            s += f' Abs. {m.group(2)}'
        return s

    def referrer(self, ref):
        if ref['ctx']:
            return self.label(ref['doc'], ref['ctx'])
        return f'{ref["doc"]} ({Path(ref["rel"]).name})'

    def referrers_of(self, doc, aid):
        return [r for r in self.refs if r['to_doc'] == doc and r['to_id'] == aid]


def find(items, msg, rel=None, line=None):
    items.append({'msg': msg, 'file': rel, 'line': line})


def run_checks(cur, base):
    errors, alarms, hints = [], [], []
    for a, b in cur.dups:
        find(errors, f'Anker-ID "{b.id}" kommt in {b.doc} doppelt vor (auch in {a.rel}:{a.line}). '
                     f'Verweise landen dann beim falschen Absatz.', b.rel, b.line)
    for ref, why in cur.broken:
        msg = f'Kaputter Verweis von {cur.referrer(ref)}: {why}'
        if base and ref['to_doc'] and (ref['to_doc'], ref['to_id']) in base.anchors:
            msg += ' (im Vergleichsstand vorhanden: Anker wurde entfernt oder umbenannt)'
        find(errors, msg, ref['rel'], ref['line'])
    for a in cur.mismatch:
        find(hints, f'Absatz-Anker "{a.id}" passt nicht zum Paragraphen-Anker der Datei '
                    f'(erwartet z.B. "{cur.file_par.get(a.rel)}-N").', a.rel, a.line)
    if base is None:
        return errors, alarms, hints

    def who(doc, aid):
        found = {}
        for m in (cur, base):
            for r in m.referrers_of(doc, aid):
                found.setdefault(m.referrer(r), (r['rel'], r['line']))
        return found

    for (doc, aid), old in sorted(base.anchors.items()):
        new = cur.anchors.get((doc, aid))
        refs = who(doc, aid)
        if new is None:
            same = [a for (d, i), a in cur.anchors.items() if d == doc and a.digest == old.digest]
            tip = f' Vermutlich umbenannt zu "{same[0].id}".' if same else ''
            if refs:
                find(errors, f'Anker "{aid}" ({base.label(doc, aid)}) ist verschwunden, wird aber '
                             f'verwiesen von: {", ".join(refs)}.{tip}', old.rel, old.line)
            else:
                find(hints, f'Anker "{aid}" ({base.label(doc, aid)}) ist verschwunden; '
                            f'es gab keinen Verweis darauf.{tip}', old.rel, old.line)
        elif new.digest != old.digest and refs:
            where = '; '.join(f'{k}' for k in refs)
            find(alarms, f'{cur.label(doc, aid)} wurde geaendert. Verweise darauf pruefen: {where}.',
                 new.rel, new.line)

    for doc, rel, line, text, num, absn, hint, ctx in cur.plain:
        tdoc = hint or doc
        if tdoc not in base.numbers or tdoc not in cur.numbers:
            continue
        old_id = next((i for i, n in base.numbers[tdoc].items() if n == num), None)
        if old_id is None:
            continue
        now = cur.numbers[tdoc].get(old_id)
        if now != num:
            where = f'jetzt § {now}' if now else 'Paragraph entfernt'
            find(hints, f'Fliesstext-Verweis "{text}" in {cur.referrer({"doc": doc, "rel": rel, "ctx": ctx})}: '
                        f'gemeint war wohl {tdoc} #{old_id}, das ist {where}.', rel, line)
    return errors, alarms, hints


def write_liste(cur, path):
    def excerpt(doc, aid):
        a = cur.anchors.get((doc, aid))
        return a.excerpt if a else ''

    by_target = {}
    for r in cur.refs:
        if r['to_id']:
            by_target.setdefault((r['to_doc'], r['to_id']), []).append(r)
    out = ['# Querverweise', '',
           '> **Automatisch erzeugt – bitte nicht bearbeiten.** Die Liste entsteht bei jedem Push aus '
           '`tools/check_verweise.py --write-liste`. Sie zeigt, wer auf welchen Paragraphen/Absatz '
           'verweist. Wird ein hier gelistetes Ziel geändert, schlägt die Prüfung Alarm '
           '(siehe README, Abschnitt „Querverweise prüfen“).', '',
           f'{len(cur.refs)} Verweise mit Link, {len(cur.plain)} Verweise im Fließtext.', '',
           '## Verweise mit Link, nach Ziel', '']
    if by_target:
        out += ['| Ziel | Textauszug | Verwiesen von |', '|---|---|---|']
        order = sorted(by_target, key=lambda k: (k[0], cur.numbers.get(k[0], {}).get(k[1].split('-')[0], '0').zfill(4), k[1]))
        for (doc, aid) in order:
            who = '<br>'.join(sorted({cur.referrer(r) for r in by_target[(doc, aid)]}))
            out.append(f'| {cur.label(doc, aid)} (`{aid}`) | {excerpt(doc, aid).replace("|", "/")[:70]} | {who} |')
    else:
        out.append('_Noch keine Verweise mit Link._')
    out += ['', '## Verweise im Fließtext (nicht automatisch geprüft)', '',
            'Diese Verweise sind nur Text („§ 5 Abs. 2“). Sie werden nur als Hinweis geprüft, '
            'wenn sich Nummern verschieben. Wer sie als Link schreibt '
            '(`[§ 5 Abs. 2](../satzung/….md#p5-2)`), bekommt die volle Prüfung.', '']
    if cur.plain:
        out += ['| Von | Verweis | Stelle |', '|---|---|---|']
        for doc, rel, line, text, num, absn, hint, ctx in cur.plain:
            out.append(f'| {cur.referrer({"doc": doc, "rel": rel, "ctx": ctx})} | {text}'
                       f'{" (" + hint + ")" if hint else ""} | {rel}:{line} |')
    else:
        out.append('_Keine._')
    Path(path).write_text(NL.join(out) + NL, encoding='utf-8', newline=NL)


def report(errors, alarms, hints, github):
    def emit(level, items, title):
        if not items:
            return
        print(f'\n{title} ({len(items)})')
        for it in items:
            loc = f' [{it["file"]}:{it["line"]}]' if it['file'] else ''
            print(f'  - {it["msg"]}{loc}')
            if github and level != 'notice':
                extra = f'file={it["file"]},line={it["line"]}::' if it['file'] else '::'
                print(f'::{level} {extra}{it["msg"]}')

    emit('error', errors, 'FEHLER')
    emit('warning', alarms, 'ALARM: geaenderte Ziele mit Verweisen')
    emit('notice', hints, 'HINWEISE')
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary, 'a', encoding='utf-8') as f:
            f.write('## Querverweise\n\n')
            if not (errors or alarms or hints):
                f.write('Alles in Ordnung.\n')
            for title, items in (('Fehler', errors), ('Alarm – Verweise prüfen', alarms), ('Hinweise', hints)):
                if items:
                    f.write(f'### {title}\n\n')
                    for it in items:
                        f.write(f'- {it["msg"]}\n')
                    f.write('\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split(NL)[0])
    ap.add_argument('--base', default='origin/main', help='Vergleichsstand (Git-Ref) oder "none"')
    ap.add_argument('--write-liste', nargs='?', const='VERWEISE.md', metavar='DATEI',
                    help='Liste aller Verweise schreiben (nur versionierte Dateien)')
    ap.add_argument('--github', action='store_true', default=bool(os.environ.get('GITHUB_ACTIONS')),
                    help='Annotationen fuer GitHub Actions ausgeben')
    args = ap.parse_args()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    if args.write_liste:
        cur = Model(files_current(only_tracked=True))
        write_liste(cur, ROOT / args.write_liste)
        print(f'geschrieben: {args.write_liste} ({len(cur.refs)} Verweise)')
        return 0

    cur = Model(files_current(only_tracked=False))
    base = None
    if args.base and args.base.lower() != 'none':
        files = files_at(args.base)
        if files is None:
            print(f'Hinweis: Vergleichsstand "{args.base}" nicht gefunden - nur Ist-Zustand geprueft.')
        else:
            base = Model(files)
            print(f'Vergleich mit {args.base}.')
    errors, alarms, hints = run_checks(cur, base)
    print(f'{len(cur.anchors)} Anker, {len(cur.refs)} Verweise mit Link, '
          f'{len(cur.plain)} im Fliesstext, {len(cur.docs)} Dokumente.')
    report(errors, alarms, hints, args.github)
    if errors:
        return 1
    if alarms:
        return 3
    print('\nOK: keine Probleme gefunden.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
