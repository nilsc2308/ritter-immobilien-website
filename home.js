/* Ritter Immobilien – Startseite: Einstieg, „So verkaufen wir“ (Foto klebt, Kapitel laufen), Ortsteil-Register, Kundenstimmen. */
(() => {
  const X = window.RIX || {};
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const motion = X.motion;

  // ---------- Flug durch das Haus ----------
  const flug = $('.flug');
  const lazy = () => $$('.flug img[data-src]').forEach(im => { im.src = im.dataset.src; if (im.dataset.srcset) im.srcset = im.dataset.srcset; delete im.dataset.src; });
  if (document.readyState === 'complete') lazy(); else addEventListener('load', lazy);
  if (flug && !motion) lazy();
  if (flug && motion) {
    const shots = $$('.fl', flug), blurs = $$('.fl-b', flug), texts = $$('.ft', flug);
    const end = $('.fl-end', flug), flash = $('.fl-flash', flug), route = $$('.route li', flug), routeEl = $('.route', flug);
    const img = el => $('img', el);
    const N = shots.length, STEP = 2.9, DIVE = 1.25;
    const tl = gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: { trigger: flug, start: 'top top', end: 'bottom bottom', scrub: .9 } });
    // Öffnung (Glas, Tür, Fenster) als Rechteck um den Durchflugpunkt; wächst mit dem Zoom der Kamera
    const opening = (el, s) => {
      const fx = +el.dataset.fx, fy = +el.dataset.fy, ow = +el.dataset.ow, oh = +el.dataset.oh;
      const w = ow / 2 * s, h = oh / 2 * s;
      const t = Math.max(0, fy - h), b = Math.max(0, 100 - fy - h), l = Math.max(0, fx - w), r = Math.max(0, 100 - fx - w);
      return `inset(${t.toFixed(2)}% ${r.toFixed(2)}% ${b.toFixed(2)}% ${l.toFixed(2)}% round ${Math.max(0, 14 - s * 2).toFixed(1)}px)`;
    };
    shots.forEach((sh, i) => {
      const S = i * STEP;
      // langsamer Vorwärtsflug mit leichter Drehung (Drohne)
      tl.fromTo(img(sh), { scale: i ? .82 : 1.12, rotation: i % 2 ? .8 : -.8, yPercent: i ? 0 : 4 }, { scale: 1.3, rotation: i % 2 ? -.6 : .6, yPercent: 0, duration: 1.85 + (i ? DIVE : 0), ease: 'power1.inOut' }, i ? S - DIVE : 0);
      // Text: rein nach dem Durchflug, raus vor dem nächsten
      if (i) tl.fromTo(texts[i], { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: .4, ease: 'power3.out' }, S + .15);
      tl.to(texts[i], { autoAlpha: 0, y: -26, duration: .3, ease: 'power2.in' }, S + (i ? 1.45 : 1.0));
      // Durchflug ins nächste Zimmer (oder durch die Haustür nach draußen)
      const D = S + 1.85, next = shots[i + 1] || end, o = { k: 1 };
      const fx = sh.dataset.fx, fy = sh.dataset.fy;
      // Kamera fliegt durch die Öffnung: Foto-Zoom und Öffnung wachsen im selben Takt
      tl.set(next, { autoAlpha: 0, clipPath: opening(sh, 1) }, D)
        .set(flash, { '--fx': fx + '%', '--fy': fy + '%' }, D)
        .to(o, { k: 9, duration: DIVE, ease: 'power3.in', onUpdate: () => {
          const sc = 1.3 * o.k; gsap.set([img(sh), img(blurs[i])], { scale: sc }); next.style.clipPath = opening(sh, o.k);
        } }, D)
        .to(next, { autoAlpha: 1, duration: DIVE * .35, ease: 'power1.out' }, D + DIVE * .05)
        .set(blurs[i], { autoAlpha: 0 }, D)
        .to(blurs[i], { autoAlpha: 1, duration: DIVE * .4 }, D + DIVE * .5)
        .fromTo(flash, { opacity: 0 }, { opacity: i === N - 1 ? .9 : .5, duration: DIVE * .3, ease: 'power2.out' }, D + DIVE * .45)
        .to(flash, { opacity: 0, duration: DIVE * .3, ease: 'power2.in' }, D + DIVE * .8)
        .set(next, { clipPath: 'none' }, D + DIVE)
        .set([sh, blurs[i]], { autoAlpha: 0 }, D + DIVE + .01);
    });
    const E = N * STEP - STEP + 1.85 + 1.25;
    tl.from($$('.fl-end-in > *', end), { opacity: 0, y: 30, duration: .5, stagger: .08, ease: 'power3.out' }, E + .05)
      .to({}, { duration: 1.2 }, E + .6);
    // Flugroute rechts
    const setRoute = () => {
      const t = tl.time(); let k = Math.min(N, Math.floor((t + .5 - 1.85 - 1.25) / STEP) + 1);
      if (t < 1.85 + 1.25) k = 0;
      route.forEach((li, j) => li.classList.toggle('on', j === k));
      routeEl.classList.toggle('dark', k === N);
    };
    tl.eventCallback('onUpdate', setRoute); setRoute();
    gsap.from($$('.ft0 > *'), { opacity: 0, y: 26, duration: 1, stagger: .1, ease: 'power3.out', delay: (X.introDelay ? X.introDelay() : 0) + .15 });
    addEventListener('resize', () => ScrollTrigger.refresh());
  }

  // ---------- So verkaufen wir: Kapitel rechts, Foto links wechselt passend ----------
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
