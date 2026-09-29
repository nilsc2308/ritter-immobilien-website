/* Ritter Immobilien – Werkzeuge: Suchauftrags-Abgleich, Bewertungsverfahren, Kaution, Kaufnebenkosten, Verwaltungsjahr, Referenzen. */
(() => {
  const X = window.RIX || {};
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const eur = n => Math.round(n).toLocaleString('de-DE') + ' €';
  const num = s => Number(String(s).replace(/[^\d]/g, '')) || 0;
  const motion = X.motion;
  const seg = (g, cb) => g && g.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; $$('button', g).forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false')); cb && cb(b.dataset.v); });
  const val = g => ($('[aria-pressed="true"]', g) || {}).dataset?.v;
  const pop = els => motion && gsap.fromTo(els, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .4, stagger: .05, ease: 'power3.out' });

  // ---------- Käufer warten schon (Signature) ----------
  const matchers = $$('[data-matcher]');
  if (matchers.length) {
    const laden = new Promise(res => {
      if (window.RI_SUCH) return res(window.RI_SUCH);
      const s = document.createElement('script'); s.src = 'data/suchauftraege.js';
      s.onload = () => res(window.RI_SUCH); s.onerror = () => res(null); document.head.appendChild(s);
    });
    laden.then(d => {
      if (!d) return;
      matchers.forEach(m => {
        const out = { n: $('[data-m-n]', m), label: $('[data-m-label]', m), list: $('[data-m-list]', m), cta: $('[data-m-cta]', m) };
        const reno = $('[data-m-reno]', m);
        const run = () => {
          const typ = val($('[data-m="typ"]', m)), ort = val($('[data-m="ort"]', m)), preis = +val($('[data-m="preis"]', m));
          // Preisband: „bis 350.000 €“ heißt 150.000–350.000 €; ein Suchauftrag passt, wenn sein Budget über der Untergrenze liegt
          const unten = { 150000: 0, 350000: 150000, 600000: 350000, 999999999: 600000 }[preis] || 0;
          const passt = d.auftraege.filter(a => {
            const t = a.typ.includes(typ);
            const o = a.orte.includes('alle') || a.orte.includes(ort);
            const p = !a.max || unten < a.max;
            const z = !a.zustand || reno.checked;
            return t && o && p && z;
          });
          out.n.textContent = passt.length;
          out.label.textContent = passt.length === 1 ? 'vorgemerkter Suchauftrag passt' : 'vorgemerkte Suchaufträge passen';
          out.list.innerHTML = passt.length ? passt.map(a => `<li><span class="k-wer">${esc(a.wer)}</span>${esc(a.text)}</li>`).join('')
            : '<li class="leer">Aus unserer veröffentlichten Liste passt gerade nichts genau – viele Suchaufträge erreichen uns aber nur telefonisch. Rufen Sie uns an: 02402 3477.</li>';
          const typT = $('[data-m="typ"] [aria-pressed="true"]', m).textContent, ortT = $('[data-m="ort"] [aria-pressed="true"]', m).textContent, prT = $('[data-m="preis"] [aria-pressed="true"]', m).textContent;
          out.cta.href = 'kontakt.html?thema=verkauf&details=' + encodeURIComponent(`Ich möchte verkaufen: ${typT} in ${ortT}, Preisvorstellung ${prT}${reno.checked ? ', renovierungsbedürftig' : ''}. Passende Suchaufträge laut Website: ${passt.length}.`);
          pop($$('li', out.list));
          if (motion) gsap.fromTo(out.n, { scale: 1.25 }, { scale: 1, duration: .45, ease: 'back.out(3)' });
        };
        $$('[data-m]', m).forEach(g => seg(g, run));
        reno.addEventListener('change', run);
        run();
      });
    });
  }

  // ---------- Bewertungsverfahren ----------
  const verf = $('[data-verf]');
  if (verf) seg($('[data-verf-typ]', verf), v => { $$('[data-verf-k]', verf).forEach(a => a.hidden = a.dataset.verfK !== v); pop($(`[data-verf-k="${v}"]`, verf)); });

  // ---------- Kaution ----------
  const kau = $('[data-kaution]');
  if (kau) {
    const inp = $('[data-k-miete]', kau), out = $('[data-k-out]', kau);
    const run = () => {
      const m = num(inp.value);
      out.innerHTML = m ? `<div><dt>Höchstens zulässige Kaution</dt><dd>${eur(m * 3)}</dd></div><div><dt>Zahlbar in drei Raten zu je</dt><dd>${eur(m)}</dd></div><div><dt>Erste Rate</dt><dd>zu Beginn des Mietverhältnisses</dd></div>` : '<div><dt>Hinweis</dt><dd>Bitte eine Kaltmiete eingeben</dd></div>';
    };
    inp.addEventListener('input', run); inp.addEventListener('blur', () => { const n = num(inp.value); if (n) inp.value = n.toLocaleString('de-DE'); }); run();
  }

  // ---------- Kaufnebenkosten (Seite Finanzierung und Exposé) ----------
  const nkRender = (preis, box) => {
    const prov = +val($('[data-nk-prov]', box)) || 0;
    const grest = preis * .065, notar = preis * .02, makler = preis * prov / 100, summe = grest + notar + makler;
    $('[data-nk-out]', box).innerHTML = `<div><dt>Grunderwerbsteuer (6,5 %)</dt><dd>${eur(grest)}</dd></div><div><dt>Notar und Grundbuch (ca. 2 %)</dt><dd>${eur(notar)}</dd></div>` +
      (prov ? `<div><dt>Maklerprovision (${String(prov).replace('.', ',')} %)</dt><dd>${eur(makler)}</dd></div>` : '') +
      `<div class="sum"><dt>Nebenkosten gesamt</dt><dd>${eur(summe)}</dd></div><div class="sum2"><dt>Gesamtaufwand</dt><dd>${eur(preis + summe)}</dd></div>`;
  };
  const nkPage = $('[data-nk-page]');
  if (nkPage) {
    const inp = $('[data-nk-preis]', nkPage);
    const run = () => nkRender(num(inp.value), nkPage);
    seg($('[data-nk-prov]', nkPage), run); inp.addEventListener('input', run);
    inp.addEventListener('blur', () => { const n = num(inp.value); if (n) inp.value = n.toLocaleString('de-DE'); }); run();
  }
  const nkObj = $('[data-nk]');
  if (nkObj) window.RI_NK = preis => { nkObj.hidden = false; seg($('[data-nk-prov]', nkObj), () => nkRender(preis, nkObj)); nkRender(preis, nkObj); };

  // ---------- Verwaltungsjahr ----------
  const hv = $('[data-hv]');
  if (hv) {
    const T = m => {
      const L = [];
      if (m <= 11) L.push(['Laufend', 'Mieterbetreuung, Kommunikation mit Handwerkern und Dienstleistern, Mieteingang.']);
      if (m >= 0 && m <= 3) L.unshift(['Nebenkostenabrechnung', 'Abrechnung für das Vorjahr erstellen – sie muss spätestens zwölf Monate nach Ende des Abrechnungszeitraums bei den Mietern sein.']);
      if (m === 2 || m === 3 || m === 8 || m === 9) L.unshift(['Objektbegehung', 'Regelmäßiger Rundgang mit Blick auf Dach, Fassade, Keller, Treppenhaus und Außenanlagen, Gespräche mit Mietern und Hausmeister.']);
      if (m >= 3 && m <= 5) L.push(['Gartenpflege', 'Saisonstart der Gartenpflege – Aufträge prüfen und überwachen.']);
      if (m >= 9 || m <= 1) L.push(['Winterdienst', 'Räum- und Streupflicht organisieren und überwachen, Heizungswartung vor der Heizperiode.']);
      if (m === 10 || m === 11) L.push(['Wirtschaftsplan', 'Kosten und anstehende Reparaturen für das nächste Jahr planen, Vorauszahlungen prüfen.']);
      if (m >= 5 && m <= 7) L.push(['Reparaturen', 'Sommerzeit ist Bauzeit: anstehende Instandhaltungen koordinieren und abnehmen.']);
      return L;
    };
    const out = $('.season-out', hv);
    const show = m => { $$('.season-m button', hv).forEach((b, i) => b.setAttribute('aria-pressed', i === m ? 'true' : 'false')); out.innerHTML = T(m).map(([h, t]) => `<article><h3>${h}</h3><p>${t}</p></article>`).join(''); pop($$('article', out)); };
    $('.season-m', hv).addEventListener('click', e => { const b = e.target.closest('button'); if (b) show(+b.dataset.m); });
    show(new Date().getMonth());
  }

  // ---------- Referenzen nach Ort ----------
  const ro = $('.ref-orte');
  if (ro) {
    const items = $$('[data-ref-list] li');
    ro.addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      $$('button', ro).forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
      items.forEach(li => li.hidden = !!b.dataset.o && li.dataset.ort !== b.dataset.o);
      pop(items.filter(li => !li.hidden).slice(0, 20));
    });
  }
})();
