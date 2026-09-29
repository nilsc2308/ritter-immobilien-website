// Holt die Originalfotos der alten Jimdo-Seite in voller Auflösung und erzeugt WebP in 800/1600/2400 px.
// Nur für die Entwicklung (Quelle _quelle/alt-img/index.json). Aufruf: node scripts/fotos.js
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const sharp = require('/Users/nilscremerius/Documents/website 1/co2-consulting-web/node_modules/sharp');
const Q = path.join(__dirname, '..', '_quelle'), IMG = path.join(__dirname, '..', 'img');
const idx = Object.fromEntries(JSON.parse(fs.readFileSync(path.join(Q, 'alt-img/index.json'))).map(x => [x.f.slice(-7, -4), x]));
const MAP = {
  // Flug durch das Bruchsteinhaus (eine Serie, gleiches Objekt)
  'flug-aussen': '004', 'flug-diele': '006', 'flug-wohnen': '007', 'flug-zimmer': '008', 'flug-garten': '012',
  // übrige Seite
  'glas-diele': '052', 'glas-wohnen': '053', 'glas-kueche': '055', 'wintergarten': '056', 'garten-palmen': '009',
  'wohnen-holz': '017', 'essplatz': '019', 'wohnen-hell': '070', 'garten-eifel': '110', 'bungalow': '108', 'weisses-haus': '103',
  'siedlungshaus': '090', 'haus-garten': '105', 'neubau': '113', 'hof-weiss': '201', 'team': '125', 'burg': '094', 'foehr-1': '266', 'foehr-2': '267',
};
(async () => {
  for (const [name, k] of Object.entries(MAP)) {
    const src = path.join(Q, 'orig', k + '.jpg');
    if (!fs.existsSync(src)) execFileSync('curl', ['-s', '-o', src, idx[k].url.replace(/transf\/[^/]+\//, 'transf/none/')]);
    const m = await sharp(src).metadata();
    for (const w of [800, 1600, 2400]) {
      const ww = Math.min(w, m.width);
      await sharp(src).rotate().resize(ww).sharpen({ sigma: ww < m.width * .6 ? .7 : .4 }).webp({ quality: w === 2400 ? 70 : 74, effort: 6 }).toFile(path.join(IMG, `${name}-${w}.webp`));
    }
    await sharp(src).resize(640).blur(10).webp({ quality: 50 }).toFile(path.join(IMG, `${name}-blur.webp`));
    console.log(name, k, m.width + 'x' + m.height);
  }
})();
