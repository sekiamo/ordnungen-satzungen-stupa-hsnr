# Formatierungsvorlagen

Schreibregeln und Vorlagen zum Kopieren für alle Texte in diesem Repo. Grundlage
ist das *Handbuch der Rechtsförmlichkeit* des Bundesjustizministeriums
(4. Auflage 2024); „Rn.“ verweist auf dessen Randnummern. Das Handbuch gilt
formal für Bundesrecht, ist aber ein guter Maßstab für jede Satzung und Ordnung.

Wie die Dateien technisch aufgebaut sind (Einzelparagraphen, `aufbau.md`,
Anker, Nummerierung), steht in der [README](README.md). Hier geht es um die
**Schreibweise des Textes**.

Für KI-Assistenten, die Texte prüfen oder korrigieren, gibt es eine eigene
Anleitung: [tools/bots/formatierung.md](tools/bots/formatierung.md).

## Inhalt

1. [Paragraph](#1-paragraph)
2. [Liste](#2-liste)
3. [Verweise](#3-verweise)
4. [Zahlen, Beträge, Datum, Fristen](#4-zahlen-beträge-datum-fristen)
5. [Personenbezeichnungen](#5-personenbezeichnungen)
6. [Abkürzungen und Zeichen](#6-abkürzungen-und-zeichen)
7. [Formulierungsbausteine](#7-formulierungsbausteine)
8. [Checkliste vor dem Pull Request](#8-checkliste-vor-dem-pull-request)

## 1. Paragraph

Jeder Paragraph hat eine Überschrift mit einem **Schlüsselwort**, das den
Gegenstand nennt (Rn. 378, 380). Lässt sich das nicht in wenigen Worten sagen,
gehört wahrscheinlich mehr als ein Paragraph in den Text. Aussagekräftig heißt:
auch ohne die Teil-Überschrift verständlich („Rechtsstellung des AStA“, nicht
„Rechtsstellung“).

**Mehrere Absätze** – jeder Absatz mit Nummer und Anker:

```markdown
### § 14 Schlüsselwort <a id="p14"></a>

1) <a id="p14-1"></a>Erster Absatz. Zweiter Satz des ersten Absatzes.

2) <a id="p14-2"></a>Zweiter Absatz.
```

**Nur ein Absatz** – dann keine Nummer, der Anker bleibt (Rn. 382, 383):

```markdown
### § 15 Schlüsselwort <a id="p15"></a>

<a id="p15-1"></a>Der einzige Absatz dieses Paragraphen.
```

Weitere Regeln:

- Sätze werden nicht nummeriert; im Text wird ein Satz nur über „Satz 2“ zitiert.
- Ein Satz enthält **eine** Regelungsaussage (Rn. 282).
- Keine allgemeinen Zweckbestimmungen als eigener Paragraph (Rn. 373).
- Begriffe immer gleich benennen: nicht abwechselnd „Rechnungsabschluss“,
  „Rechnungsergebnis“ und „Jahresabschluss“ für dasselbe (Rn. 257, 302).
- Teil-Überschriften in `aufbau.md`: `## Teil 3 Titel` – arabische Ziffer,
  kein Doppelpunkt (Rn. 389). Bei weniger als 20 Paragraphen sind Teile meist
  überflüssig (Rn. 387).

## 2. Liste

Eine Liste ist **ein einziger Satz** (Rn. 385). Ihre Punkte sind keine ganzen
Sätze und enthalten keine Sätze.

```markdown
2) <a id="p9-2"></a>Der Ausschuss wird tätig, wenn

   1. das Präsidium ihn beauftragt,

   2. mindestens drei Mitglieder es verlangen oder

   3. die Geschäftsordnung es vorsieht.
```

Regeln:

| Regel | Rn. |
|---|---|
| Einleitungssatz endet mit Doppelpunkt, „Folgendes“, „wie folgt“ oder mit einem Wort, an das die Punkte anschließen | 333 |
| Punkte enden mit Komma; nur der letzte mit Punkt | 295 |
| Vor dem letzten Punkt steht „und“ (alle gelten) oder „oder“ (einer genügt); bei langen Punkten „sowie“ | 292, 295 |
| Soll „oder“ ausschließend gemeint sein: „entweder … oder“; einschließend: „mindestens eine der folgenden Voraussetzungen“ | 292 |
| Nach der Liste nicht weiterschreiben („Sandwich“); stattdessen den Einleitungssatz so bauen, dass er mit dem letzten Punkt endet | 296 |
| Jeder Punkt muss zusammen mit dem Einleitungssatz allein verständlich sein – keine Pronomen („sie“, „diese“), die sich auf den vorigen Punkt beziehen | 297 |
| Untergliederung: Nummern (`1.`), darunter Buchstaben (`a)`), darunter Doppelbuchstaben (`aa)`); tiefer nicht | 382 |
| Keine Spiegelstriche (`-`) | 382 |

**Braucht ein Punkt ganze Sätze, ist es keine Liste.** Dann jeden Punkt als
eigenen Absatz schreiben und im ersten Absatz darauf verweisen:

```markdown
1) <a id="p8-1"></a>Wahlkampfkosten werden nach Maßgabe der Absätze 2 bis 4 erstattet.

2) <a id="p8-2"></a>Erstattet werden höchstens 400 Euro.

3) <a id="p8-3"></a>Es ist eine Abrechnung mit allen Belegen zu erstellen; nur belegte Kosten werden erstattet.

4) <a id="p8-4"></a>Die Abrechnung ist spätestens vierzehn Tage nach der Ergebnisverkündung einzureichen.
```

## 3. Verweise

Gliederungseinheiten werden im Text **ausgeschrieben** (Rn. 77); nur bei
Paragraphen steht das Zeichen `§`.

| Statt | Schreiben |
|---|---|
| § 5 Abs. 2 S. 1 Nr. 3 lit. a | § 5 Absatz 2 Satz 1 Nummer 3 Buchstabe a |
| §§ 8 – 12 | die §§ 8 bis 12 (kein Gedankenstrich, Rn. 78) |
| §§ 3,5 und 7 | die §§ 3, 5 und 7 |
| § 3 Abs. 1, 2 | § 3 Absatz 1 und 2 |
| Abs. (1) | Absatz 1 |

Mehrere Verweise: Wechselt die Ebene, wird die Einheit erneut genannt (Rn. 80):
„§ 1 Absatz 1 Nummer 4, § 2 Absatz 5 Satz 2 und 3, Absatz 6, § 3 Nummer 13 und § 15“.
Steht die oberste Einheit im Plural, steht das Verb im Plural, sonst im
Singular (Rn. 79): „Die §§ 3 und 5 gelten entsprechend.“ – „§ 14 Absatz 5 bis 7 gilt entsprechend.“

**Verweise als Link** (damit der Build die Nummer mitführt, siehe README):

```markdown
... nach [§ 7](p07-kassenanordnungen-vier-augen-prinzip.md) ...
... nach [§ 8 Absatz 1](p08-das-finanzreferat-der-fachschaft.md#p8-1) ...
... nach [§ 7 Finanzordnung](../ordnungen/finanzordnung.md#p7) ...
```

Weitere Regeln:

- Verweise sagen, worum es geht („… nach § 5 über die Kassenprüfung“), statt
  nackt zu zitieren (Rn. 279).
- Keine Verweisungsketten (Rn. 93).
- Ein Gesetz oder eine Verordnung wird beim ersten Vorkommen mit Namen und
  Fundstelle genannt, danach mit der eingeführten Kurzform (Rn. 55 ff., 327).

## 4. Zahlen, Beträge, Datum, Fristen

| Was | Schreibweise | Beispiel | Rn. |
|---|---|---|---|
| Zahlen im Fließtext | einheitlich Zahlwörter (Festlegung in diesem Repo) | „vierzehn Tage“, „einundzwanzig Mitglieder“ | 340 |
| Prozent | Ziffer, „Prozent“ ausgeschrieben | „10 Prozent“ | 341 |
| Geldbeträge | Ziffern, „Euro“ ausgeschrieben, ohne „,00“ | „400 Euro“, „5,50 Euro“ | 347 |
| Zahlen über 999 | geschütztes Leerzeichen, kein Punkt; nicht bei Jahreszahlen | „1 200 Euro“, aber „2026“ | 342 |
| Bruchzahlen | als Wort | „Zweidrittelmehrheit“, „die Hälfte“ | 343 |
| Zahlenverhältnis | Ziffern, Doppelpunkt | „2 : 1“ | 344 |
| Datum | „1. September 2026“ | nicht „01.09.2026“ | 345 |
| Uhrzeit | „von 6 bis 20 Uhr“ | | 346 |

Das **geschützte Leerzeichen** (Zeichen U+00A0) tippt man unter Windows mit
`Alt` + `0160` auf dem Ziffernblock, am Mac mit `Option` + `Leertaste`.

**Fristen und Stichtage** so, dass kein Zweifel über den letzten Tag bleibt
(Rn. 147–155):

| Gemeint | Schreiben |
|---|---|
| Frist läuft am Tag X noch | „bis einschließlich 31. Dezember“ oder „bis zum Ablauf des 31. Dezember“ – nicht „bis zum 31. Dezember“ |
| Beginn am Tag X | „ab dem 1. September“ |
| Frist nach Ereignis | „innerhalb von vierzehn Tagen nach …“, „spätestens sechs Wochen vor …“ |
| Alter | „mindestens 18 Jahre alt“ statt „das 18. Lebensjahr vollendet“ |

## 5. Personenbezeichnungen

Reihenfolge der Wahl (Rn. 318, 319):

1. **Geschlechtsneutral formulieren**: „Person“, „Mitglied“, „Vorsitz“,
   „Stellvertretung“, „Leitung“; Partizipien im Plural („Studierende“,
   „Referierende“, „Kassenprüfende“); „wer“, „alle“, „diejenigen“.
2. Geht das nicht: **Paarform ausschreiben** („die Finanzreferentin oder der
   Finanzreferent“). Nicht bei jeder Gelegenheit; Häufungen mit „seine oder
   ihre“ unlesbar machen den Text.
3. **Keine Sparschreibungen**: kein `*`, `_`, `:`, `/`, `(in)` – also nicht
   „Referent*in“, „Prüfer/in“, „Bewerber(innen)“. Screenreader lesen sie nicht
   vor.
4. Organe und Körperschaften haben kein Geschlecht: „der AStA“, „das
   Präsidium“, nicht mit Paarform (Rn. 321).

## 6. Abkürzungen und Zeichen

**Keine Kurzformen im Regelungstext** (Rn. 326):

| Nicht | Sondern |
|---|---|
| z. B. / z.B. | zum Beispiel |
| u. a. | unter anderem |
| d. h. | das heißt |
| bzw. | oder, und, beziehungsweise – je nachdem, was gemeint ist |
| ggf. | gegebenenfalls (oder umformulieren) |
| usw. / etc. | streichen; bei Aufzählungen „insbesondere“ voranstellen |
| Abs., S., Nr., Art. | Absatz, Satz, Nummer, Artikel |
| €, % | Euro, Prozent |

**Erlaubt** (Rn. 327): allgemein bekannte Kurzwörter ohne deutsche Entsprechung
(„E-Mail“, „PDF“) und Abkürzungen als Teil von Namen. **Eigene Kurzformen**
(„StuPa“, „AStA“, „HWVO NRW“) werden **an der ersten Stelle im Text
eingeführt**: „das Studierendenparlament (StuPa)“ – und danach durchgehend
benutzt.

**Zeichen** (Rn. 328–336):

| Zeichen | Regel |
|---|---|
| „…“ | deutsche Anführungszeichen, nicht `"…"` |
| `/` | nicht verwenden; „und“, „oder“ oder ein Komma schreiben |
| Gedankenstrich `–` | nicht im Text; nur in Überschriften |
| Bindestrich | für eingesparte Wortteile („Ausbildungs- oder Studienplatz“) und um Wortgruppen zu koppeln („Queer-Feminismus-Referat“) |
| `;` | zwischen Teilsätzen, wenn ein Komma zu schwach und ein Punkt zu hart wäre; besser ein neuer Satz, weil Teilsätze nicht zitierbar sind |
| Klammern | für Kurzformen, Fundstellen und Legaldefinitionen; keine vollständigen Sätze in Klammern |

## 7. Formulierungsbausteine

**Inkrafttreten** – immer der letzte Paragraph, Überschrift „Inkrafttreten“,
bezieht sich auf die ganze Ordnung (Rn. 158, 160, 161):

```markdown
### § 27 Inkrafttreten <a id="p27"></a>

<a id="p27-1"></a>Diese Ordnung tritt am Tag nach ihrer Veröffentlichung in den Amtlichen Bekanntmachungen der Hochschule Niederrhein in Kraft.
```

Nicht „am Tag der Veröffentlichung“ – das wirkt ab 0 Uhr zurück. Mit festem
Datum: „Diese Ordnung tritt am 1. September 2027 in Kraft.“ Nicht „Die §§ 1 bis
5 treten … in Kraft“ – der Inkrafttretens-Paragraph selbst muss mit erfasst sein.

**Außerkrafttreten** – vorletzter Paragraph, Überschrift „Außerkrafttreten“,
die alte Regelung mit Titel und Datum nennen (Rn. 381):

```markdown
<a id="p26-1"></a>Mit dem Inkrafttreten dieser Ordnung tritt die Ordnung … vom [Datum] außer Kraft.
```

**Verhältnis zu anderen Regeln** (Rn. 278):

| Gemeint | Schreiben |
|---|---|
| beide Regeln gelten nebeneinander | „§ 5 bleibt unberührt.“ |
| die andere Regel geht vor | „soweit in § 5 nichts anderes geregelt ist“ / „es sei denn, es liegt ein Fall des § 5 vor“ |
| nicht verwenden | „unbeschadet“, „vorbehaltlich“ |

**Bedingungen** (Rn. 308): „wenn“, „falls“, „sofern“ für ein Entweder-oder;
„soweit“ nur, wenn es um ein **Maß** geht („soweit die Mittel reichen“).

**Verbindlichkeit** (Rn. 309): „muss“, „ist zu“, „darf nicht“ für Pflichten und
Verbote; „kann“ für Ermessen; „soll“ nur für Regelfälle mit möglichen
Ausnahmen – nicht als höfliches „muss“.

**Verneinung** (Rn. 298, 299): höchstens eine Verneinung pro Satz. Zwei
Aufzählungsglieder verneinen mit „weder … noch“.

**Definition** (Rn. 273): „Fachschaftsvollversammlung (FSVV)“ beim ersten
Auftreten oder ein Paragraph „Begriffsbestimmungen“ am Anfang; keine Regeln in
der Definition.

## 8. Checkliste vor dem Pull Request

- [ ] Keine Kurzformen (`z. B.`, `Abs.`, `etc.`, `bzw.`, `%`, `€`) im Text
- [ ] Keine Sparschreibungen (`*`, `_`, `/in`) und keine Schrägstriche
- [ ] Zahlen, Beträge und Datum nach Abschnitt 4
- [ ] Listen: ein Satz, keine ganzen Sätze in Punkten, „und“/„oder“ vor dem letzten Punkt
- [ ] Absatznummer nur, wenn der Paragraph mehrere Absätze hat
- [ ] Eigene Kurzformen an der ersten Stelle eingeführt
- [ ] Verweise ausgeschrieben; nach Einfügen oder Löschen von Absätzen alle
      Verweise auf **Absätze** und **Fließtext-Verweise** geprüft (siehe README)
- [ ] Gleiche Dinge gleich benannt
- [ ] Schlüsselwort in der Paragraphenüberschrift, ohne Teil-Titel verständlich
- [ ] Rechtschreibung geprüft; Schlusspunkt am Absatzende
