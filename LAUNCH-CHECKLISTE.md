# Launch-Checkliste – Ritter Immobilien e.K. (Stand 29.9.2026)

Unbeauftragter Entwurf. Bisherige Seite: www.ritterimmobilien.de (Jimdo, Copyright 2017).

## Offen beim Kunden

- [ ] **Einverständnis** von Rudolf Ritter für die neue Website.
- [ ] **Domain:** Die Angebote laden nur live, wenn die Seite unter **ritterimmobilien.de** läuft (das immowelt-Homepagemodul ist an diese Domain gebunden). Vor dem Umzug im immowelt-Kundenbereich prüfen, ob `www.` und ohne `www.` freigeschaltet sind. Bis dahin zeigt die Vorschau den Stand vom 29.9.2026 (9 Angebote).
- [ ] **Nutzung des Homepagemoduls** im eigenen Design mit immowelt abstimmen (die Seite ruft dieselben Schnittstellen auf wie das Original-Modul, stellt sie aber selbst dar). Fallback: das Original-Modul-Skript einbinden.
- [ ] **Fotorechte:** eigene Objektfotos von der alten Seite; Freigabe bestätigen. Der Flug zeigt das verkaufte Bruchsteinhaus (Originalfotos bis 6000 px). Schön wäre ein echtes Drohnen-/Rundgangvideo eines Objekts – es ersetzt einfach `video/flug-quer.mp4` und `video/flug-hoch.mp4`.
- [ ] **Kundenstimmen** mit Namen stammen von der alten Seite – Veröffentlichung weiterhin in Ordnung?
- [ ] **Suchaufträge** (Stand 12.09.2025) aktualisieren; sie stehen in `_build.py` (Liste `SUCH`).
- [ ] **Vermietung:** Die alte Unterseite „Immobilienvermietung“ war leer; Texte aus Hausverwaltung und Kundenstimmen abgeleitet – Leistungsumfang bestätigen.
- [ ] **Maklerprovision:** Rechner nutzt 3,57 % Käuferanteil als üblichen Wert – tatsächliche Höhe bestätigen.
- [ ] **Hoster und Formular-Dienst** in der Datenschutzerklärung eintragen (Platzhalter in Abschnitt 3 und 6).
- [ ] Öffnungszeiten (alte Seite nennt keine) – aktuell „Termine nach Vereinbarung“.
- [ ] Ferienhaus auf Föhr: Wird es noch vermietet? Sonst Seite entfernen.
- [ ] Bewusst weggelassen: Stockfotos, Fotos mit „VERKAUFT!“-Bannern, Emoji-Überschriften, Facebook-/Instagram-Einbindung (nur Links möglich), Google-Maps-Einbettung (ersetzt durch OpenStreetMap per Klick), Bewertungs-Widgets von immowelt/ImmoScout/makler-vergleich (Auszeichnungen stehen als Text auf „Über uns“).

## Technik & Recht – geprüft 29.9.2026

| Punkt | Ergebnis |
|---|---|
| Datenschutz | `datenschutz.html`: keine Cookies/Tracking; jsDelivr, immowelt-Homepagemodul + Bildserver, OSM per Klick, GwG. Hoster/Formular als Platzhalter. |
| Impressum | Angaben der alten Seite: Inhaber Rudolf Ritter, HRA 9345 AG Aachen, USt-ID DE 121824998, § 34c GewO, Aufsicht StädteRegion Aachen, IHK Aachen. |
| AGB / Widerruf | übernommen: `agb.html`, `widerruf.html`. |
| Cookie-Banner | nicht nötig. |
| Mobile | Playwright 390 × 844, Chromium + WebKit, alle 25 Seiten durchgescrollt: kein seitliches Scrollen (nach Korrektur der Eingabefelder). Flug läuft am Handy wie am Desktop. |
| JS-Fehler | 0 (Chromium, WebKit; 1400 px und 390 px). |
| Einstiegsvideo | läuft in WebKit (Desktop 1920 × 1080, Handy 1080 × 1920), Pause-Knopf getestet, Autostart aus bei reduzierter Bewegung; Video 6,6 / 5,5 MB, lädt erst nach dem Seitenaufbau nach. |
| Meta | alle Titel ≤ 65, Descriptions ≤ 155 Zeichen. |
| Favicon / OG | `favicon.svg`, `apple-touch-icon.png`, `og.jpg` 1200 × 630. |
| Sitemap / Robots / Canonical | vorhanden; Canonical auf https://www.ritterimmobilien.de/. |
| 404 | `404.html`; Exposé eines verkauften Objekts zeigt „verkauft oder reserviert“ + Angebote. |
| Links | 42 interne Links: 0 kaputt. |
| Performance | bis „load“: Desktop 554 KB, Handy 456 KB (Video, Kapitelfotos und Angebote laden danach). |
| Formular | Netlify-Forms + Honeypot; Pflichtfelder (3 markiert), `?thema=` und `?objekt=` vorbelegt; Vorschau leitet auf danke.html. |
| Weiterleitungen | alte Jimdo-Adressen → neue Seiten in `netlify.toml`. |
| Lokale SEO | JSON-LD `RealEstateAgent` auf allen Seiten, `FAQPage`, `Article`, `Offer` im Exposé. |
| Barrierefreiheit | Tastatur (Menü mit Fokusfalle, Kundenstimmen per Pfeil), Kontrast Ritter-Blau auf Weiß 9,6 : 1, reduzierte Bewegung: Flug wird zur Foto-Reihe. |

## Richtwerte

Kaufnebenkosten: Grunderwerbsteuer NRW 6,5 % (gesetzlich), Notar/Grundbuch 2 % (Richtwert), Provision laut Auswahl. Kaution: § 551 BGB (drei Nettokaltmieten). Verwaltungsjahr und Bewertungs-Hinweise: allgemeine Richtwerte, auf den Seiten gekennzeichnet.
