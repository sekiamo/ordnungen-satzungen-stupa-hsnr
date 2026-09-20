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

Verweise zwischen Paragraphen desselben Dokuments werden in den Einzeldateien
als Dateilinks geschrieben, z.B. [§ 14](p14-redeliste.md), und beim Bauen in
Anker-Links auf den Gesamttext umgewandelt ([§ 14](#p14)).

Neue Paragraphen: Der Link "Neuen Paragraphen danach einfügen" im Gesamttext
öffnet den GitHub-Editor mit einer Vorlage, die in der ersten Zeile
    <!-- einfuegen-nach: p07-kassenanordnungen.md -->
enthält. Beim nächsten Bauen trägt dieses Skript die neue Datei automatisch in
aufbau.md hinter dem genannten Paragraphen ein und entfernt die Markierung.
Eine Datei ohne diese Markierung, die nicht in aufbau.md steht, ist ein Fehler.

Das Skript enthält keine repo-spezifischen Daten: Besitzer/Repo für die Links
kommen aus GITHUB_REPOSITORY bzw. der origin-URL des Git-Checkouts.
"""
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
BRANCH = 'main'

INCLUDE = re.compile(r'^- \[[^\]]*\]\(([^)\s]+\.md)\)\s*$')
HEADING = re.compile(r'^(#{1,2}) (.+?)\s*$')
SECTION_ID = re.compile(r'^### .*<a id="(p\d+[a-z]*)"></a>', re.M)
SECTION_TITLE = re.compile(r'^### (.*?)\s*<a id="p\d+[a-z]*"></a>', re.M)
LINK = re.compile(r'\]\(([^)#\s]+\.md)(#[^)\s]*)?\)')
MARKER = re.compile(r'\A<!--\s*einfuegen-nach:\s*(\S+\.md)\s*-->[ \t]*\n')

TEMPLATE = ('### § N Titel  <a id="pN"></a>\n\n'
            '1) <a id="pN-1"></a>Text des ersten Absatzes.\n')


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
    return path.read_bytes().decode('utf-8').replace('\r\n', '\n')


def build(aufbau):
    """Liefert (Dateiname des Gesamttexts, Text, {Pfad: neuer Text} für weitere Dateien)."""
    rel_aufbau = aufbau.relative_to(ROOT)
    doc_dir = aufbau.parent
    lines = read(aufbau).split('\n')
    writes = {}

    def include_target(line):
        m = INCLUDE.match(line)
        return m.group(1) if m else None

    # 1. Neue, noch nicht eingetragene Paragraphen (mit Markierung) einsortieren
    listed = {include_target(l) for l in lines} | {'aufbau.md'}
    placed_after = {}
    for path in sorted(doc_dir.glob('*.md')):
        if path.name in listed:
            continue
        text = read(path)
        m = MARKER.match(text)
        if not m:
            raise SystemExit(
                f'{rel_aufbau}: {path.name} ist nicht in aufbau.md eingetragen und hat keine '
                f'Markierung "<!-- einfuegen-nach: <datei>.md -->" in der ersten Zeile.')
        after = m.group(1)
        anchor = placed_after.get(after, after)
        idx = next((i for i, l in enumerate(lines) if include_target(l) == anchor), None)
        if idx is None:
            raise SystemExit(f'{path.relative_to(ROOT)}: "einfuegen-nach: {after}" – '
                             f'diese Datei steht nicht in aufbau.md.')
        body = text[m.end():].lstrip('\n')
        t = SECTION_TITLE.search(body)
        label = t.group(1) if t else path.stem
        lines.insert(idx + 1, f'- [{label}]({path.name})')
        placed_after[after] = path.name
        writes[path] = body
        writes[aufbau] = '\n'.join(lines)

    def content(path):
        return writes[path] if path in writes else read(path)

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
        path = doc_dir / val
        if not path.is_file():
            raise SystemExit(f'{rel_aufbau}: Datei fehlt: {val}')
        m = SECTION_ID.search(content(path))
        if m:
            if m.group(1) in anchors.values():
                raise SystemExit(f'{path.relative_to(ROOT)}: Anker-ID {m.group(1)} kommt in '
                                 f'diesem Dokument schon vor.')
            anchors[val] = m.group(1)
        elif not val.startswith('00-'):
            raise SystemExit(f'{path.relative_to(ROOT)}: Überschrift fehlt oder ungültig. '
                             f'Erwartet: "### § 5 Titel  <a id=\"p5\"></a>" '
                             f'(Platzhalter N und Titel ersetzen).')

    listed = {val for kind, val in order if kind == 'file'} | {'aufbau.md'}

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
        template = f'<!-- einfuegen-nach: {val} -->\n{TEMPLATE}'
        new = (f'{base}/new/{BRANCH}/{quote(doc_rel)}?filename={quote("pNN-kurztitel.md")}'
               f'&value={quote(template, safe="")}')
        link = (f'<sub>[✏️ Diesen Paragraphen bearbeiten]({edit}) · '
                f'[➕ Neuen Paragraphen danach einfügen]({new})</sub>')
        head, _, rest = text.partition('\n')
        return f'{head}\n\n{link}\n{rest}'

    parts = []
    title_done = False
    for kind, val in order:
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
            body = LINK.sub(rewrite, content(doc_dir / val)).strip('\n')
            parts.append(with_action_links(val, body))
    return doc_dir.name + '.md', '\n\n'.join(parts) + '\n', writes


def main():
    check = '--check' in sys.argv[1:]
    stale = []
    for aufbau in sorted(ROOT.glob('**/aufbau.md')):
        if '.git' in aufbau.parts:
            continue
        name, text, writes = build(aufbau)
        writes[aufbau.parent.parent / name] = text
        for target, new_text in writes.items():
            new_text = new_text.rstrip('\n') + '\n'
            current = read(target) if target.exists() else None
            if current == new_text:
                continue
            rel = target.relative_to(ROOT).as_posix()
            if check:
                stale.append(rel)
            else:
                target.write_text(new_text, encoding='utf-8', newline='\n')
                print('aktualisiert:', rel)
    if check and stale:
        print('Nicht aktuell (bitte "python tools/build_gesamttext.py" ausführen):')
        for s in stale:
            print('  ', s)
        sys.exit(1)


if __name__ == '__main__':
    main()
