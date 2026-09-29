/* Ritter Immobilien – Startseite: Einstieg, „So verkaufen wir“ (Foto klebt, Kapitel laufen), Ortsteil-Register, Kundenstimmen. */
(() => {
  const X_ = window.RIX || {};
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const motion = X_.motion;

  // ---------- Einstiegsvideo: Hochformat am Handy, Pause-Knopf, reduzierte Bewegung respektieren ----------
  const v = $('.hero-video');
  if (v) {
    const hoch = matchMedia('(max-aspect-ratio: 4/5)').matches;
    if (hoch) v.src = v.dataset.hoch;
    v.addEventListener('playing', () => v.classList.add('on'), { once: true });
    const btn = $('.hero-pause');
    const setBtn = paused => { btn.setAttribute('aria-pressed', paused ? 'true' : 'false'); btn.setAttribute('aria-label', paused ? 'Video abspielen' : 'Video anhalten'); btn.classList.toggle('paused', paused); };
    const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (still) setBtn(true);
    else { v.preload = 'auto'; v.play().then(() => setBtn(false)).catch(() => setBtn(true)); }
    btn.addEventListener('click', () => { if (v.paused) { v.play(); setBtn(false); } else { v.pause(); setBtn(true); } });
    // außerhalb des Bildschirms anhalten (spart Akku)
    if ('IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(en => { if (btn.classList.contains('paused')) return; en.isIntersecting ? v.play().catch(() => {}) : v.pause(); })).observe(v);
    if (motion) {
      gsap.from(['.hero h1', '.hero .path'], { opacity: 0, y: 26, duration: 1, stagger: .1, ease: 'power3.out', delay: (X_.introDelay ? X_.introDelay() : 0) + .2 });
      gsap.to('.hero-in', { yPercent: -12, opacity: .2, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: .5 } });
    }
  }

  // ---------- So verkaufen wir: Kapitel rechts, Foto links wechselt passend ----------
  addEventListener('load', () => $$('.sv-img img[data-src]').forEach(im => { im.srcset = im.dataset.srcset; im.src = im.dataset.src; }));
  const imgs = $$('.sv-img'), kap = $$('.sv-k');
  const setK = i => { imgs.forEach((f, k) => f.classList.toggle('on', k === i)); kap.forEach((a, k) => a.classList.toggle('on', k === i)); };
  if (kap.length) {
    setK(0);
    if (motion) kap.forEach((a, i) => ScrollTrigger.create({ trigger: a, start: 'top 60%', end: 'bottom 60%', onToggle: s => s.isActive && setK(i) }));
    else kap.forEach(a => a.classList.add('on'));
  }

  // ---------- Ortsteil-Register: Balken wachsen beim Scrollen ----------
  $$('.ot-list li').forEach(li => {
    const bar = $('.ot-bar i', li), v = parseFloat(bar.style.getPropertyValue('--v'));
    if (!motion) return;
    gsap.fromTo(bar, { scaleX: 0 }, { scaleX: v, ease: 'none', scrollTrigger: { trigger: li, start: 'top 92%', end: 'top 60%', scrub: .6 } });
    gsap.fromTo($('.ot-n', li), { x: -24, opacity: 0 }, { x: 0, opacity: 1, ease: 'power2.out', scrollTrigger: { trigger: li, start: 'top 94%', end: 'top 72%', scrub: .6 } });
  });

  // ---------- Kundenstimmen: blättern per Pfeil, Tastatur, Wischen ----------
  const st = $('[data-stimmen]');
  if (st) {
    const items = $$('.st-item', st), n = $('[data-st-n]', st);
    let cur = 0, tl;
    const show = i => {
      i = (i + items.length) % items.length; if (i === cur) return;
      const old = items[cur], nu = items[i]; cur = i; n.textContent = `${i + 1} / ${items.length}`;
      if (!motion) { old.hidden = true; nu.hidden = false; return; }
      tl && tl.progress(1).kill();
      // erst raus, dann rein – Texte nie gleichzeitig sichtbar
      tl = gsap.timeline().to(old, { opacity: 0, y: -10, duration: .18, ease: 'power2.in', onComplete: () => { old.hidden = true; nu.hidden = false; } })
        .fromTo(nu, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .4, ease: 'power3.out' });
    };
    $('.st-prev', st).addEventListener('click', () => show(cur - 1));
    $('.st-next', st).addEventListener('click', () => show(cur + 1));
    st.addEventListener('keydown', e => { if (e.key === 'ArrowRight') show(cur + 1); if (e.key === 'ArrowLeft') show(cur - 1); });
    let sx = null;
    st.addEventListener('touchstart', e => sx = e.touches[0].clientX, { passive: true });
    st.addEventListener('touchend', e => { if (sx == null) return; const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 40) show(cur + (dx < 0 ? 1 : -1)); sx = null; });
  }
})();
