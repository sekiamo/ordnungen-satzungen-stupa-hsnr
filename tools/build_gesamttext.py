#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut aus den Einzelparagraphen den lesbaren Gesamttext.

Jedes Dokument (Satzung, Ordnung) liegt als Verzeichnis mit einer Datei pro
Paragraph vor, z.B. ordnungen/finanzordnung/. Die Datei aufbau.md in diesem
Verzeichnis legt Reihenfolge und Teil-Überschriften fest. Aus allem zusammen
wird ordnungen/finanzordnung.md erzeugt.

Aufruf (aus dem Repo-Root oder von überall):

    python tools/build_gesamttext.py          # Gesamttexte neu erzeugen
    python tools/build_gesamttext.py --check  # nur prüfen, ob sie aktuell sind

Regeln für aufbau.md:
  - eine Zeile "# Titel" ist die Dokument-Überschrift,
  - Zeilen "## Teil ..." werden als Teil-Überschrift übernommen,
  - Zeilen "- [Text](datei.md)" binden die Datei an dieser Stelle ein,
  - alles andere (Zitatblöcke, Leerzeilen, Erklärtext) wird ignoriert.

Automatische Nummerierung: Die sichtbare §-Nummer ergibt sich allein aus der
Reihenfolge in aufbau.md. Das Skript schreibt sie in die Überschriften der
Paragraphen-Dateien, in aufbau.md und in die Linktexte von Verweisen
("[§ 14](p14-redeliste.md)"). Die Anker-IDs (<a id="p14">) bleiben unverändert.
Verweise, die nur als Text im Fließtext stehen ("gemäß § 5 Abs. 2"), kann das
Skript nicht sicher zuordnen; es listet sie nach einer Umnummerierung auf.

