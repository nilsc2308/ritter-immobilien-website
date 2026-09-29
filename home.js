/* Ritter Immobilien – Startseite: Einstieg, „So verkaufen wir“ (Foto klebt, Kapitel laufen), Ortsteil-Register, Kundenstimmen. */
(() => {
  const X_ = window.RIX || {};
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const motion = X_.motion;

  // ---------- Flug durch das Haus ----------
  const flug = $('.flug');
  const lazy = () => $$('.flug img[data-src]').forEach(im => { im.src = im.dataset.src; if (im.dataset.srcset) im.srcset = im.dataset.srcset; delete im.dataset.src; });
  if (document.readyState === 'complete') lazy(); else addEventListener('load', lazy);
  if (flug && !motion) lazy();
  if (flug && motion) {
    const stage = $('.flug-stage', flug), shots = $$('.fl', flug), blurs = $$('.fl-b', flug), subs = $$('.sub', flug);
    const end = $('.fl-end', flug), title = $('.fl-title', flug), bar = $('.fl-time i', flug);
    const img = el => $('img', el);
    const N = shots.length, SEG = 3, X = .9;              // Länge je Raum, Dauer der Überblendung
    const tl = gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: { trigger: flug, start: 'top top', end: 'bottom bottom', scrub: 1.2 } });
    shots.forEach((sh, i) => {
      const S = i * SEG, E = S + SEG;
      // durchgehende Vorwärtsfahrt mit leichter Drehung – nie ein Stillstand
      tl.fromTo(img(sh), { scale: 1, rotation: i % 2 ? .5 : -.5 }, { scale: 1.3, rotation: i % 2 ? -.4 : .4, duration: SEG - X }, i ? S - .1 : 0);
      // Übergang: weiter hineinfliegen, unscharf werden, nächster Raum blendet auf
      const next = shots[i + 1] || end;
      tl.to(img(sh), { scale: 2, duration: X + .1, ease: 'power1.in' }, E - X)
        .fromTo(img(blurs[i]), { scale: 1.3 }, { scale: 2, duration: X + .1, ease: 'power1.in' }, E - X)
        .fromTo(blurs[i], { autoAlpha: 0 }, { autoAlpha: 1, duration: X * .55, ease: 'power1.in' }, E - X)
        .fromTo(next, { autoAlpha: 0 }, { autoAlpha: 1, duration: X * .6, ease: 'power1.out' }, E - X * .55)
        .set([sh, blurs[i]], { autoAlpha: 0 }, E + .1);
      // Untertitel nacheinander, nie gleichzeitig
      const tin = i ? S + .45 : 1.35, tout = E - X - .35;
      tl.fromTo(subs[i], { autoAlpha: 0, y: 12 }, { autoAlpha: 1, y: 0, duration: .35, ease: 'power2.out' }, tin)
        .to(subs[i], { autoAlpha: 0, y: -8, duration: .3, ease: 'power2.in' }, tout);
    });
    tl.to(title, { autoAlpha: 0, y: -20, duration: .5, ease: 'power2.in' }, .6);
    const T = N * SEG;
    tl.from($$('.fl-end-in > *', end), { opacity: 0, y: 26, duration: .5, stagger: .08, ease: 'power3.out' }, T - .2)
      .to({}, { duration: 1.4 }, T + .4);
    tl.fromTo(bar, { scaleX: 0 }, { scaleX: 1, duration: T, ease: 'none' }, 0);
    // leichte Handkamera-Bewegung
    tl.eventCallback('onUpdate', () => { const t = tl.time(); stage.style.setProperty('--dx', (Math.sin(t * 1.9) * 5).toFixed(2) + 'px'); stage.style.setProperty('--dy', (Math.cos(t * 1.4) * 4).toFixed(2) + 'px'); });
    gsap.from(title, { opacity: 0, y: 24, duration: 1.1, ease: 'power3.out', delay: (X_.introDelay ? X_.introDelay() : 0) + .1 });
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
