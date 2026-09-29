// Speichert einen Vorschau-Stand der Immobilien-Angebote (nur für die Vorschau außerhalb von ritterimmobilien.de).
// Die fertige Website unter ritterimmobilien.de lädt die Angebote bei jedem Aufruf live aus dem
// immowelt-Homepagemodul – dieses Skript braucht es dann nicht mehr.
//
// Ablauf: öffnet die öffentliche Angebotsseite von Ritter Immobilien in einem Browser, lässt das
// immowelt-Modul dort ganz normal laden, öffnet jedes Exposé und merkt sich die Antworten.
// Aufruf im Projektordner: node scripts/angebote-stand.js   (braucht Playwright)

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const SEITE = 'https://www.ritterimmobilien.de/immobilien/';
const ZIEL = path.join(__dirname, '..', 'data', 'angebote-stand.js');
const jsonp = t => JSON.parse(t.slice(t.indexOf('(') + 1, t.lastIndexOf(')')));

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  let liste = null; const exposes = {};
  page.on('response', async r => {
    const u = r.url();
    try {
      if (/\/list\/api\/list\//.test(u) && !liste) liste = jsonp(await r.text());
      const m = u.match(/\/home\/api\/Expose\/.*[?&]id=([0-9A-F-]+)/i);
      if (m) exposes[m[1].toUpperCase()] = jsonp(await r.text());
    } catch (e) { /* nächste Antwort */ }
  });
  await page.goto(SEITE, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2000);
  if (!liste) { console.error('Keine Angebotsliste erhalten.'); process.exit(1); }
  const ids = [...liste.matchAll(/ToExpose\("([0-9A-F-]+)"\)/gi)].map(m => m[1].toUpperCase());
  for (const id of ids) {
    await page.evaluate(i => IwAG.HomepageModul.getInstance().ToExpose(i), id);
    for (let t = 0; t < 30 && !exposes[id]; t++) await page.waitForTimeout(250);
    console.log(id, exposes[id] ? 'ok' : 'fehlt');
  }
  await browser.close();
  // schlank machen: Formulare, Skripte, Leerraum raus – Daten und Texte bleiben
  const schlank = h => h.replace(/<script[\s\S]*?<\/script>/gi, '').replace(/<fieldset[\s\S]*?<\/fieldset>/gi, '')
    .replace(/<div id="(divcontact|recommend|iwrecommend|hm_printContainer)"[\s\S]*?<\/div>\s*<\/div>/gi, '').replace(/<select[\s\S]*?<\/select>/gi, '')
    .replace(/\s+/g, ' ').replace(/> </g, '><');
  Object.keys(exposes).forEach(k => exposes[k] = schlank(exposes[k]));
  const stand = { stand: new Date().toISOString(), liste: schlank(liste), exposes };
  fs.mkdirSync(path.dirname(ZIEL), { recursive: true });
  fs.writeFileSync(ZIEL, 'window.RI_STAND=' + JSON.stringify(stand) + ';\n');
  console.log('Gespeichert:', ids.length, 'Angebote');
})();
