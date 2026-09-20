# Mitmachen – Anleitung für GitHub-Einsteiger

Du musst kein:e Programmierer:in sein, um hier mitzuarbeiten. Für die meisten
Änderungen reicht der Browser. Diese Anleitung führt dich durch die zwei
gängigen Wege: **kleine Änderung direkt im Browser** und **größere Änderung
lokal am eigenen Rechner**.

## Kurz erklärt: Wie GitHub hier benutzt wird

- **Repository ("Repo")**: dieser gesamte Projektordner, inklusive alter
Versionen (Verlauf).
- **Branch**: eine eigene "Arbeitskopie" der Dateien, in der du Änderungen
machst, ohne die Hauptversion (`main`) direkt zu verändern.
- **Pull Request (PR)**: dein Änderungsvorschlag. Andere können ihn lesen,
kommentieren und erst nach Zustimmung wird er in `main` übernommen.
- **Issue**: ein Diskussions- oder Aufgabenpunkt, z.B. "§ 5 der Finanzordnung
ist unklar formuliert" – auch ohne fertigen Textvorschlag nützlich.

Nichts geht "kaputt", wenn du etwas falsch machst: Jede Änderung kann vor der
Übernahme noch geprüft und korrigiert werden.

## Weg 1: Kleine Textänderung direkt im Browser (empfohlen für den Einstieg)

1. Öffne die **Paragraphen-Datei**, die du ändern willst – z.B.
`ordnungen/finanzordnung/p09-ruecklagen.md`. Jeder Paragraph ist eine eigene
Datei; die Übersicht steht in der `aufbau.md` des jeweiligen Ordners. Am
bequemsten geht es über den Link „✏️ Diesen Paragraphen bearbeiten“ unter der
Überschrift im Gesamttext. (Die Datei direkt in `ordnungen/` bzw. `satzung/`,
z.B. `ordnungen/finanzordnung.md`, ist der **automatisch erzeugte
Gesamttext** – dort bitte nichts ändern, die Änderung ginge beim nächsten
Bauen verloren.)
2. Klicke oben rechts auf das Stift-Symbol ("Edit this file" / "Diese Datei
bearbeiten"). GitHub erstellt dafür automatisch einen eigenen Branch für
dich (du kannst gar nicht versehentlich `main` überschreiben).
3. Ändere den Text direkt im Editor-Fenster.
- Ändere möglichst nur das, was inhaltlich gemeint ist – keine
Rechtschreib-"Aufräumaktionen" quer durchs Dokument in derselben
Änderung, das macht die Prüfung für andere unnötig schwer.
- Beachte die Nummerierungs-Konvention aus der [README](README.md):
Absätze sind als `1)`, `2)`, ... geschrieben (echte Markdown-Liste).
Fügst du einen Absatz ein oder löschst einen, verschieben sich alle
folgenden Nummern automatisch – durchsuche danach das Repo nach
Verweisen auf die alte Nummer (z.B. "§ 5 Abs. 2") und korrigiere sie.
- Jeder § und jeder Absatz hat eine feste Anker-ID (`<a id="p5-2"></a>`).
Beim Einfügen eines neuen § oder Absatzes: neue ID nach demselben
Schema ergänzen. Bestehende IDs nicht ändern, auch wenn sich die
sichtbare Nummer verschiebt.
4. Scrolle runter zu "Propose changes" / "Änderungen vorschlagen". Trag eine
kurze Beschreibung ein, z.B. "§ 8 FSRO: Frist von 7 auf 14 Tage geändert".
5. Klicke auf "Propose changes" – GitHub öffnet danach automatisch die Seite
für den Pull Request. Klicke dort auf "Create pull request".
6. Den Gesamttext musst du nicht von Hand ändern: Er wird nach der
Übernahme in `main` automatisch neu gebaut.
7. Fertig. Andere sehen jetzt deinen Vorschlag, können kommentieren, und er
wird nach Abstimmung/Freigabe übernommen.

## Weg 2: Größere Änderung (z.B. mehrere Paragraphen neu strukturieren)

Für größere Eingriffe lohnt sich ein eigener Branch, den du in Ruhe
bearbeitest, bevor du ihn vorschlägst.

1. Oben auf der Repo-Seite auf den Branch-Umschalter (zeigt meist "main") und
einen neuen Branch-Namen eingeben, z.B. `aenderung-finanzordnung-ruecklagen`.
2. In diesem neuen Branch kannst du wie in Weg 1 mehrere Dateien nacheinander
bearbeiten ("Edit this file"), alle Änderungen landen im selben Branch.
Einen **neuen Paragraphen** legst du am einfachsten über den Link
„➕ Neuen Paragraphen danach einfügen“ im Gesamttext an (Details:
Abschnitt „Neuen Paragraphen einfügen“ in der [README](README.md)).
3. Wenn du fertig bist: oben auf "Contribute" → "Open pull request" klicken,
kurze Beschreibung schreiben, "Create pull request".

## Am eigenen Rechner arbeiten (optional, für Vielschreiber:innen)

Falls dir das Browser-Editieren zu umständlich wird:

1. [GitHub Desktop](https://desktop.github.com/) installieren (grafische
Oberfläche, kein Kommandozeilen-Wissen nötig).
2. Repo über "File → Clone repository" herunterladen.
3. Dateien mit einem normalen Text-Editor bearbeiten (z.B. VS Code, Notepad++,
sogar Editor/Notepad reicht für Markdown).
Um das Ergebnis als Ganzes zu sehen, kannst du den Gesamttext lokal neu
erzeugen: `python tools/build_gesamttext.py` (benötigt Python 3).
4. In GitHub Desktop die Änderungen sehen, einen Branch erstellen, committen
und über "Push" hochladen, dann im Browser den Pull Request eröffnen
(GitHub Desktop bietet dafür einen direkten Knopf an).

## Wie sieht eine gute Änderung aus?

- **Ein Thema pro Pull Request.** Lieber drei kleine PRs als einen großen, in
dem sich niemand mehr zurechtfindet.
- **Begründung in der PR-Beschreibung.** Warum die Änderung? Verweis auf
Diskussion/Beschluss, falls vorhanden.
- **Verweise auf Absatz-Nummern prüfen.** Wenn du einen Absatz einfügst oder
löscht, müssen alle Nummern danach von Hand angepasst werden – und alle
Stellen im Text, die auf die alte Nummer verweisen (z.B. "gemäß Abs. 3").
- Bei reinen Verständnisfragen oder Formulierungsideen ohne fertigen Text:
einfach ein **Issue** eröffnen statt gleich einen Pull Request.

## Hilfe, ich weiß nicht weiter

Ein "falscher" Klick auf GitHub lässt sich fast immer rückgängig machen oder
einfach ignorieren (z.B. einen nicht mehr gewollten Pull Request schließen,
ohne ihn zu übernehmen). Im Zweifel: Frage im zuständigen Gremium
(StuPa/AStA) oder bei der Person, die dieses Repo eingerichtet hat.
