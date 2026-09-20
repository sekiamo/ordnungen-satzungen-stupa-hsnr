# Anleitung für Bots: Formatierung prüfen

Für KI-Assistenten (und Menschen), die Texte in diesem Repo – Satzung,
Fachschaftsrahmenordnung, Finanzordnung – auf **formale Richtigkeit** prüfen
oder korrigieren sollen. Sie beschreibt, *wie* gearbeitet wird. Was diesmal zu
tun ist, steht im Auftrag.

## Quelle der Regeln

[`FORMATIERUNG.md`](../../FORMATIERUNG.md) enthält die Schreibregeln und
Vorlagen mit den Randnummern („Rn.“) des *Handbuchs der Rechtsförmlichkeit*
(Bundesministerium der Justiz, 4. Auflage 2024). **Dort lesen, hier nicht
duplizieren.** Ändert sich eine Regel, dann in der `FORMATIERUNG.md`.

Das Handbuch selbst (rund 400 Seiten, PDF beim Bundesjustizministerium) nur bei
Zweifeln zur Randnummer nachschlagen. Für die Textextraktion:

```
pdftotext -enc UTF-8 -layout handbuch-der-rechtsfoermlichkeit.pdf handbuch.txt 2>/dev/null
```

`-enc UTF-8` ist nötig (sonst kaputte Umlaute), `2>/dev/null` auch (das PDF
erzeugt tausende Warnzeilen). Die Textdatei gehört nicht ins Repo. Das
Inhaltsverzeichnis mit den Randnummern-Überschriften steht in den ersten
Prozent des Textes.

## Formal oder inhaltlich?

Die wichtigste Unterscheidung. Ein Bot ändert nur **formal**; alles, was die
Regelung verändern könnte, wird **gemeldet, nicht geändert**.

| Formal – darf geändert werden | Inhaltlich – nur melden |
|---|---|
| „Abs.“, „z. B.“, „etc.“, „%“, „€“ ausschreiben | Wortlaut mit anderer Bedeutung (etwa „und“ oder „oder“ für einen Schrägstrich, wenn unklar) |
| Sparschreibungen und Schrägstriche auflösen | Beträge, Fristen, Mehrheiten, Anzahl von Mitgliedern |
| Zahlwörter durch Ziffern ersetzen (Festlegung des Repos) | Paragraphen neu ordnen, zusammenlegen, aufteilen |
| Listen: Konjunktion, keine ganzen Sätze (als Absätze) | Fehlende oder unvollständige Sätze ergänzen (nicht raten) |
| Absatznummer bei nur einem Absatz entfernen | Außerkrafttreten, Fundstellen, Datum der alten Satzung (nicht erfinden) |
| Rechtschreibung, Interpunktion, Anführungszeichen | Begriffe vereinheitlichen, wenn sie Unterschiedliches meinen könnten |
| Kurzformen an der ersten Stelle einführen | Wahl zwischen „soll“, „muss“, „kann“ |

Bei zwei denkbaren Lesarten (etwa „Tagesordnung/Abstimmungsfragen“) die
schwächere Änderung wählen **und** im Bericht als Rückfrage aufführen.

## Vorgehen

1. **Eigener Worktree ab `origin/main`.** Im Repo arbeiten oft mehrere Personen
   oder Sessions gleichzeitig. Deshalb
   `git worktree add -b <branch> <verzeichnis> origin/main` und nur dort
   editieren; den Hauptordner und fremde Branches nicht anfassen.
2. **Alles lesen.** Der Quelltext ist klein (rund 40 KB, je Paragraph eine
   Datei). Vollständig lesen, nicht nur suchen – Urteilsfälle (Sätze in Listen,
   fehlende Wörter) findet ein Suchmuster nicht.
3. **Muster suchen** (Tabelle unten), dann jeden Treffer einzeln beurteilen.
4. **Änderungen als Skript mit Zähl-Prüfung:** jede Ersetzung muss genau
   einmal treffen, sonst Abbruch. Danach `git diff` vollständig lesen – so
   fällt auf, wenn eine Ersetzung Text verdoppelt hat.
5. **Bauen:** `python tools/build_gesamttext.py` muss ohne Fehler laufen.
   Doppelte Anker im Gesamttext ausschließen:
   `grep -o 'a id="[^"]*"' <gesamttext>.md | sort | uniq -d` darf nichts liefern.
