# Ordnungen und Satzungen der Studierendenschaft der Hochschule Niederrhein

Dieses Repository sammelt die **Entwürfe** für die Neufassung der Satzung sowie
diverser Ordnungen der Studierendenschaft der Hochschule Niederrhein. Ziel ist
es, die Weiterarbeit an diesen Texten für mehrere Mitwirkende über GitHub zu
ermöglichen – mit Versionsgeschichte, nachvollziehbaren Änderungen (Diffs) und
Diskussion einzelner Formulierungen über Pull Requests.

**Status:** Alle Dokumente in diesem Repo sind Arbeitsentwürfe und noch nicht
durch ein Organ der Studierendenschaft (StuPa) beschlossen, sofern nicht
anders vermerkt.

Falls du zum ersten Mal mit GitHub arbeitest: In [CONTRIBUTING.md](CONTRIBUTING.md)
steht Schritt für Schritt, wie du Änderungsvorschläge einreichen kannst.

## Struktur

```
satzung/ Die Satzung der Studierendenschaft (Grundordnung)
ordnungen/ Ergänzende Ordnungen (Fachschaftsrahmenordnung, Finanzordnung)
vorlagen/ Muster-/Beispieldokumente (z.B. Erklärungen, Formulare)
```

## Warum Markdown statt Word?

Die Entwürfe wurden von `.docx` nach Markdown (`.md`) konvertiert, weil sich
Markdown-Dateien in Git sinnvoll vergleichen (diffen) und in Pull Requests
zeilengenau kommentieren lassen – bei Word-Dateien funktioniert das praktisch
nicht. GitHub stellt `.md`-Dateien automatisch lesbar formatiert dar (Titel,
Abschnitte, Überschriften), ganz ohne zusätzliche Software.

## Wichtige Konvention: § und Absatz-Nummerierung

In den Original-Word-Dokumenten wurden §-Nummern und Absatznummern
`(1)`, `(2)`, ... automatisch von Word vergeben. In den Markdown-Dateien sind
sie als **echte Markdown-Listen** umgesetzt, damit sie sauber gerendert
werden und sich mit den üblichen Editor-Werkzeugen bearbeiten lassen:

- `## Teil N ...` – Abschnitt (Teil) einer Ordnung
- `### § N Titel` – Paragraph (mit unsichtbarer Anker-ID, siehe unten)
- `1) ...`, `2) ...` – Absätze innerhalb eines Paragraphen, als nummerierte
Liste (Klammer-Schreibweise `(1)` ist in Markdown-Listen technisch nicht
möglich, deshalb `1)` statt `(1)`)
- ` 1. ...`, ` a. ...` – Unterpunkte innerhalb eines Absatzes, eine Ebene
eingerückt

**Renummerierungs-Risiko:** Markdown-Listen nummerieren beim Rendern
automatisch durch. Fügt jemand einen Absatz ein oder löscht einen, verschieben
sich alle folgenden Nummern automatisch – bestehende Verweise wie "gemäß § 5
Abs. 2" an anderer Stelle würden dann unbemerkt auf den falschen Absatz
zeigen. **Nach jedem Einfügen/Löschen eines Absatzes deshalb gezielt nach
Verweisen auf die alte Nummerierung suchen** (Volltextsuche nach `§ N` bzw.
`Abs.` im ganzen Repo) und diese von Hand korrigieren.

## Stabile Anker für Querverweise

Jeder `§`-Heading und jeder Absatz hat eine feste, unsichtbare Anker-ID, die
bei einer späteren Umnummerierung **nicht mitverschoben wird**:

```
### § 14 Redeliste <a id="p14"></a>

1) <a id="p14-1"></a>Die Redeleitung führt eine Redeliste ...
```

Ein Verweis im Text wird als Markdown-Link auf diese ID gesetzt:

```
... Bestimmungen zu Ordnungsmaßnahmen ([§ 14](#p14)) sowie ...
```

Verweis in eine andere Datei: Dateipfad vor das `#` schreiben, z.B.
`[§ 7 Finanzordnung](../ordnungen/finanzordnung.md#p7)`.

**Warum das hilft:** Der Link zeigt immer auf dieselbe physische Stelle,
auch wenn sich die dort sichtbare §- oder Absatznummer später ändert. Fällt
die Nummer im Linktext dann nicht mehr mit der Nummer an der Zielstelle
zusammen, ist das ein sichtbares Warnsignal beim Lesen, dass der Linktext
aktualisiert werden muss – der Sprung führt aber trotzdem an die richtige
Stelle.

Beim Einfügen eines neuen § oder Absatzes: der neuen Stelle ebenfalls eine
Anker-ID nach demselben Schema geben (`p<§-Nummer>` bzw.
`p<§-Nummer>-<Absatz-Nummer>`, basierend auf der Nummer zum Zeitpunkt der
Einführung – die ID muss danach nicht mehr angepasst werden, auch wenn sich
die sichtbare Nummer später ändert).
