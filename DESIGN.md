# Design-Kontrakt – Ritter Immobilien e.K., Immobilienmakler, Stolberg (29.9.2026)

Design-Read: Redesign einer Jimdo-Seite (Copyright 2017, Cookie-Wand, Aachener Dom als Titelbild, Emoji-Überschriften) eines familiengeführten Maklerbüros: Rudolf Ritter (seit 1989) und Tochter Maike Steyns (Immobilienfachwirtin IHK). Zwei Zielgruppen: **Eigentümer**, die verkaufen oder vermieten wollen (Hauptgeschäft, meist ältere Hausbesitzer in Stolberg, Eschweiler, Aachen-Süd, Roetgen), und **Suchende**, die ein Haus kaufen oder mieten. Tonlage: persönlich, ruhig, verlässlich – „wo Träume ein Zuhause finden“ ist der eigene Leitsatz.

1. **Leitidee: Bruchstein.** Stolberg ist Bruchsteinland – viele der rund 60 verkauften Referenzobjekte sind Bruchsteinhäuser in Zweifall, Mausbach, Vicht, Venwegen. Die Seite hat die Wärme dieses Steins: Sand- und Steintöne, eigene Fotos der verkauften Häuser, eine Serifenschrift wie auf einem Hausschild. Kein Glas, kein Tech.
2. **Signature-Element: „Käufer warten schon“.** Ritters stärkstes Argument sind vorgemerkte Kaufinteressenten (echte Suchaufträge auf der alten Seite, Stand 12.09.2025). Eigentümer wählen Haustyp, Ort und Preisrahmen – die passenden echten Suchaufträge leuchten auf („Für sympathische Familie … EFH Raum Stolberg/Eschweiler bis ca. 350.000 €“), daneben die Zahl der Treffer und der Weg zur Bewertung. Pflegbar in `data/suchauftraege.js`. Gab es in keinem Vorprojekt.
3. **Angebote live:** Die Angebote kommen über das immowelt-Homepagemodul des Maklers (bisher schon auf der alten Seite). Die neue Seite lädt Liste und Exposés im Browser direkt dort und zeigt sie im eigenen Design – auf ritterimmobilien.de immer aktuell. Außerhalb der Domain (Vorschau) greift automatisch ein gespeicherter Stand. Kein Scroll-Wechsel, keine festen Fotos einzelner Angebote (Lehre Euregio Motorcars), Fotos im Originalformat 4:3.
4. **Typo-Charakter:** *Fraunces Variable* (lokal, mit Kursive) für Titel – eine weiche, warme Serif, passend zum kursiven Serifen-Schriftzug im Logo; *Instrument Sans Variable* für Text und Daten (Preise, Flächen tabellarisch). Nicht Inter, Manrope, Archivo, Public Sans, Plex, Barlow, Figtree, Saira.
5. **Farbwelt:** Weiß / Kalk `#f7f4ee` / `#1d1d1f`. Marke: **Ritter-Blau `#0a3890`** aus dem Logo (Buttons, Links, dunkle Sektionen in Tiefblau `#0b2256`), **Bruchstein-Sand `#c8b48e`** für Linien und Akzente, Stein-Grau `#6f6a61` für Nebentext. Radius **16 px** – freundlich, nicht verspielt. Dunkle Sektionen mit 28-px-Ecken über die vorige gelegt.
6. **Navigation: klare Kopfzeile nach Zielgruppe.** Logo links; „Angebote“ (mit Live-Zahl), „Verkaufen & Vermieten ▾“ (Verkauf, Vermietung, Bewertung, Käufer warten schon, Finanzierung, Referenzen, Kundenstimmen), „Hausverwaltung“, „Über uns“, „Kontakt“; rechts Telefon. Handy: Burger → Vollbild-Menü mit Staffelung, Kontakt unten.
7. **Einstieg ohne Scroll-Through** (Nils' Rückmeldung vom 28.9. für Bestandsseiten): großes eigenes Foto einer Stolberger Bruchstein-Häuserzeile, Leitsatz, darunter **zwei Wege als große Flächen**: „Ich suche ein Zuhause“ (Live-Zahl der Angebote) und „Ich möchte verkaufen“ (Zahl der vorgemerkten Suchaufträge). Ruhige Einblendung, leichter Tiefeneffekt.
8. **Sechs Bausteine der Startseite:** (a) **Aktuelle Angebote** – Karten mit Titelbild 4:3, Preis, Fläche, Zimmer, Ort, live; (b) **Käufer warten schon** (Signature); (c) **So verkaufen wir** – Sticky-Storytelling: links klebt ein Foto, rechts die echten Zusagen der alten Seite in fünf Kapiteln (Bewertung vor Ort, keine Sammelbesichtigungen, vorgemerkte Käufer, Bonitätsprüfung, bis zum Notar und danach), das Foto wechselt je Kapitel; (d) **Ortsteil-Register** – die 60 Referenzen der alten Seite, nach Ort gezählt (Zweifall, Mausbach, Breinig …), Balken wachsen beim Scrollen; (e) **Kundenstimmen** – echte Zitate mit Ort, zum Blättern per Pfeil; (f) **Rudolf Ritter & Maike Steyns** + Anfrage direkt in der Sektion.
9. **Unterseiten-Kopf „Hausschild“:** Titel in Fraunces auf einer kalkweißen Fläche mit feiner Sandlinie wie ein emailliertes Hausnummernschild, rechts ein eigenes Foto im Originalformat. Werkzeuge je Kernseite, alle neu: Angebote = Filter nach Art/Ort/Preis (live); Exposé = Kaufnebenkosten-Rechner NRW für genau dieses Objekt; Verkaufen = Suchauftrags-Abgleich; Bewertung = Verfahrens-Wähler (Vergleichs-, Sach-, Ertragswert je nach Objektart, Texte der alten Seite); Vermieten = Kautions-Rechner (§ 551 BGB); Finanzierung = Kaufnebenkosten-Rechner; Hausverwaltung = Jahreslauf der Verwaltung.
10. **Regler:** Dichte **4** (Eigentümer lesen in Ruhe, wenige Abschnitte, große Fotos), Kontrast **6** (Blau und Sand auf Kalkweiß), Bewegung **5** Startseite (ruhig, Bestandsseite – Nils' Rückmeldung), 4 Kernseiten, 1 Impressum/Datenschutz.

**Bewusst NICHT übernommen:** Foto-Scroll-Through und alle Szenen-Blenden, Scroll-Pins mit wechselnden Angeboten, Pill, Glasleiste, Overlay-Menü, linke Leiste, Logo mittig, zweizeilige Leiste; Energiefluss, Counter-Kacheln, Bento, Marquee, Wort-Wolke, Uhr, Akkordeon, Kreisdiagramm, Donut, Vorher/Nachher, Assistent, Vergleichstabelle, Filter-Galerie für Referenzen, Referenzkarte, Stempel, Zettel, Umschlag, Tachos, Schaltkulisse. AI-Tells ausgeschlossen. Aus der alten Seite nicht übernommen: Emoji-Überschriften, „V E R K A U F T“-Sperrschrift, Stockfotos (rcphotostock/Adobe), Fotos mit „VERKAUFT!“-Bannern.

## Inhaltsliste der alten Seite → neue Seite

| Alte Seite (Jimdo) | Neue Seite |
|---|---|
| Startseite (Leitsatz, Suche nach Objekten, Verkaufsmeldungen) | index.html |
| Über uns (seit 1989, Rudolf Ritter, Maike Steyns, PremiumPartner, Service für Senioren, Haushaltsauflösungen) | ueber-uns.html |
| Unsere Partner (Notare, Gutachter, IT) | ueber-uns.html (Abschnitt Partner) |
| Immobilien (immowelt-Modul) | angebote.html, objekt.html?id= |
| Hinweis (diskrete Angebote ohne Veröffentlichung) | angebote.html (Hinweis), faq.html |
| Eigentümer (Verkauf, Bewertungsverfahren) | verkaufen.html, bewertung.html |
| Aktuelle Suchanfragen | kaeufer-warten.html (Signature) |
| Immobilienverkauf (Garantien) | verkaufen.html |
| Immobilienvermietung (leer auf der alten Seite) | vermieten.html (aus Hausverwaltung/Über-uns-Texten, Umfang mit Kunde klären) |
| Meinungen / Kundenmeinungen | kundenstimmen.html |
| mein-Wohnhaus-bewerten.de | bewertung.html |
| Finanzierungen | finanzierung.html |
| Referenzen (Verkauf) | referenzen.html |
| Hausverwaltung + Referenzen | hausverwaltung.html |
| Urlaubsreif? (Ferienhaus auf Föhr) | ferienhaus-foehr.html (im Fuß verlinkt) |
| Kontakt, Impressum, Datenschutz, AGB, Widerrufsbelehrung | kontakt.html, impressum.html, datenschutz.html, agb.html, widerruf.html |

---

## 2. Fassung (29.9.2026 mittags) – nach Nils' Rückmeldung

Nils: „sieht noch zu sehr nach KI aus, das Scroll-Through soll eher wie ein Video sein, und die Bilder sind unscharf.“

- **Schärfe:** Alle Fotos neu aus den Jimdo-**Originalen** (bis 6000 px) statt der 1600-px-Vorschauen, als WebP in 800/1600/2400 px mit echten Breitenangaben im srcset. Das Außenfoto des Glasgiebel-Hauses gab es nur in 1024 px → Flug auf das **Bruchsteinhaus** umgestellt (durchgehend scharfe Serie): Hofweg → Diele mit Holztreppe → Wohnzimmer mit Bruchsteinwand und Kronleuchter → Garten mit Palmen → „Wie dürfen wir helfen?“. Kamera-Zoom höchstens 1,3-fach im Bild, stärkerer Zoom nur in der unscharfen Überblendung.
- **Wie ein Video:** durchgehende Kamerafahrt ohne Stillstand (Tempo gleichmäßig, scrub 1,2), leichte Handkamera-Bewegung, Zoom-Überblendungen mit Unschärfe statt sichtbarer Ausschnitt-Rechtecke, Texte nur als Untertitel, Titel nur am Anfang, Film-Korn und Vignette, dünne Zeitleiste wie bei einem Video.
- **Weniger KI:** Schrift **Schibsted Grotesk** statt Fraunces/Instrument Sans; redaktioneller Stil wie ein Architekturmagazin: Papierweiß, Tinte, Haarlinien statt Karten mit weichen Schatten, eckige Knöpfe, keine Überschriften-Etiketten, keine Pillen; Suchauftrags-Abgleich als Satz mit Auswahlfeldern („Ich möchte ein Einfamilienhaus in Stolberg verkaufen …“); Seitenkopf: großer Titel + Lead, darunter Foto über die volle Breite; Ritter-Blau nur als Akzent.

---

## 3. Fassung (29.9.2026 mittags) – Video statt Scroll-Through

Nils: „das Scroll-Through gefällt mir immer noch nicht, mach's lieber als Video.“ Der Einstieg ist jetzt ein **echtes Video** (MP4, H.264, 20,8 s, nahtlose Schleife, stumm, startet von selbst): Kamerafahrt durch das verkaufte Bruchsteinhaus – Hofweg → Diele → Wohnzimmer (Schwenk Bruchsteinwand → Fenster) → Garten → zurück zum Anfang. Aus den Originalfotos Bild für Bild gerendert (`scripts/video.js`, sharp + ffmpeg), weiche Überblendungen mit Bewegungsunschärfe. Zwei Fassungen: quer 1920 × 1080 (6,6 MB) und hoch 1080 × 1920 fürs Handy (5,5 MB), Vorschaubild je Format, Pause-Knopf, bei „reduzierter Bewegung“ kein Autostart. Darüber Titel und die zwei Wege. Kein gepinntes Scrollen mehr auf der Seite.