6. **Gesamttexte nicht committen** (`satzung/*.md`, `ordnungen/*.md`,
   `VERWEISE.md`): die GitHub Action baut sie nach dem Merge. Mit
   `git checkout -- <datei>` zurücksetzen.
7. **Commit auf dem Branch, dann vorlegen.** `git push` und Pull Request nur mit
   ausdrücklichem OK der zuständigen Person. Der Bericht enthält die Liste der
   inhaltlichen Rückfragen.

## Suchmuster

Auf die Paragraphendateien anwenden, nicht auf `aufbau.md` und nicht auf die
Gesamttexte. Vorher Anker (`<a id="…"></a>`) und Link-Ziele `](…)` aus der
Zeile entfernen.

| Befund | Muster (Regex) |
|---|---|
| Kurzformen | `z\.\s?B\.`, `\betc\b`, `bzw\.`, `ggf\.`, `u\.\s?a\.`, `d\.\s?h\.`, `\bAbs\.`, `\bNr\.`, `\bArt\.` |
| Sparschreibung | `[*]`, `_in\b`, `/in\b`, `\(in\)` |
| Zeichen und Einheiten | `€`, `[0-9]\s?%`, `"` (gerade Anführungszeichen) |
| Schrägstrich | `[A-Za-zäöüÄÖÜ)]/[A-Za-zäöüÄÖÜ(]` |
| Datum und Zahlen | `\b\d{1,2}\.\d{1,2}\.`, `\b\d{1,3}\.\d{3}\b` (Tausenderpunkt) |
| Formeln | `unbeschadet`, `vorbehaltlich` |
| Formales | doppelte Leerzeichen, Leerzeichen am Zeilenende, `Absatz \(\d` |

**Bekannte Fehlalarme:** `usw` trifft „Au**sw**irkungen“ – als Wort mit
`\busw\b` suchen. `Abs\.` trifft „Abs.“ auch in Link-Texten; Links vorher
entfernen.

Nicht per Muster findbar, nur durch Lesen: ganze Sätze in Listenpunkten,
Fortsetzung nach einer Liste, fehlendes „und“ oder „oder“ vor dem letzten
Punkt, Absatznummer bei nur einem Absatz, Kurzform vor ihrer Einführung,
uneinheitliche Begriffe, unvollständige Sätze, doppelte Anker.

## Fallstricke aus der Praxis

- **Backslashes und `\uXXXX`** werden von manchen Werkzeugen beim Übergeben
  verändert (Heredoc, Schreib-Werkzeuge): `\n` im Quelltext wurde zum
  Zeilenumbruch, ein `\u`-Escape für das Paragraphenzeichen zum Zeichen selbst. Skripte mit Regex deshalb mit
  Zeichenklassen (`[*]`, `[.]`) statt Escapes schreiben, Umlaute über
  Konstanten bilden und die Datei nach dem Schreiben ansehen.
- **Zeilenenden:** Der Index hat LF, der Arbeitsordner unter Windows CRLF
  (`core.autocrlf=true`). Beim Lesen `\r\n` normalisieren, beim Schreiben CRLF
  zurückgeben, sonst treffen mehrzeilige Suchtexte nicht.
- **Geschütztes Leerzeichen** (U+00A0) bei Tausendern ist gewollt und im Diff
  unsichtbar. Nicht „bereinigen“.
- **Anker sind stabil.** Nie umbenennen, außer sie kollidieren (dann melden).
  Beim Entfernen der Absatznummer bleibt der Anker im Text stehen.
- **Verweise auf Absätze und im Fließtext** („§ 5 Absatz 2“) führt der Build
  nicht mit. Nach jeder Umnummerierung im Repo danach suchen.
- **Nichts erfinden:** Fundstellen, Daten, fehlende Wörter, die Bezeichnung der
  bisherigen Satzung – melden.

## Berichtsform

1. Was geändert wurde, **nach Regel** (Randnummer) gruppiert, mit Beispiel.
2. Was **nicht** geändert wurde und warum – als Checkliste (`- [ ]`) von
   Entscheidungen für die Maintainer.
3. Was nicht der Auftrag war, aber auffiel (zum Beispiel kaputte Anker), am Ende.
4. Ergebnis von Build und Ankerprüfung, ehrlich auch bei Fehlern.

Als Beispiel dient der Pull Request „Formale Angleichung an das Handbuch der
Rechtsförmlichkeit“ (#5).
