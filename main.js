/* Ritter Immobilien – gemeinsames Skript. GSAP + ScrollTrigger + Lenis (CDN). Tweens nur auf transform/opacity. */
(() => {
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
  const hasGsap = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';
  const motion = !reduce && hasGsap;
  root.classList.add(motion ? 'js-motion' : 'no-motion');
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const eur = n => n == null ? '' : Math.round(n).toLocaleString('de-DE') + ' €';
  const qm = n => n == null ? '' : n.toLocaleString('de-DE', { maximumFractionDigits: 0 }) + ' m²';
  const params = new URLSearchParams(location.search);

  // ---------- Lenis ----------
  let lenis;
  if (motion && typeof Lenis !== 'undefined') {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }

  // ---------- Kopfzeile ----------
  const head = $('#head');
  const dds = $$('.has-dd');
  const setDd = (li, open) => { li.classList.toggle('open', open); $('button', li).setAttribute('aria-expanded', open ? 'true' : 'false'); };
  const closeDds = except => dds.forEach(li => li !== except && setDd(li, false));
  dds.forEach(li => {
    const b = $('button', li);
    b.addEventListener('click', () => { const o = !li.classList.contains('open'); closeDds(li); setDd(li, o); });
    if (fine) { li.addEventListener('mouseenter', () => { closeDds(li); setDd(li, true); }); li.addEventListener('mouseleave', () => setDd(li, false)); }
    li.addEventListener('focusout', e => { if (!li.contains(e.relatedTarget)) setDd(li, false); });
  });
  document.addEventListener('click', e => { if (!e.target.closest('.has-dd')) closeDds(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { const o = dds.find(li => li.classList.contains('open')); if (o) { setDd(o, false); $('button', o).focus(); } } });
  const hero = $('.hero, .flug');
  const overStart = head.classList.contains('over');
  let lastY = scrollY;
  const onScroll = () => {
    const y = scrollY;
    const overZone = overStart && hero && y < hero.offsetHeight - innerHeight * 1.7;
    if (overStart) head.classList.toggle('over', !!overZone && !document.body.classList.contains('menu-open'));
    if (!document.body.classList.contains('menu-open') && !dds.some(li => li.classList.contains('open'))) {
      if (!overZone && y > 300 && y > lastY + 6 && y - lastY < 400) head.classList.add('hide');
      else if (y < lastY - 6 || overZone || y < 300) head.classList.remove('hide');
    }
    lastY = y;
    const sc = $('.sticky-cta');
    if (sc) sc.classList.toggle('show', y > 520 && scrollY + innerHeight < document.documentElement.scrollHeight - 700 && !blockers.size);
  };
  const blockers = new Set();
  addEventListener('scroll', onScroll, { passive: true });
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => { es.forEach(en => en.isIntersecting ? blockers.add(en.target) : blockers.delete(en.target)); onScroll(); });
    $$('.form, .cta-end, .obj-side, .filters, .matcher, .flug').forEach(el => io.observe(el));
  }
  onScroll();

  // ---------- Menü (Handy) ----------
  const menu = $('#menu'), menuBtn = $('.menu-btn');
  $$('li', menu).forEach((li, i) => li.style.setProperty('--i', i));
  let lastFocus;
  const closeMenu = () => {
    if (!menu.classList.contains('open')) return;
    document.body.classList.remove('menu-open'); menu.classList.remove('open');
    menuBtn.setAttribute('aria-expanded', 'false'); $('.lbl', menuBtn).textContent = 'Menü';
    lenis && lenis.start(); onScroll(); lastFocus && lastFocus.focus();
  };
  const openMenu = () => {
    lastFocus = document.activeElement;
    document.body.classList.add('menu-open'); menu.classList.add('open'); head.classList.remove('hide', 'over');
    menuBtn.setAttribute('aria-expanded', 'true'); $('.lbl', menuBtn).textContent = 'Schließen';
    lenis && lenis.stop(); setTimeout(() => $('a', menu).focus(), 350);
  };
  menuBtn.addEventListener('click', () => menu.classList.contains('open') ? closeMenu() : openMenu());
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && menu.classList.contains('open')) { closeMenu(); menuBtn.focus(); }
    if (e.key === 'Tab' && menu.classList.contains('open')) {
      const f = $$('a', menu); const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); menuBtn.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); menuBtn.focus(); }
      else if (!e.shiftKey && document.activeElement === menuBtn) { e.preventDefault(); first.focus(); }
    }
  });
  addEventListener('resize', () => { if (innerWidth > 1020) closeMenu(); });

  // ---------- Wort-für-Wort ----------
  $$('.split').forEach(el => {
    const words = el.textContent.trim().split(/\s+/);
    el.setAttribute('aria-label', words.join(' '));
    el.innerHTML = words.map(w => `<span class="split-line" aria-hidden="true"><span class="w">${esc(w)}</span></span>`).join(' ');
  });

  // ---------- Vorhang ----------
  let seen = false; try { seen = sessionStorage.getItem('ri-intro'); } catch (e) {}
  const intro = $('.curtain.intro');
  let introDelay = 0;
  if (!seen && motion) {
    try { sessionStorage.setItem('ri-intro', '1'); } catch (e) {}
    document.body.classList.add('intro-on');
    gsap.fromTo($('.logo-mark', intro), { y: 18, opacity: 0 }, { y: 0, opacity: 1, duration: .6, ease: 'power3.out' });
    gsap.fromTo($$('.logo-w, .logo-s', intro), { x: -10, opacity: 0 }, { x: 0, opacity: 1, duration: .5, stagger: .1, delay: .25, ease: 'power3.out' });
    gsap.to(intro, { yPercent: -101, duration: .7, ease: 'power3.inOut', delay: 1.05, onComplete: () => document.body.classList.remove('intro-on') });
    introDelay = 1.3;
  }
  document.addEventListener('click', e => {
    const a = e.target.closest('a'); if (!a || !motion) return;
    const href = a.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('tel:') || href.startsWith('mailto:') || a.target === '_blank' || e.metaKey || e.ctrlKey || e.shiftKey || e.defaultPrevented) return;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin || (url.pathname === location.pathname && url.hash && url.search === location.search)) return;
    e.preventDefault(); document.body.classList.add('leaving'); setTimeout(() => location.href = a.href, 420);
  });
  addEventListener('pageshow', e => { if (e.persisted) document.body.classList.remove('leaving'); });
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]'); if (!a) return;
    const t = document.querySelector(a.getAttribute('href')); if (!t) return; e.preventDefault();
    lenis ? lenis.scrollTo(t, { offset: -90, duration: 1.2 }) : t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
  });
  if (location.hash) {
    const t = document.querySelector(location.hash);
    if (t) addEventListener('load', () => setTimeout(() => { hasGsap && ScrollTrigger.refresh(); lenis ? lenis.scrollTo(t, { offset: -90, immediate: true }) : t.scrollIntoView(); head.classList.remove('hide'); }, 80));
  }
  if (hasGsap) gsap.to('#progress', { scaleX: 1, ease: 'none', scrollTrigger: { start: 0, end: 'max', scrub: .3 } });

  // ---------- Magnet, Neigung ----------
  const magnet = b => {
    if (!fine || !motion || b._mag) return; b._mag = 1;
    const xTo = gsap.quickTo(b, 'x', { duration: .4, ease: 'power3' }), yTo = gsap.quickTo(b, 'y', { duration: .4, ease: 'power3' });
    b.addEventListener('pointermove', e => { const r = b.getBoundingClientRect(); const x = e.clientX - r.left, y = e.clientY - r.top; b.style.setProperty('--mx', x + 'px'); b.style.setProperty('--my', y + 'px'); xTo((x - r.width / 2) * .16); yTo((y - r.height / 2) * .25); });
    b.addEventListener('pointerleave', () => { xTo(0); yTo(0); });
  };
  const tilt = c => {
    if (!fine || !motion || c._tilt) return; c._tilt = 1;
    const rx = gsap.quickTo(c, 'rotationX', { duration: .5, ease: 'power3' }), ry = gsap.quickTo(c, 'rotationY', { duration: .5, ease: 'power3' });
    gsap.set(c, { transformPerspective: 900 });
    c.addEventListener('pointermove', e => { const r = c.getBoundingClientRect(); ry(((e.clientX - r.left) / r.width - .5) * 4); rx(-((e.clientY - r.top) / r.height - .5) * 4); });
    c.addEventListener('pointerleave', () => { rx(0); ry(0); });
  };
  $$('.mag').forEach(magnet);

  // ---------- Reveals ----------
  const reveal = () => {
    if (!motion) return;
    $$('.split').forEach(el => {
      if (el._rv) return; el._rv = 1;
      const top = el.closest('.kopf, .hero, .flug');
      gsap.to($$('.w', el), { y: 0, duration: .9, ease: 'power4.out', stagger: .045, delay: top ? introDelay + .1 : 0, scrollTrigger: top ? null : { trigger: el, start: 'top 88%', once: true } });
    });
    $$('.lead, .kopf-foto, .ticks li, .facts div, .qa, .rg-list li, .form, .cols2 > div, .tool-head, .va-grid figure, .contact-list li, .such-list li, .partner li, .hinweis').forEach(el => {
      if (el._rv || el.closest('.hero') || el.closest('.flug') || el.closest('.menu')) return; el._rv = 1;
      el.classList.add('rv');
      const top = el.closest('.kopf');
      gsap.to(el, { opacity: 1, y: 0, duration: .8, ease: 'power3.out', delay: top ? introDelay + .3 : 0, scrollTrigger: top ? null : { trigger: el, start: 'top 92%', once: true } });
    });
  };
  if (hasGsap && !motion) $$('.split .w').forEach(w => w.style.transform = 'none');

  // ---------- Karte erst auf Klick ----------
  $$('[data-map]').forEach(m => $('.map-load', m).addEventListener('click', async () => {
    // Adresse erst nach dem Klick bei OpenStreetMap nachschlagen (Einwilligung durch den Klick)
    let lat = 50.7706, lon = 6.2270; const d = .006;
    try {
      const r = await fetch('https://nominatim.openstreetmap.org/search?format=json&limit=1&q=' + encodeURIComponent(m.dataset.q));
      const j = await r.json(); if (j[0]) { lat = +j[0].lat; lon = +j[0].lon; }
    } catch (e) {}
    m.innerHTML = `<iframe title="Karte: ${esc(m.dataset.q)}" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=${lon - d},${lat - d * .6},${lon + d},${lat + d * .6}&layer=mapnik&marker=${lat},${lon}"></iframe>`;
  }));

  // ---------- Formulare ----------
  $$('form.form').forEach(f => {
    const th = $('[data-thema]', f);
    if (th && params.get('thema') && $(`option[value="${CSS.escape(params.get('thema'))}"]`, th)) th.value = params.get('thema');
    const ta = $('textarea', f); if (ta && params.get('details')) ta.value = params.get('details');
    const obj = params.get('objekt');
    if (obj) {
      $('[name="objekt"]', f).value = obj;
      const p = $('[data-form-objekt]', f); p.hidden = false; p.textContent = 'Anfrage zum Angebot: ' + obj;
      if (th) th.value = 'objekt';
    }
    f.addEventListener('submit', e => {
      const err = $('.form-err', f);
      const bad = $$('[required]', f).filter(i => i.type === 'checkbox' ? !i.checked : !i.value.trim() || (i.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(i.value)));
      $$('[aria-invalid]', f).forEach(i => i.removeAttribute('aria-invalid'));
      if ($('[name="firma_web"]', f).value) { e.preventDefault(); return; }
      if (bad.length) { e.preventDefault(); bad.forEach(i => i.setAttribute('aria-invalid', 'true')); err.hidden = false; err.textContent = 'Bitte Name, eine gültige E-Mail-Adresse und die Einwilligung ergänzen.'; bad[0].focus(); return; }
      if (location.protocol === 'file:' || /github\.io$/.test(location.hostname) || /^(localhost|127\.0\.0\.1)$/.test(location.hostname)) { e.preventDefault(); location.href = 'danke.html'; }
    });
  });

  // ---------- Angebote: Zahl im Menü, Karten, Filter, Exposé ----------
  const RI = window.RI;
  const setCount = n => { $$('[data-live-count]').forEach(el => el.textContent = n); $$('[data-live-count-text]').forEach(el => el.textContent = n + ' aktuell'); };
  if (RI && RI.menge() != null) setCount(RI.menge());
  const kurzOrt = o => o.ortKurz && o.ortKurz !== o.stadt ? `${o.stadt}-${o.ortKurz}` : o.stadt;
  const karte = o => `<article class="oc"><a href="objekt.html?id=${encodeURIComponent(o.id)}">
    <div class="oc-img">${o.bild ? `<img src="${RI.IMG(o.bild, 640)}" srcset="${RI.IMG(o.bild, 640)} 640w, ${RI.IMG(o.bild, 1024)} 1024w" sizes="(max-width: 700px) 100vw, 33vw" alt="${esc(o.titel)}" loading="lazy" width="640" height="480">` : '<span class="oc-noimg">Foto auf Anfrage</span>'}${o.neu ? '<span class="oc-neu">Neu</span>' : ''}</div>
    <div class="oc-body"><p class="oc-ort">${esc(kurzOrt(o))}</p><h3>${esc(o.titel)}</h3>
     <p class="oc-price"><b>${esc(o.preisText || eur(o.preis))}</b> <span>${esc(o.preisLabel || '')}</span></p>
     <p class="oc-data">${[o.wohnflaeche && qm(o.wohnflaeche) + ' Wohnfläche', o.zimmer && o.zimmer + ' Zimmer', o.grundstueck && qm(o.grundstueck) + ' Grundstück'].filter(Boolean).join(' · ')}</p></div></a></article>`;
  const note = r => r.quelle === 'stand'
    ? `Vorschau-Stand vom ${new Date(r.stand).toLocaleDateString('de-DE')} – auf ritterimmobilien.de werden die Angebote bei jedem Aufruf live geladen.`
    : 'Live aus unserem Angebotsbestand.';
  const needs = $('[data-offers]') || $('[data-obj]') || $('[data-offers-sim]');
  const nachLoad = f => document.readyState === 'complete' ? f() : addEventListener('load', f);
  if (RI && needs) nachLoad(() => RI.liste().then(r => {
    setCount(r.angebote.length);
    $$('[data-offers-note]').forEach(el => el.textContent = note(r));
    $$('[data-offers]').forEach(g => {
      if (g.dataset.offers === 'all') return liste(g, r);
      const n = +g.dataset.offers || 6;
      g.innerHTML = r.angebote.slice(0, n).map(karte).join('') || '<p class="muted">Derzeit keine öffentlichen Angebote – fragen Sie uns nach diskreten Objekten.</p>';
      afterCards(g);
    });
    if ($('[data-obj]')) exposeSeite(r);
  }).catch(() => $$('[data-offers], .obj-foto').forEach(g => g.innerHTML = '<p class="muted">Die Angebote können gerade nicht geladen werden. Rufen Sie uns gern an: 02402 3477.</p>')));
  const afterCards = g => {
    $$('.oc', g).forEach(tilt);
    if (motion) gsap.fromTo($$('.oc', g), { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: .6, stagger: .06, ease: 'power3.out', scrollTrigger: { trigger: g, start: 'top 90%', once: true } });
    hasGsap && ScrollTrigger.refresh();
  };

  function liste(g, r) {
    const f = $('[data-filters]'), rc = $('[data-result-count]');
    const orte = [...new Set(r.angebote.map(o => o.stadt).filter(Boolean))].sort();
    $('[data-f-ort]', f).insertAdjacentHTML('beforeend', orte.map(o => `<option>${esc(o)}</option>`).join(''));
    ['art', 'km', 'ort', 'preis', 'sort'].forEach(k => { if (params.get(k)) f.elements[k].value = params.get(k); });
    const render = () => {
      const v = k => f.elements[k].value;
      let a = r.angebote.filter(o => (!v('art') || o.art === v('art')) && (!v('km') || o.km === v('km')) && (!v('ort') || o.stadt === v('ort')) && (!v('preis') || (o.preis || 0) <= +v('preis')));
      const s = v('sort');
      a = a.slice().sort(s === 'preis-auf' ? (x, y) => x.preis - y.preis : s === 'preis-ab' ? (x, y) => y.preis - x.preis : s === 'flaeche' ? (x, y) => (y.wohnflaeche || y.grundstueck || 0) - (x.wohnflaeche || x.grundstueck || 0) : (x, y) => x.reihe - y.reihe);
      g.innerHTML = a.map(karte).join('') || '<div class="empty"><h3>Kein Angebot passt zu diesen Filtern.</h3><p>Viele Objekte vermitteln wir diskret. <a href="kontakt.html?thema=suche">Hinterlassen Sie einen Suchauftrag</a>.</p></div>';
      rc.textContent = a.length === r.angebote.length ? `${a.length} Angebote` : `${a.length} von ${r.angebote.length} Angeboten`;
      afterCards(g);
    };
    f.addEventListener('change', render); render();
  }

  async function exposeSeite(r) {
    const id = (params.get('id') || '').toUpperCase();
    const o = r.angebote.find(x => x.id === id);
    const root = $('[data-obj]');
    const set = (k, h) => { const el = $(`[data-o="${k}"]`, root); if (el) el.innerHTML = h; return el; };
    const sim = r.angebote.filter(x => x.id !== id).slice(0, 3);
    $('[data-offers-sim]').innerHTML = sim.map(karte).join(''); afterCards($('[data-offers-sim]'));
    if (!o) {
      $('.obj-grid', root).innerHTML = `<div class="sold"><p class="kicker">Nicht mehr verfügbar</p><h1>Dieses Angebot ist verkauft oder reserviert.</h1><p class="lead">Unser Bestand ändert sich laufend. Schauen Sie sich die aktuellen Angebote an – oder hinterlassen Sie einen Suchauftrag.</p><div class="btns"><a class="btn" href="angebote.html">Aktuelle Angebote</a><a class="btn ghost" href="kontakt.html?thema=suche">Suchauftrag</a></div></div>`;
      $('.obj-body', root).remove(); return;
    }
    document.title = `${o.titel} – ${o.preisText || ''} | Ritter Immobilien`;
    set('titel', esc(o.titel));
    set('preis', `<b>${esc(o.preisText || eur(o.preis))}</b> <span>${esc(o.preisLabel || '')}</span>`);
    set('keys', [['Ort', kurzOrt(o)], ['Wohnfläche', o.wohnflaeche && qm(o.wohnflaeche)], ['Zimmer', o.zimmer], ['Grundstück', o.grundstueck && qm(o.grundstueck)]].filter(x => x[1]).map(x => `<div><dt>${x[0]}</dt><dd>${esc(x[1])}</dd></div>`).join(''));
    $('.obj-foto', root).innerHTML = o.bild ? `<img src="${RI.IMG(o.bild, 1024)}" srcset="${RI.IMG(o.bild, 800)} 800w, ${RI.IMG(o.bild, 1200)} 1200w, ${RI.IMG(o.bild, 1600)} 1600w" sizes="(max-width: 900px) 100vw, 60vw" alt="${esc(o.titel)}" width="1200" height="900">` : '<div class="obj-ph muted">Fotos auf Anfrage</div>';
    set('anfrage', 'Besichtigung anfragen <span class="ar"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>').href = `kontakt.html?thema=objekt&objekt=${encodeURIComponent(o.titel + ' (' + (o.preisText || '') + ')')}`;
    const ex = await RI.expose(id);
    if (!ex) { set('texte', '<p class="muted">Die Details zu diesem Angebot senden wir Ihnen gern zu.</p>'); return; }
    set('art', esc([ex.kategorie || ex.art, o.km === 'miete' ? 'zur Miete' : 'zum Kauf'].filter(Boolean).join(' ')));
    set('texte', ex.texte.map(([h, t]) => `<h2>${esc(h)}</h2><p>${esc(t).replace(/\n/g, '<br>')}</p>`).join(''));
    set('daten', ex.daten.filter(d => !/online-id|ref\.-nr/i.test(d[0])).map(([l, v]) => `<div><dt>${esc(l)}</dt><dd>${esc(v)}</dd></div>`).join('') + (ex.anschrift ? `<div><dt>Lage</dt><dd>${esc(ex.anschrift)}</dd></div>` : ''));
    set('merkmale', ex.merkmale.map(m => `<li>${esc(m)}</li>`).join('') || '<li class="muted">auf Anfrage</li>');
    const eK = (ex.energie.find(x => /klasse/i.test(x[0])) || [])[1];
    set('energie', (eK ? `<p class="eklasse"><span class="ek ek-${esc(eK.replace('+', 'p'))}">${esc(eK)}</span> Energieeffizienzklasse</p>` : '') +
      `<dl class="obj-data">${ex.energie.map(([l, v]) => `<div><dt>${esc(l.replace(/:$/, ''))}</dt><dd>${esc(v)}</dd></div>`).join('') || (ex.energieTraeger.length ? `<div><dt>Energieträger</dt><dd>${esc(ex.energieTraeger.join(', '))}</dd></div>` : '<div><dt>Energieausweis</dt><dd>auf Anfrage</dd></div>')}</dl>`);
    if (ex.onlineId) set('fotos', `<a href="https://www.immowelt.de/expose/${encodeURIComponent(ex.onlineId)}" target="_blank" rel="noopener">Alle Fotos im Exposé auf immowelt ansehen →</a>`);
    const ld = document.createElement('script'); ld.type = 'application/ld+json';
    ld.textContent = JSON.stringify({ '@context': 'https://schema.org', '@type': 'Offer', name: o.titel, price: o.preis, priceCurrency: 'EUR', image: o.bild ? RI.IMG(o.bild, 1024) : undefined, seller: { '@id': 'https://www.ritterimmobilien.de/#firma' } });
    document.head.appendChild(ld);
    if (o.km === 'kauf' && o.preis && window.RI_NK) window.RI_NK(o.preis);
    hasGsap && ScrollTrigger.refresh();
  }

  window.RIX = { motion, reduce, $, $$, esc, eur, magnet, tilt, introDelay: () => introDelay, lenis: () => lenis };
  const init = () => reveal();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
  addEventListener('load', () => { hasGsap && document.fonts && document.fonts.ready.then(() => ScrollTrigger.refresh()); });
})();