Verweise zwischen Paragraphen desselben Dokuments werden in den Einzeldateien
als Dateilinks geschrieben, z.B. [§ 14](p14-redeliste.md), und beim Bauen in
Anker-Links auf den Gesamttext umgewandelt ([§ 14](#p14)). Verweise in ein
anderes Dokument: [§ 7 Finanzordnung](../ordnungen/finanzordnung.md#p7).

Neue Paragraphen: Der Link "Neuen Paragraphen danach einfügen" im Gesamttext
öffnet den GitHub-Editor mit einer Vorlage, die in der ersten Zeile
    <!-- einfuegen-nach: p07-kassenanordnungen.md -->
enthält. Beim nächsten Bauen trägt dieses Skript die neue Datei automatisch
hinter dem genannten Paragraphen in aufbau.md ein, vergibt Anker-ID (z.B. p7a)
und Dateinamen, ersetzt die Platzhalter "N" und entfernt die Markierung. Die
Nummern aller folgenden Paragraphen werden dabei angepasst. Eine Datei ohne
Markierung, die nicht in aufbau.md steht, ist ein Fehler.

Das Skript enthält keine repo-spezifischen Daten: Besitzer/Repo für die Links
kommen aus GITHUB_REPOSITORY bzw. der origin-URL des Git-Checkouts.
"""
import os
import re
import string
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
BRANCH = 'main'
NL = chr(10)

INCLUDE = re.compile(r'^- \[[^\]]*\]\(([^)\s]+\.md)\)\s*$')
INCLUDE_LABEL = re.compile(r'^(- \[§ )(\d+|N)([^\]]*\]\(([^)\s]+\.md)\)\s*)$')
HEADING = re.compile(r'^(#{1,2}) (.+?)\s*$')
SECTION_ID = re.compile(r'^### .*<a id="(p\d+[a-z]*)"></a>', re.M)
NEW_HEADING = re.compile(r'^### § (?:\d+|N)\s+(.*?)\s*<a id="[^"]*"></a>\s*$', re.M)
NUM_HEADING = re.compile(r'^(### § )(\d+|N)(?=\s)', re.M)
LINK = re.compile(r'\]\(([^)#\s]+\.md)(#[^)\s]*)?\)')
LINK_TEXT = re.compile(r'\[§ (\d+)([^\]]*)\]\(([^)\s#]+\.md)(#[^)\s]*)?\)')
MARKER = re.compile(r'\A<!--\s*einfuegen-nach:\s*(\S+\.md)\s*-->[ \t]*\n')

TEMPLATE = ('### § N Titel  <a id="pN"></a>' + NL + NL +
            '1) <a id="pN-1"></a>Text des ersten Absatzes.' + NL)


def repo_slug():
    """'besitzer/repo' aus GITHUB_REPOSITORY oder der origin-URL; sonst None."""
    slug = os.environ.get('GITHUB_REPOSITORY')
    if not slug:
        try:
            url = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=ROOT,
                                 capture_output=True, text=True).stdout.strip()
        except OSError:
            return None
        m = re.search(r'github\.com[:/]([^/]+/[^/]+?)(?:\.git)?$', url)
        slug = m.group(1) if m else None
    return slug


def read(path):
    return path.read_bytes().decode('utf-8').replace('\r\n', NL)


def file_slug(title, n=56):
    for a, b in (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('Ä', 'ae'), ('Ö', 'oe'), ('Ü', 'ue'), ('ß', 'ss')):
        title = title.replace(a, b)
    t = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode().lower()
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    if len(t) > n:
        t = t[:n].rsplit('-', 1)[0]
    return t or 'paragraph'


def include_target(line):
    m = INCLUDE.match(line)
    return m.group(1) if m else None


def prepare(aufbau):
    """Liest ein Dokument, sortiert neue Paragraphen ein und nummeriert durch."""
    rel_aufbau = aufbau.relative_to(ROOT)
    doc_dir = aufbau.parent
    lines = read(aufbau).split(NL)
    disk_aufbau = NL.join(lines)
    contents = {}          # Dateiname -> Inhalt (nach allen Änderungen)
    deleted = set()        # Pfade, die gelöscht werden (umbenannte neue Dateien)

    def content(name):
        if name not in contents:
            contents[name] = read(doc_dir / name)
        return contents[name]

    # 1. Neue, noch nicht eingetragene Paragraphen (mit Markierung) einsortieren
    listed = {include_target(l) for l in lines} | {'aufbau.md'}
    used_anchors = set()
    for name in listed - {'aufbau.md', None}:
        m = SECTION_ID.search(content(name))
        if m:
            used_anchors.add(m.group(1))
    placed_after = {}
    orphans = [p for p in sorted(doc_dir.glob('*.md')) if p.name not in listed]
    for path in orphans:
        text = read(path)
        m = MARKER.match(text)
        if not m:
            raise SystemExit(
                f'{rel_aufbau}: {path.name} ist nicht in aufbau.md eingetragen und hat keine '
                f'Markierung "<!-- einfuegen-nach: <datei>.md -->" in der ersten Zeile.')
        after = m.group(1)
        pred = placed_after.get(after, after)
        idx = next((i for i, l in enumerate(lines) if include_target(l) == pred), None)
        if idx is None:
            raise SystemExit(f'{path.relative_to(ROOT)}: "einfuegen-nach: {after}" – '
                             f'diese Datei steht nicht in aufbau.md.')
        body = text[m.end():].lstrip(NL)
        h = NEW_HEADING.search(body)
        if not h:
            raise SystemExit(f'{path.relative_to(ROOT)}: Überschrift fehlt oder ungültig. '
                             f'Erwartet: "### § N Titel  <a id=\"pN\"></a>".')
        title = h.group(1)
        if title.strip() in ('', 'Titel'):
            raise SystemExit(f'{path.relative_to(ROOT)}: Bitte den Platzhalter "Titel" in der '
                             f'Überschrift durch den echten Titel ersetzen.')
        if 'id="pN"' in body:
            pm = SECTION_ID.search(content(pred))
            base = re.match(r'p\d+', pm.group(1)).group(0) if pm else 'p0'
            anchor = next(base + s for s in string.ascii_lowercase if base + s not in used_anchors)
            body = body.replace('id="pN"', f'id="{anchor}"').replace('id="pN-', f'id="{anchor}-')
        am = SECTION_ID.search(body)
        if not am:
            raise SystemExit(f'{path.relative_to(ROOT)}: Anker-ID ungültig (erwartet z.B. p7a).')
        anchor = am.group(1)
        if anchor in used_anchors:
            raise SystemExit(f'{path.relative_to(ROOT)}: Anker-ID {anchor} kommt in diesem '
                             f'Dokument schon vor.')
        used_anchors.add(anchor)
        dm = re.match(r'p(\d+)([a-z]*)$', anchor)
        new_name = f'p{int(dm.group(1)):02d}{dm.group(2)}-{file_slug(title)}.md'
        while new_name in listed or (doc_dir / new_name).exists() and new_name != path.name:
            new_name = new_name[:-3] + '-2.md'
        contents[new_name] = body
        deleted.add(path)
        lines.insert(idx + 1, f'- [§ N {title}]({new_name})')
        placed_after[after] = new_name
        listed.add(new_name)

    # 2. Reihenfolge lesen
    order = []            # (Art, Inhalt)
    for line in lines:
        target = include_target(line)
        if target:
            order.append(('file', target))
            continue
        m = HEADING.match(line)
        if m:
            order.append(('head', line.rstrip()))

    # 3. Anker jeder Paragraphen-Datei (Dateien "00-..." sind Vorspann ohne Anker)
    anchors = {}
    for kind, val in order:
        if kind != 'file':
            continue
        if not (doc_dir / val).is_file() and val not in contents:
            raise SystemExit(f'{rel_aufbau}: Datei fehlt: {val}')
        m = SECTION_ID.search(content(val))
        if m:
            if m.group(1) in anchors.values():
                raise SystemExit(f'{(doc_dir / val).relative_to(ROOT)}: Anker-ID {m.group(1)} '
                                 f'kommt in diesem Dokument schon vor.')
            anchors[val] = m.group(1)
        elif not val.startswith('00-'):
            raise SystemExit(f'{(doc_dir / val).relative_to(ROOT)}: Überschrift fehlt oder '
                             f'ungültig. Erwartet: "### § 5 Titel  <a id=\"p5\"></a>".')

    # 4. Durchnummerieren nach Reihenfolge in aufbau.md
    numbers = {}
    for kind, val in order:
        if kind == 'file' and val in anchors:
            numbers[val] = len(numbers) + 1
    renumbered = False
    for val, n in numbers.items():
        old = content(val)
        new = NUM_HEADING.sub(lambda m: f'{m.group(1)}{n}', old, count=1)
        if new != old:
            contents[val] = new
            on_disk = NUM_HEADING.search(read(doc_dir / val)) if (doc_dir / val).is_file() else None
            if on_disk is None or on_disk.group(2) != str(n):
                renumbered = True
    for i, l in enumerate(lines):
        m = INCLUDE_LABEL.match(l)
        if m and m.group(4) in numbers:
            lines[i] = f'{m.group(1)}{numbers[m.group(4)]}{m.group(3)}'

    return {'aufbau': aufbau, 'doc_dir': doc_dir, 'lines': lines, 'order': order,
            'contents': contents, 'anchors': anchors, 'numbers': numbers,
            'deleted': deleted, 'renumbered': renumbered, 'disk_aufbau': disk_aufbau,
            'anchor_numbers': {a: numbers[f] for f, a in anchors.items()}}


def finish(doc, all_docs):
    """Verweis-Linktexte anpassen, Gesamttext bauen. Liefert (name, text, writes)."""
    aufbau, doc_dir = doc['aufbau'], doc['doc_dir']
    contents, anchors, numbers = doc['contents'], doc['anchors'], doc['numbers']
    listed = {val for kind, val in doc['order'] if kind == 'file'} | {'aufbau.md'}

    def relabel(m):
        num, rest, target, frag = m.group(1), m.group(2), m.group(3), m.group(4)
        new = None
        if '/' not in target:
            new = numbers.get(target)
        else:
            other = all_docs.get(Path(target).stem)
            fm = re.match(r'#(p\d+[a-z]*)', frag or '')
            if other and fm:
                new = other['anchor_numbers'].get(fm.group(1))
        if new is None or str(new) == num:
            return m.group(0)
        return m.group(0).replace(f'[§ {num}', f'[§ {new}', 1)

    for val in list(numbers) + [v for k, v in doc['order'] if k == 'file' and v not in numbers]:
        contents[val] = LINK_TEXT.sub(relabel, contents[val])

    # Geänderte Dateien bestimmen
    writes = {}
    for path in doc['deleted']:
        writes[path] = None
    for val, text in contents.items():
        path = doc_dir / val
        if val in listed and (not path.is_file() or read(path) != text):
            writes[path] = text
    new_aufbau = NL.join(doc['lines'])
    if new_aufbau != doc['disk_aufbau']:
        writes[aufbau] = new_aufbau

    if doc['renumbered']:
        print(f'Hinweis: In {doc_dir.name} wurden Paragraphen umnummeriert. Verweise, die nur als '
              f'Text im Fließtext stehen, werden nicht automatisch angepasst – bitte prüfen:')
        plain = re.compile(r'§\s*\d+(?:\s*(?:Abs\.|Absatz)\s*\d+)?')
        for val in numbers:
            for line in contents[val].split(NL):
                if line.startswith('### '):
                    continue
                stripped = re.sub(r'\[[^\]]*\]\([^)]*\)', '', line)
                for m in plain.finditer(stripped):
                    print(f'   {val}: "{m.group(0)}"')

    # Rewrite: Dateilinks -> Sprungmarken
    def rewrite(m):
        target, frag = m.group(1), m.group(2)
        if '/' in target or target not in listed:
            return m.group(0)
        if frag:
            return f']({frag})'
        if target in anchors:
            return f'](#{anchors[target]})'
        return m.group(0)

    slug = repo_slug()
    doc_rel = doc_dir.relative_to(ROOT).as_posix()

    def with_action_links(val, text):
        """Fügt unter der §-Überschrift Links zum Bearbeiten / Einfügen ein."""
        if not slug or val not in anchors:
            return text
        base = f'https://github.com/{slug}'
        edit = f'{base}/edit/{BRANCH}/{quote(doc_rel + "/" + val)}'
        template = f'<!-- einfuegen-nach: {val} -->' + NL + TEMPLATE
        new = (f'{base}/new/{BRANCH}/{quote(doc_rel)}?filename={quote("neu.md")}'
               f'&value={quote(template, safe="")}')
        link = (f'<sub>[✏️ Diesen Paragraphen bearbeiten]({edit}) · '
                f'[➕ Neuen Paragraphen danach einfügen]({new})</sub>')
        head, _, rest = text.partition(NL)
        return f'{head}{NL}{NL}{link}{NL}{rest}'

    parts = []
    title_done = False
    for kind, val in doc['order']:
        if kind == 'head':
            parts.append(val)
            if not title_done and val.startswith('# '):
                title_done = True
                parts.append(
                    f'> **Gesamttext – bitte hier nicht bearbeiten.** Diese Datei wird '
                    f'automatisch aus den Einzelparagraphen in '
                    f'[`{doc_dir.name}/`]({doc_dir.name}/aufbau.md) erzeugt. '
                    f'Änderungen gehören in die jeweilige Paragraphen-Datei dort.')
        else:
            body = LINK.sub(rewrite, contents[val]).strip(NL)
            parts.append(with_action_links(val, body))
    return doc_dir.name + '.md', (NL + NL).join(parts) + NL, writes


def main():
    check = '--check' in sys.argv[1:]
    aufbaus = [a for a in sorted(ROOT.glob('**/aufbau.md')) if '.git' not in a.parts]
    docs = {a.parent.name: prepare(a) for a in aufbaus}
    stale = []
    for name, doc in docs.items():
        out_name, text, writes = finish(doc, docs)
        writes[doc['doc_dir'].parent / out_name] = text
        for target, new_text in writes.items():
            rel = target.relative_to(ROOT).as_posix()
            if new_text is None:
                if target.exists():
                    if check:
                        stale.append(rel)
                    else:
                        target.unlink()
                        print('entfernt:', rel)
                continue
            new_text = new_text.rstrip(NL) + NL
            current = read(target) if target.exists() else None
            if current == new_text:
                continue
            if check:
                stale.append(rel)
            else:
                target.write_text(new_text, encoding='utf-8', newline=NL)
                print('aktualisiert:', rel)
    if check and stale:
        print('Nicht aktuell (bitte "python tools/build_gesamttext.py" ausführen):')
        for s in stale:
            print('  ', s)
        sys.exit(1)


if __name__ == '__main__':
    main()
