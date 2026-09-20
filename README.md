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
satzung/      Die Satzung der Studierendenschaft (Grundordnung)
ordnungen/    Ergänzende Ordnungen (Fachschaftsrahmenordnung, Finanzordnung)
vorlagen/     Muster-/Beispieldokumente (z.B. Erklärungen, Formulare)
tools/        Skript, das den Gesamttext aus den Einzelparagraphen erzeugt
.github/      Automatisierung (baut den Gesamttext nach jeder Änderung)
```

## Einzelparagraphen und Gesamttext

Jede Satzung und jede Ordnung gibt es in **zwei Formen**:

| Form | Beispiel | Wofür |
|---|---|---|
| **Gesamttext** (zum Lesen) | [`ordnungen/finanzordnung.md`](ordnungen/finanzordnung.md) | Das ganze Dokument am Stück in Klartext lesen, durchsuchen, verlinken. Unter jeder §-Überschrift stehen zwei Links: „✏️ Diesen Paragraphen bearbeiten“ (öffnet den Editor für genau diesen Paragraphen) und „➕ Neuen Paragraphen danach einfügen“. **Wird automatisch erzeugt – nicht direkt bearbeiten.** |
| **Einzelparagraphen** (zum Bearbeiten) | [`ordnungen/finanzordnung/`](ordnungen/finanzordnung/aufbau.md) | Jeder Paragraph ist eine eigene Datei (z.B. `p07-kassenanordnungen-vier-augen-prinzip.md`). Änderungen und Pull-Request-Kommentare beziehen sich so immer auf genau einen Paragraphen. |

In jedem Verzeichnis mit Einzelparagraphen liegt eine Datei `aufbau.md`. Sie ist
zugleich Inhaltsverzeichnis (die Links führen zu den Paragraphen) und legt
fest, **in welcher Reihenfolge** die Paragraphen im Gesamttext erscheinen und
welche **Teil-Überschriften** (`## Teil 3 ...`) dazwischen stehen.

### Gesamttext neu bauen

Nach jeder Änderung an `main` baut die GitHub Action
[`.github/workflows/gesamttext.yml`](.github/workflows/gesamttext.yml) den
Gesamttext automatisch neu und committet ihn (dauert etwa eine Minute; unter
„Actions“ sichtbar). Wer lokal arbeitet, kann ihn selbst erzeugen (benötigt
Python 3, sonst nichts):

```
python tools/build_gesamttext.py           # Gesamttexte neu erzeugen
python tools/build_gesamttext.py --check   # nur prüfen, ob sie aktuell sind
```

### Dateinamen

`p<Nr>-<kurzer-titel>.md`, z.B. `p14-redeliste.md`. Die Nummer im Dateinamen
ist wie die Anker-ID (siehe unten) die Nummer **zum Zeitpunkt der Einführung**
und wird bei späteren Umnummerierungen **nicht** angepasst; maßgeblich für die
Reihenfolge ist allein `aufbau.md`. Texte vor dem ersten Paragraphen
(Eingangsformel, Präambel, Einleitung) heißen `00-....md`.

### Neuen Paragraphen einfügen (einfachster Weg: Button)

1. Im Gesamttext beim Paragraphen, **nach dem** der neue stehen soll, auf
   „➕ Neuen Paragraphen danach einfügen“ klicken. GitHub öffnet einen Editor
   mit einer Vorlage.
2. **Dateiname** anpassen: `p<Nr>-<kurztitel>.md` (er muss im Ordner eindeutig
   sein).
3. In der Vorlage `N` und `Titel` ersetzen, z.B.
   `### § 8 Rücklagen  <a id="p8"></a>` und `<a id="p8-1"></a>` beim ersten
   Absatz. Die **Anker-ID muss im Dokument eindeutig sein**; wer zwischen § 7
   und § 8 einfügt, nimmt z.B. `p7a` statt einer schon vergebenen Nummer.
   Die erste Zeile `<!-- einfuegen-nach: ... -->` **nicht ändern oder
   löschen** – sie sagt dem Skript, wohin der Paragraph gehört.
4. Änderung speichern („Commit changes“ bzw. „Propose changes“ → Pull
   Request). Sobald sie in `main` ist, trägt die GitHub Action den Paragraphen
   automatisch in `aufbau.md` ein, entfernt die Markierung und baut den
   Gesamttext neu.
5. Sichtbare §-Nummern der folgenden Paragraphen (`### § N ...`) und Verweise
   darauf von Hand anpassen (siehe Abschnitt zum Renummerierungs-Risiko).

Schlägt der Build fehl (z.B. weil `N`/`Titel` noch in der Überschrift stehen
oder die Anker-ID doppelt vergeben ist), erscheint unter „Actions“ ein rotes
Kreuz mit einer Fehlermeldung.

### Paragraph von Hand einfügen, verschieben oder entfernen

1. **Einfügen:** neue Datei im Dokument-Verzeichnis anlegen und in
   `aufbau.md` als Zeile `- [§ N Titel](dateiname.md)` an der richtigen Stelle
   eintragen. Eine Datei, die weder in `aufbau.md` steht noch die
   `einfuegen-nach`-Markierung trägt, bricht den Build ab.
2. **Entfernen:** Datei löschen und die Zeile aus `aufbau.md` streichen.
3. **Verschieben:** nur die Zeile in `aufbau.md` an eine andere Stelle setzen.

## Verweise zwischen Paragraphen

In den Einzeldateien verweist man auf einen anderen Paragraphen desselben
Dokuments **über den Dateinamen**, damit der Link auch in der Einzelansicht
funktioniert:

```
... Ordnungsmaßnahmen ([§ 14](p14-redeliste.md)) ...
... Erklärung gemäß [§ 8 Absatz (1)](p08-das-finanzreferat-der-fachschaft.md#p8-1) ...
```

Beim Bauen des Gesamttexts werden daraus automatisch Sprungmarken
(`#p14`, `#p8-1`). Verweise in ein **anderes** Dokument zeigen auf dessen
Gesamttext, z.B. `[§ 7 Finanzordnung](../ordnungen/finanzordnung.md#p7)`.

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

Im Gesamttext springt ein Link wie `[§ 14](#p14)` auf diese ID. In den
Einzeldateien schreibt man stattdessen den Dateinamen (siehe Abschnitt
„Verweise zwischen Paragraphen“ oben); der Build macht daraus die
Sprungmarke.

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
