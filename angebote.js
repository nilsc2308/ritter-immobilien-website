/* Ritter Immobilien – Angebote live aus dem immowelt-Homepagemodul des Maklers.
   Auf ritterimmobilien.de liefert das Modul Liste und Exposés bei jedem Aufruf aktuell.
   Anderswo (Vorschau) lehnt immowelt ab → gespeicherter Stand aus data/angebote-stand.js. */
(() => {
  const GUID = 'c57171380d504aaa9b52af8626cd44fb';
  const API = 'https://homepagemodul.immowelt.de';
  const CACHE_MIN = 10;
  const IMG = (base, w = 800) => base ? `${base}/${w}x${Math.round(w * .75)}.webp` : '';

  let n = 0;
  const jsonp = (path, params, timeout = 8000) => new Promise((res, rej) => {
    const cb = '__riCb' + (++n) + Date.now();
    const q = new URLSearchParams({ callback: cb, guid: GUID, ...params, _: Date.now() });
    const s = document.createElement('script');
    const done = (fn, v) => { clearTimeout(t); delete window[cb]; s.remove(); fn(v); };
    const t = setTimeout(() => done(rej, new Error('Zeitüberschreitung')), timeout);
    window[cb] = data => done(res, data);
    s.onerror = () => done(rej, new Error('Netzwerk'));
    s.src = `${API}${path}?${q}`;
    document.head.appendChild(s);
  });
  const ok = h => typeof h === 'string' && !/Anfrage fehlerhaft|Keine g(&uuml;|ü)ltigen Daten/i.test(h) && h.length > 200;

  let standP;
  const stand = () => standP || (standP = new Promise(res => {
    if (window.RI_STAND) return res(window.RI_STAND);
    const s = document.createElement('script'); s.src = 'data/angebote-stand.js';
    s.onload = () => res(window.RI_STAND || null); s.onerror = () => res(null);
    document.head.appendChild(s);
  }));

  const txt = el => el ? el.textContent.replace(/\s+/g, ' ').trim() : '';
  const num = s => { const m = String(s || '').replace(/\./g, '').replace(',', '.').match(/[\d.]+/); return m ? parseFloat(m[0]) : null; };
  const titel = t => t.replace(/^Ritter Immobilien e\.?\s?K\.?\s*:\s*/i, '').replace(/\s*!+\s*$/, '').trim();
  const artVon = (t, o) => /grundst/i.test(t) && !o.wohnflaeche ? 'grund' : /wohnung|etw|zimmer-|zikdb|appartement|penthouse/i.test(t) ? 'wohnung' : /garage|stellplatz|büro|laden|halle|gewerbe/i.test(t) ? 'sonst' : 'haus';

  // ---------- Liste zerlegen ----------
  function parseListe(html) {
    const doc = new DOMParser().parseFromString(html, 'text/html');
    return [...doc.querySelectorAll('.hm_listbox')].map((box, i) => {
      const a = box.querySelector('a');
      const id = ((a && a.getAttribute('href')) || '').match(/ToExpose\("([^"]+)"\)/);
      const im = box.querySelector('img');
      const src = im ? im.getAttribute('src') : '';
      const o = { id: id ? id[1].toUpperCase() : '', titel: titel(txt(box.querySelector('h2'))), neu: !!box.querySelector('.hm_icon_new'), reihe: i };
      o.bild = /ms\.immowelt\.org/.test(src) ? src.replace(/\/\d+x\d+(\.\w+)?$/, '') : '';
      const strongs = [...box.querySelectorAll('strong.hm_price')];
      strongs.forEach(s => {
        const label = txt(s.nextElementSibling), val = txt(s);
        if (/kaufpreis/i.test(label)) { o.preis = num(val); o.km = 'kauf'; o.preisText = val; o.preisLabel = 'Kaufpreis'; }
        else if (/miete|kalt/i.test(label)) { o.preis = num(val); o.km = 'miete'; o.preisText = val; o.preisLabel = label; }
        else if (/wohnfl/i.test(label)) o.wohnflaeche = num(val);
        else if (/grundst/i.test(label)) o.grundstueck = num(val);
        else if (/zimmer/i.test(label)) o.zimmer = num(val);
        else if (/fläche|nutzfl/i.test(label)) o.flaeche = num(val);
      });
      o.merkmale = [...box.querySelectorAll('.hm_listextrafield li span')].map(txt).filter(Boolean);
      o.ort = txt(box.querySelector('.hm_listaddress span'));
      const ohne = o.ort.replace(/\s*\((Rheinland|Rhld\.?)\)/i, '');
      o.ortKurz = (ohne.match(/\(([^)]+)\)\s*$/) || [])[1] || '';
      o.stadt = o.ort.replace(/^\d{5}\s*/, '').replace(/\s*\(.*$/, '').trim();
      o.art = artVon(o.titel, o);
      return o;
    }).filter(o => o.id);
  }

  // ---------- Exposé zerlegen ----------
  function parseExpose(html) {
    const doc = new DOMParser().parseFromString(html, 'text/html');
    const daten = [...doc.querySelectorAll('#hm_objectdata li')].map(li => {
      const l = li.querySelector('.hm_data_label'); if (!l) return null;
      const label = txt(l).replace(/:$/, ''); const val = txt(li).replace(txt(l), '').trim();
      return val ? [label, val] : null;
    }).filter(Boolean);
    const merkmale = [...doc.querySelectorAll('#hm_features li')].map(txt).filter(Boolean);
    const energieTraeger = [...doc.querySelectorAll('#hm_energy > ul li, #hm_energy ul.hm_features li')].map(txt).filter(Boolean);
    const energie = [...doc.querySelectorAll('#hm_energy table tr')].map(tr => [...tr.querySelectorAll('td')].map(txt)).filter(r => r.length === 2 && r[1]);
    const adr = [...doc.querySelectorAll('h2')].find(h => /Objektanschrift/.test(h.textContent));
    const anschrift = adr ? [...adr.parentElement.querySelectorAll('span')].map(txt).filter(x => x && x !== 'Deutschland').join(' ') : '';
    const texte = [];
    const beschr = [...doc.querySelectorAll('h2')].find(h => /Objektbeschreibung/.test(h.textContent));
    if (beschr) {
      const box = beschr.parentElement;
      box.querySelectorAll('strong').forEach(st => {
        const p = st.nextElementSibling;
        if (p && p.tagName === 'P') texte.push([txt(st), p.innerHTML.replace(/<br\s*\/?>/gi, '\n').replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/\?\?/g, '').trim()]);
      });
    }
    const get = k => (daten.find(d => d[0].toLowerCase().startsWith(k)) || [])[1] || '';
    return { daten, merkmale, energieTraeger, energie, anschrift, texte, onlineId: get('online-id'), art: get('immobilienart'), kategorie: get('kategorie') };
  }

  // ---------- öffentlicher Zugriff ----------
  const store = (k, v) => { try { sessionStorage.setItem(k, JSON.stringify({ t: Date.now(), v })); } catch (e) {} };
  const cached = k => { try { const o = JSON.parse(sessionStorage.getItem(k)); if (o && Date.now() - o.t < CACHE_MIN * 60000) return o.v; } catch (e) {} return null; };

  let listeP;
  function liste() {
    if (listeP) return listeP;
    const c = cached('ri-liste');
    if (c) return (listeP = Promise.resolve(c));
    listeP = (async () => {
      let quelle = 'live', html = null, standDatum = null;
      try {
        const alle = []; let seite = 1, gesamt = 1;
        while (seite <= gesamt && seite <= 10) {
          const h = await jsonp('/list/api/list/', { area: '', eType: -1, eCat: -1, geoid: -1, livingarea: '', page: seite, price: '', rentfactor: '', room: '', squareprice: '', wi: '' });
          if (!ok(h)) throw new Error('abgelehnt');
          alle.push(h);
          const m = h.match(/von\s+(\d+)\s+Objekt/); const pro = (h.match(/hm_listbox/g) || []).length || 1;
          gesamt = m ? Math.ceil(+m[1] / pro) : 1; seite++;
        }
        html = alle.join('');
      } catch (e) {
        const s = await stand();
        if (!s) throw new Error('keine Angebote');
        html = s.liste; quelle = 'stand'; standDatum = s.stand;
      }
      const res = { quelle, stand: standDatum, angebote: parseListe(html) };
      store('ri-liste', res);
      return res;
    })();
    return listeP;
  }

  async function expose(id) {
    id = String(id).toUpperCase();
    const c = cached('ri-exp-' + id); if (c) return c;
    let html = null, quelle = 'live';
    try {
      html = await jsonp('/home/api/Expose/', { id, isVorschau: '', isStatistic: 'false' });
      if (!ok(html)) throw new Error('abgelehnt');
    } catch (e) {
      const s = await stand(); html = s && s.exposes[id]; quelle = 'stand';
      if (!html) return null;
    }
    const res = { quelle, ...parseExpose(html) };
    store('ri-exp-' + id, res);
    return res;
  }

  // Zahl im Menü nur aus dem Zwischenspeicher (kein Abruf auf Seiten ohne Angebote)
  const menge = () => { const c = cached('ri-liste'); return c ? c.angebote.length : null; };

  window.RI = { liste, expose, menge, IMG };
})();
