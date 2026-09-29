// Rendert das Einstiegsvideo (Kamerafahrt durch das verkaufte Bruchsteinhaus) aus den Originalfotos.
// Aufruf: node scripts/video.js quer|hoch   → video/flug-quer.mp4 bzw. video/flug-hoch.mp4 + Posterbild
// Braucht sharp und ffmpeg (Pfad in FFMPEG).
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const sharp = require('/Users/nilscremerius/Documents/website 1/co2-consulting-web/node_modules/sharp');
const FFMPEG = process.env.FFMPEG || '/private/tmp/claude-501/-Users-nilscremerius/8a68bef3-a22a-4d16-ba0b-a21cea6c7f25/scratchpad/ff/node_modules/ffmpeg-static/ffmpeg';
const ROOT = path.join(__dirname, '..'), ORIG = path.join(ROOT, '_quelle', 'orig');
const MODE = process.argv[2] || 'quer';
const [OW, OH] = MODE === 'hoch' ? [1080, 1920] : [1920, 1080];
const FPS = 30;
const TMP = path.join(require('os').tmpdir(), 'ri-frames-' + MODE);

// Einstellungen: Quelle, Dauer (s), Kamera von → nach: Mittelpunkt (x,y in 0..1) und Zoom
const SHOTS = [
  { src: '004', d: 6.0, from: { x: .40, y: .45, z: 1.08 }, to: { x: .46, y: .43, z: 1.42 } },   // Hofweg zur Tür
  { src: '006', d: 5.6, from: { x: .47, y: .45, z: 1.00 }, to: { x: .45, y: .41, z: 1.45 } },   // Diele zur hinteren Tür
  { src: '007', d: 6.2, from: { x: .30, y: .52, z: 1.18 }, to: { x: .74, y: .42, z: 1.34 } },   // Schwenk Bruchsteinwand → Fenster
  { src: '012', d: 6.0, from: { x: .50, y: .55, z: 1.00 }, to: { x: .52, y: .50, z: 1.40 } },   // den Gartenweg entlang
];
const X = 1.0;                         // Überblendung (s)
const ease = t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;      // weich
const lerp = (a, b, t) => a + (b - a) * t;

(async () => {
  fs.rmSync(TMP, { recursive: true, force: true }); fs.mkdirSync(TMP, { recursive: true });
  // Quellen einmal dekodieren (Arbeitsauflösung 4000 px Breite)
  const src = {};
  for (const s of SHOTS) {
    const img = sharp(path.join(ORIG, s.src + '.jpg')).rotate().resize({ width: 4000, withoutEnlargement: true });
    const { data, info } = await img.raw().toBuffer({ resolveWithObject: true });
    src[s.src] = { data, w: info.width, h: info.height, c: info.channels };
  }
  // Zeitplan: Einstellungen überlappen um X Sekunden
  let t0 = 0; SHOTS.forEach(s => { s.t0 = t0; s.t1 = t0 + s.d; t0 = s.t1 - X; });
  const total = t0 + X;                // letzte Überblendung führt zurück zum Anfang (Schleife)
  const frames = Math.round(total * FPS);
  const view = (s, t) => {             // Kameraausschnitt einer Einstellung zur Zeit t (auch vor/nach ihrer Dauer für Überblendungen)
    const S = src[s.src], p = (t - s.t0) / s.d;
    let k = ease(Math.min(1, Math.max(0, p)));
    let z = lerp(s.from.z, s.to.z, k), x = lerp(s.from.x, s.to.x, k), y = lerp(s.from.y, s.to.y, k);
    if (p > 1) z *= 1 + (p - 1) * s.d * .22;         // am Ende weiter hinein (Durchflug)
    if (p < 0) z *= 1 / (1 + (-p) * s.d * .10);      // am Anfang von etwas weiter weg
    z = Math.max(1, z);
    const A = OW / OH;
    let bw = S.w, bh = S.w / A; if (bh > S.h) { bh = S.h; bw = S.h * A; }
    const w = bw / z, h = bh / z;
    let l = x * S.w - w / 2, tp = y * S.h - h / 2;
    l = Math.max(0, Math.min(S.w - w, l)); tp = Math.max(0, Math.min(S.h - h, tp));
    return { l, tp, w, h };
  };
  const render = async (s, t, blur) => {
    const S = src[s.src], v = view(s, t);
    let im = sharp(S.data, { raw: { width: S.w, height: S.h, channels: S.c } })
      .extract((() => { const w = Math.min(S.w, Math.round(v.w)), h = Math.min(S.h, Math.round(v.h)); return { left: Math.min(S.w - w, Math.max(0, Math.round(v.l))), top: Math.min(S.h - h, Math.max(0, Math.round(v.tp))), width: w, height: h }; })())
      .resize(OW, OH, { kernel: 'lanczos3' });
    if (blur > .3) im = im.blur(blur);
    return im.removeAlpha().raw().toBuffer();
  };
  for (let f = 0; f < frames; f++) {
    const t = f / FPS;
    // aktive Einstellungen (inkl. der ersten als Nachfolger der letzten für die Schleife)
    const act = [];
    SHOTS.forEach(s => { if (t >= s.t0 - 1e-6 && t < s.t1) act.push({ s, t }); });
    if (t >= total - X) act.push({ s: SHOTS[0], t: t - total });
    act.sort((a, b) => (a.s.t0 + (a.t < 0 ? 999 : 0)) - (b.s.t0 + (b.t < 0 ? 999 : 0)));
    let buf;
    if (act.length === 1) buf = await render(act[0].s, act[0].t, 0);
    else {
      const [a, b] = act;               // a endet, b beginnt
      const tb = b.t < 0 ? t - (total - X) : b.t - b.s.t0;
      const k = Math.min(1, Math.max(0, tb / X)), m = ease(k);
      const bl = Math.sin(Math.PI * k) * 7;          // Unschärfe in der Mitte der Überblendung
      const A = await render(a.s, a.t, bl), B = await render(b.s, b.t < 0 ? b.t : b.t, bl);
      buf = Buffer.alloc(A.length);
      for (let i = 0; i < A.length; i++) buf[i] = A[i] * (1 - m) + B[i] * m;
    }
    await sharp(buf, { raw: { width: OW, height: OH, channels: 3 } }).jpeg({ quality: 93 }).toFile(path.join(TMP, String(f).padStart(5, '0') + '.jpg'));
    if (f % 60 === 0) process.stdout.write(`${f}/${frames} `);
  }
  const out = path.join(ROOT, 'video'); fs.mkdirSync(out, { recursive: true });
  const mp4 = path.join(out, `flug-${MODE}.mp4`);
  execFileSync(FFMPEG, ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(TMP, '%05d.jpg'),
    '-c:v', 'libx264', '-preset', 'slower', '-tune', 'film', '-crf', '28', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-movflags', '+faststart', '-an', mp4]);
  await sharp(path.join(TMP, '00000.jpg')).webp({ quality: 72 }).toFile(path.join(out, `flug-${MODE}-poster.webp`));
  console.log('\nfertig', mp4, (fs.statSync(mp4).size / 1e6).toFixed(1) + ' MB', total.toFixed(1) + ' s');
})();
