# Ritter Immobilien – Website

Statischer Mehrseiter (25 Seiten), erzeugt mit `_build.py`. Gestaltung: `DESIGN.md`, offene Punkte: `LAUNCH-CHECKLISTE.md`.

## Ansehen
Im Projektordner `python3 -m http.server 8774` und http://localhost:8774 öffnen.

## Texte ändern
Texte stehen in `_build.py` (z. B. Suchaufträge in `SUCH`, Kundenstimmen in `STIMMEN`). Danach `python3 _build.py`.

## Wie die Angebote aktuell bleiben
Ritter Immobilien hat bei immowelt ein **Homepagemodul** (schon auf der alten Seite eingebunden). `angebote.js` lädt Liste und Exposés bei jedem Seitenaufruf direkt dort – im eigenen Design. Neue, geänderte oder verkaufte Objekte erscheinen damit sofort, ohne dass jemand etwas tun muss.

Wichtig: immowelt liefert nur an die registrierte Domain **ritterimmobilien.de**. Auf jeder anderen Adresse (z. B. der GitHub-Vorschau) greift automatisch ein gespeicherter Stand aus `data/angebote-stand.js` – auf der Seite als „Vorschau-Stand“ markiert. Neu speichern: `node scripts/angebote-stand.js`.

## Suchaufträge pflegen
Liste `SUCH` in `_build.py` anpassen (Text, Objektart, Orte, Budget), dann `python3 _build.py` – der Abgleich „Käufer warten schon“ nutzt sie sofort.
