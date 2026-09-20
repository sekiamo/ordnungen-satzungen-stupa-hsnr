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

## Dokumente

Alle Texte sind **Entwürfe**. Zum **Lesen** führt der Link in der Mitte zum kompletten
Text; zum **Bearbeiten** gibt es jeden Paragraphen als eigene Datei (rechte Spalte, siehe
auch [Einzelparagraphen und Gesamttext](#einzelparagraphen-und-gesamttext)).

| Dokument | Gesamttext lesen | Paragraphen bearbeiten |
|---|---|---|
| Satzung der Studierendenschaft | [satzung/satzung-der-studierendenschaft.md](satzung/satzung-der-studierendenschaft.md) | [satzung/satzung-der-studierendenschaft/](satzung/satzung-der-studierendenschaft/aufbau.md) |
| Fachschaftsrahmenordnung (FSRO) | [ordnungen/fachschaftsrahmenordnung.md](ordnungen/fachschaftsrahmenordnung.md) | [ordnungen/fachschaftsrahmenordnung/](ordnungen/fachschaftsrahmenordnung/aufbau.md) |
| Finanzordnung | [ordnungen/finanzordnung.md](ordnungen/finanzordnung.md) | [ordnungen/finanzordnung/](ordnungen/finanzordnung/aufbau.md) |
| Muster: Erklärung zur pflichtbewussten Verwaltung der Finanzen des Fachschaftsrats | [vorlagen/erklaerung-finanzverwaltung-fachschaftsrat.md](vorlagen/erklaerung-finanzverwaltung-fachschaftsrat.md) | – |

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

### Nummerierung (automatisch)

Die sichtbare §-Nummer ergibt sich **allein aus der Reihenfolge in
`aufbau.md`**. Das Skript schreibt sie bei jedem Bauen in

- die Überschriften der Paragraphen-Dateien (`### § 8 ...`),
- die Zeilen in `aufbau.md`,
- die Linktexte von Verweisen wie `[§ 14](p14-redeliste.md)` – auch dokumentübergreifend.

Nach dem Einfügen, Verschieben oder Löschen eines Paragraphen rücken alle
folgenden Nummern also von selbst nach. **Nicht automatisch angepasst** werden
Verweise auf **Absätze** („Abs. 2“) und Verweise, die nur als **Text im
Fließtext** stehen („gemäß § 5“). Das Skript listet diese im Build-Protokoll
auf, sobald umnummeriert wurde; sie müssen von Hand geprüft werden (Suche nach
`§ ` im Repo). Die Anker-IDs (`p14`) ändern sich nie.

### Neuen Paragraphen einfügen (einfachster Weg: Button)

1. Im Gesamttext beim Paragraphen, **nach dem** der neue stehen soll, auf
   „➕ Neuen Paragraphen danach einfügen“ klicken. GitHub öffnet einen Editor
   mit einer Vorlage.
2. In der Vorlage **nur `Titel` und den Text ersetzen** und ggf. weitere
   Absätze ergänzen (`2) ...`). `N` in der Überschrift, `pN` in den Anker-IDs,
   die erste Zeile `<!-- einfuegen-nach: ... -->` und den Dateinamen `neu.md`
   **nicht ändern** – das erledigt das Skript.
3. Änderung speichern („Commit changes“ bzw. „Propose changes“ → Pull
   Request). Sobald sie in `main` ist, macht die GitHub Action daraus einen
   fertigen Paragraphen: Sie vergibt Nummer, Anker-ID (z.B. `p7a` für einen
   Paragraphen hinter § 7) und Dateinamen, trägt ihn in `aufbau.md` ein,
   nummeriert alle folgenden Paragraphen neu und baut den Gesamttext.
4. Verweise auf **Absätze** und Verweise im **Fließtext** prüfen (siehe
   „Nummerierung“).

Schlägt der Build fehl (z.B. weil `Titel` noch in der Überschrift steht),
erscheint unter „Actions“ ein rotes Kreuz mit einer Fehlermeldung.

### Paragraph von Hand einfügen, verschieben oder entfernen

1. **Einfügen:** neue Datei im Dokument-Verzeichnis anlegen (Muster: eine
   bestehende Datei kopieren) und in `aufbau.md` als Zeile
   `- [§ N Titel](dateiname.md)` an der richtigen Stelle eintragen; die
   **Anker-ID** (`<a id="p7a"></a>`) muss im Dokument eindeutig sein. Alternativ
   die Datei mit der Vorlage aus dem Button anlegen; dann entfällt der
   Eintrag in `aufbau.md`. Eine Datei, die weder in `aufbau.md` steht noch die
   `einfuegen-nach`-Markierung trägt, bricht den Build ab.
2. **Entfernen:** Datei löschen und die Zeile aus `aufbau.md` streichen.
3. **Verschieben:** nur die Zeile in `aufbau.md` an eine andere Stelle setzen.

Die Nummern der Paragraphen passen sich in allen drei Fällen automatisch an.

## Verweise zwischen Paragraphen

In den Einzeldateien verweist man auf einen anderen Paragraphen desselben
Dokuments **über den Dateinamen**, damit der Link auch in der Einzelansicht
funktioniert:

```
... Ordnungsmaßnahmen ([§ 14](p14-redeliste.md)) ...
... Erklärung gemäß [§ 8 Absatz (1)](p08-das-finanzreferat-der-fachschaft.md#p8-1) ...
```

Beim Bauen des Gesamttexts werden daraus automatisch Sprungmarken
(`#p14`, `#p8-1`), und die Paragraphen-Nummer im Linktext wird bei
Umnummerierungen automatisch mitgeführt. Verweise in ein **anderes** Dokument
zeigen auf dessen Gesamttext, z.B.
`[§ 7 Finanzordnung](../ordnungen/finanzordnung.md#p7)`; auch hier wird die
Nummer im Linktext aktualisiert.

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

**Renummerierung:** Markdown-Listen nummerieren beim Rendern automatisch
durch (Absätze `1)`, `2)`, ...), und die §-Nummern setzt das Build-Skript aus
der Reihenfolge in `aufbau.md` (siehe „Nummerierung (automatisch)“ oben).
Fügt jemand einen Absatz oder Paragraphen ein oder löscht einen, verschieben
sich folgende Nummern automatisch; Linktexte wie `[§ 14](...)` werden mit
angepasst. **Nicht** angepasst werden Verweise auf Absätze („§ 5 Abs. 2“) und
Verweise, die nur als Text im Fließtext stehen. **Nach jedem Einfügen/Löschen
deshalb gezielt danach suchen** (Volltextsuche nach `§ N` bzw. `Abs.` im
ganzen Repo) und von Hand korrigieren.

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

Beim Einfügen eines neuen § über den Button vergibt das Skript die
Anker-ID selbst (z.B. `p7a` für einen Paragraphen hinter § 7). Wer einen § oder
Absatz von Hand anlegt, vergibt die ID nach dem Schema `p<§-Nummer>` bzw.
`p<§-Nummer>-<Absatz-Nummer>` selbst; sie muss im Dokument eindeutig sein und
wird danach nie mehr angepasst, auch wenn sich die sichtbare Nummer später
ändert. Die Absatz-IDs eines Paragraphen tragen dessen ID als Präfix: bei
`p10a` also `p10a-1`, `p10a-2`, ... (nicht `p11-1`). Die Prüfung (nächster
Abschnitt) meldet Abweichungen.

## Querverweise prüfen

Sobald jemand einen Paragraphen oder Absatz ändert, auf den anderswo verwiesen
wird, muss sich der Verweis nicht mehr auf dasselbe beziehen. Damit das nicht
unbemerkt bleibt, prüft `tools/check_verweise.py` bei jedem Push und Pull
Request (Workflow `verweise-pruefen.yml`). Verweise sind alle Links auf einen
Paragraphen oder Absatz, in derselben oder einer anderen Satzung/Ordnung. Die
Liste aller Verweise steht in [`VERWEISE.md`](VERWEISE.md) und wird
automatisch erzeugt.

| Stufe | Auslöser | Wirkung |
|---|---|---|
| **Fehler** | Verweis zeigt auf einen Anker, den es nicht (mehr) gibt; ein Anker, auf den verwiesen wurde, ist verschwunden oder umbenannt; dieselbe Anker-ID kommt zweimal im Dokument vor | Prüfung schlägt fehl |
| **Alarm** | Der Text eines Paragraphen/Absatzes, auf den verwiesen wird, wurde geändert; die Meldung nennt alle, die darauf verweisen | Prüfung schlägt fehl, bis die Verweise geprüft sind |
| **Hinweis** | Absatz-ID passt nicht zum Paragraphen; ein Verweis im Fließtext („§ 5 Abs. 2“) meint eine Nummer, die sich verschoben hat; ein nicht verlinkter Anker ist verschwunden | nur Information |

**Ein Alarm ist kein Fehler im Text**, sondern die Aufforderung: Öffne die
genannten Stellen und prüfe, ob der Verweis noch passt. Danach im Pull Request
das Label **`verweise-geprueft`** setzen (einmalig unter Issues → Labels
anlegen); die Prüfung läuft dann durch. Wer direkt auf `main` schreibt, sieht
den Alarm als rote Prüfung beim Commit und korrigiert bei Bedarf nach.

Was zählt als Änderung? Der Vergleich läuft gegen den Stand vor dem Push bzw.
gegen die Basis des Pull Requests. Ein Verweis auf einen **Paragraphen** löst
bei jeder Änderung in einem seiner Absätze Alarm aus; ein Verweis auf einen
**Absatz** nur bei Änderung dieses Absatzes. Umnummerierungen (`§ 5` wird
`§ 6`) und Änderungen an Linkzielen zählen **nicht** als Textänderung.

Damit die Prüfung greift, Verweise **als Link** schreiben
(`[§ 10 Abs. 4](../satzung/satzung-der-studierendenschaft.md#p10-4)`), nicht
nur als Text. Verweise im Fließtext erkennt das Skript nur als Hinweis. Ein
Verweis auf ein anderes Dokument braucht dessen Anker-ID nach `#`.

Lokal prüfen (vor dem Hochladen, prüft auch nicht versionierte Dateien wie
lokale Geschäftsordnungen, die auf GitHub fehlen):

```
python tools/check_verweise.py                 # gegen origin/main
python tools/check_verweise.py --base HEAD~1   # gegen einen anderen Stand
python tools/check_verweise.py --base none     # nur Ist-Zustand
```

Exit-Code 0 = in Ordnung, 1 = Fehler, 3 = nur Alarm.
