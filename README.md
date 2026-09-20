# Ordnungen und Satzungen der Studierendenschaft der Hochschule Niederrhein

Dieses Repository sammelt die **Entwürfe** für die Neufassung der Satzung sowie
diverser Ordnungen der Studierendenschaft der Hochschule Niederrhein. Ziel ist
es, die Weiterarbeit an diesen Texten für mehrere Mitwirkende über GitHub zu
ermöglichen – mit Versionsgeschichte, nachvollziehbaren Änderungen (Diffs) und
Diskussion einzelner Formulierungen über Pull Requests.

**Status:** Alle Dokumente in diesem Repo sind Arbeitsentwürfe und noch nicht
durch ein Organ der Studierendenschaft (StuPa) beschlossen, sofern nicht
anders vermerkt.

Zum ersten Mal auf GitHub? Dann fang mit [CONTRIBUTING.md](CONTRIBUTING.md) an.

## Dokumente

Zum **Lesen** führt der Link in der Mitte zum kompletten Text; zum **Bearbeiten** gibt es
jeden Paragraphen als eigene Datei (rechte Spalte, siehe
[Einzelparagraphen und Gesamttext](TECHNIK.md#einzelparagraphen-und-gesamttext)).

| Dokument | Gesamttext lesen | Paragraphen bearbeiten |
|---|---|---|
| Satzung der Studierendenschaft | [satzung/satzung-der-studierendenschaft.md](satzung/satzung-der-studierendenschaft.md) | [satzung/satzung-der-studierendenschaft/](satzung/satzung-der-studierendenschaft/aufbau.md) |
| Fachschaftsrahmenordnung (FSRO) | [ordnungen/fachschaftsrahmenordnung.md](ordnungen/fachschaftsrahmenordnung.md) | [ordnungen/fachschaftsrahmenordnung/](ordnungen/fachschaftsrahmenordnung/aufbau.md) |
| Finanzordnung | [ordnungen/finanzordnung.md](ordnungen/finanzordnung.md) | [ordnungen/finanzordnung/](ordnungen/finanzordnung/aufbau.md) |
| Muster: Erklärung zur pflichtbewussten Verwaltung der Finanzen des Fachschaftsrats | [vorlagen/erklaerung-finanzverwaltung-fachschaftsrat.md](vorlagen/erklaerung-finanzverwaltung-fachschaftsrat.md) | – |

## Struktur

```
satzung/          Die Satzung der Studierendenschaft (Grundordnung)
ordnungen/        Ergänzende Ordnungen (Fachschaftsrahmenordnung, Finanzordnung)
vorlagen/         Muster- und Beispieldokumente
tools/            Skripte (Gesamttext bauen, Verweise prüfen) und tools/bots/
.github/          Automatisierung (baut den Gesamttext nach jeder Änderung)
```

## Weiterlesen

| Datei | Inhalt |
|---|---|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Änderungen vorschlagen, Schritt für Schritt (auch für GitHub-Einsteiger) |
| [FORMATIERUNG.md](FORMATIERUNG.md) | Wie Paragraphen, Listen, Verweise, Zahlen usw. geschrieben werden, mit Vorlagen zum Kopieren |
| [TECHNIK.md](TECHNIK.md) | Einzelparagraphen und Gesamttext, Nummerierung, Anker, Querverweise und ihre Prüfung |
| [tools/bots/formatierung.md](tools/bots/formatierung.md) | Anleitung für KI-Assistenten, die Texte prüfen |

## Warum Markdown statt Word?

Die Entwürfe wurden von `.docx` nach Markdown konvertiert, weil sich
Markdown-Dateien in Git vergleichen und in Pull Requests zeilengenau
kommentieren lassen; bei Word-Dateien geht das praktisch nicht.
