#!/usr/bin/env python3
# Generator für die Website der Ritter Immobilien e.K. (Stolberg). Aufruf: python3 _build.py
# Die Angebote stecken NICHT im HTML – sie kommen live aus dem immowelt-Homepagemodul (angebote.js).

import json, os, html, datetime, re

ROOT = os.path.dirname(os.path.abspath(__file__))
V = datetime.datetime.now().strftime('%Y%m%d%H%M')
BASE = 'https://www.ritterimmobilien.de/'
FIRMA = 'Ritter Immobilien e.K.'
STR = 'Pfarrer-Gau-Str. 51'
PLZ = '52223'
ORT = 'Stolberg'
TEL = '02402 3477'
TEL_L = '+4924023477'
MOBIL = '0171 7803453'
MOBIL_L = '+491717803453'
FAX = '02402 9020970'
MAIL = 'info@ritterimmobilien.de'
e = html.escape

def load(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return json.load(f)

REFS = load('_quelle/referenzen.json')

# ---------------------------------------------------------------- Bausteine
def img(name, alt, cls='', sizes='100vw', eager=False, w=1600, h=1067):
    load_ = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    dim = GR.get(f'{name}-1600.webp', [w, h])
    return (f'<img class="{cls}" src="img/{name}-1600.webp" srcset="{srcset(name)}" '
            f'sizes="{sizes}" width="{dim[0]}" height="{dim[1]}" alt="{e(alt)}" {load_}>')

LOGO = '''<svg class="logo-svg" viewBox="0 0 250 56" role="img" aria-label="Ritter Immobilien e.K.">
<g class="logo-mark"><path d="M4 22 L24 4 L44 22 V52 H4 Z" fill="none" stroke-width="3.2" stroke-linejoin="round"/><rect x="11" y="26" width="26" height="20" rx="1.5" fill="none" stroke-width="2.4"/><text x="24" y="42" text-anchor="middle" class="logo-ri">Ri</text></g>
<text x="54" y="31" class="logo-w">Ritter Immobilien</text><text x="55" y="48" class="logo-s">seit 1989 · Stolberg</text></svg>'''

ICON = {
 'phone': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z" fill="currentColor"/></svg>',
 'arrow': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 'pin': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="10" r="2.6" fill="currentColor"/></svg>',
 'mail': '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M3.5 6.5 12 13l8.5-6.5" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
}
def arrow(): return '<span class="ar">' + ICON['arrow'] + '</span>'

EIGENTUEMER = [
 ('verkaufen.html', 'Immobilie verkaufen', 'Bewertung, Vermarktung, Besichtigung, Notar – persönlich begleitet'),
 ('kaeufer-warten.html', 'Käufer warten schon', 'Unsere vorgemerkten Suchaufträge – passt Ihr Haus?'),
 ('bewertung.html', 'Immobilie bewerten', 'Kostenlose Einschätzung vor Ort – welches Verfahren passt?'),
 ('vermieten.html', 'Immobilie vermieten', 'Mieterauswahl, Vertrag, Übergabe – mit Kautions-Rechner'),
 ('finanzierung.html', 'Finanzierung', 'Unabhängige Finanzierungsvermittlung und Kaufnebenkosten'),
 ('referenzen.html', 'Referenzen', 'Verkaufte Häuser von Zweifall bis Roetgen'),
 ('kundenstimmen.html', 'Kundenstimmen', 'Was Verkäufer und Vermieter über uns sagen'),
]
EIG_FILES = [x[0] for x in EIGENTUEMER]

def header(p):
    cur = lambda f: ' aria-current="page"' if p['file'] == f or p.get('group') == f else ''
    sub = ''.join(f'<li><a href="{h}"{cur(h)}><b>{e(t)}</b><span>{e(d)}</span></a></li>' for h, t, d in EIGENTUEMER)
    eig_act = ' aria-current="true"' if p['file'] in EIG_FILES else ''
    return f'''<a class="skip" href="#main">Zum Inhalt springen</a>
<div id="progress" aria-hidden="true"></div>
<header id="head" class="{'over' if p.get('over') else ''}">
 <a class="brand" href="index.html" aria-label="Ritter Immobilien – Startseite">{LOGO}</a>
 <nav class="mainnav" aria-label="Hauptmenü"><ul>
  <li><a href="angebote.html"{cur('angebote.html')}>Angebote <span class="count" data-live-count></span></a></li>
  <li class="has-dd"><button type="button" aria-expanded="false" aria-controls="dd-eig"{eig_act}>Verkaufen &amp; Vermieten<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
   <div class="dd" id="dd-eig"><ul>{sub}</ul></div></li>
  <li><a href="hausverwaltung.html"{cur('hausverwaltung.html')}>Hausverwaltung</a></li>
  <li><a href="ueber-uns.html"{cur('ueber-uns.html')}>Über uns</a></li>
  <li><a href="kontakt.html"{cur('kontakt.html')}>Kontakt</a></li>
 </ul></nav>
 <div class="head-r">
  <a class="head-tel" href="tel:{TEL_L}">{ICON['phone']}<span>{TEL}</span></a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu"><span class="bars" aria-hidden="true"><i></i><i></i></span><span class="lbl">Menü</span></button>
 </div>
</header>
<div id="menu" class="menu" aria-label="Menü">
 <ul class="menu-main">
  <li><a href="angebote.html">Angebote <small data-live-count-text></small></a></li>
  <li><a href="verkaufen.html">Verkaufen</a></li>
  {''.join(f'<li class="sub"><a href="{h}">{e(t)}</a></li>' for h, t, d in EIGENTUEMER[1:])}
  <li><a href="hausverwaltung.html">Hausverwaltung</a></li>
  <li><a href="ueber-uns.html">Über uns</a></li>
  <li><a href="kontakt.html">Kontakt</a></li>
 </ul>
 <div class="menu-foot">
  <a href="tel:{TEL_L}">{ICON['phone']} {TEL}</a>
  <a href="mailto:{MAIL}">{ICON['mail']} {MAIL}</a>
  <p>{STR}, {PLZ} {ORT} · Termine nach Vereinbarung</p>
 </div>
</div>'''

def footer(p):
    return f'''<footer class="foot">
 <div class="wrap foot-grid">
  <div class="foot-brand">{LOGO}
   <p>Familiengeführtes, unabhängiges Maklerbüro in der StädteRegion Aachen – seit 1989.<br><em>Wo Träume ein Zuhause finden.</em></p></div>
  <div><h2>Büro</h2><address>{FIRMA}<br>{STR}<br>{PLZ} {ORT}</address><p>Termine nach Vereinbarung</p></div>
  <div><h2>Kontakt</h2><ul>
   <li><a href="tel:{TEL_L}">Telefon {TEL}</a></li><li><a href="tel:{MOBIL_L}">Mobil {MOBIL}</a></li>
   <li><a href="mailto:{MAIL}">{MAIL}</a></li></ul></div>
  <div><h2>Seiten</h2><ul>
   <li><a href="angebote.html">Angebote</a></li><li><a href="verkaufen.html">Verkaufen</a></li><li><a href="vermieten.html">Vermieten</a></li>
   <li><a href="hausverwaltung.html">Hausverwaltung</a></li><li><a href="ratgeber.html">Ratgeber</a></li><li><a href="faq.html">Häufige Fragen</a></li>
   <li><a href="ferienhaus-foehr.html">Ferienhaus auf Föhr</a></li></ul></div>
 </div>
 <div class="wrap foot-bottom"><span>© {datetime.date.today().year} {FIRMA}</span>
  <span><a href="impressum.html">Impressum</a> <a href="datenschutz.html">Datenschutz</a> <a href="agb.html">AGB</a> <a href="widerruf.html">Widerrufsbelehrung</a></span></div>
</footer>
<a class="sticky-cta" href="kontakt.html?thema=bewertung">Kostenlose Bewertung anfragen</a>'''

LD_BIZ = {
 "@context": "https://schema.org", "@type": "RealEstateAgent", "@id": BASE + "#firma",
 "name": FIRMA, "url": BASE, "telephone": "+49 2402 3477", "faxNumber": "+49 2402 9020970", "email": MAIL,
 "image": BASE + "img/flug-aussen-1600.webp", "logo": BASE + "apple-touch-icon.png", "foundingDate": "1989",
 "founder": {"@type": "Person", "name": "Rudolf Ritter"},
 "address": {"@type": "PostalAddress", "streetAddress": STR, "postalCode": PLZ, "addressLocality": ORT, "addressRegion": "NRW", "addressCountry": "DE"},
 "areaServed": ["Stolberg", "Eschweiler", "Aachen", "Würselen", "Roetgen", "Simmerath", "Jülich", "Düren"],
}

def head(p):
    lds = [LD_BIZ] + p.get('ld', [])
    ld = ''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in lds)
    url = BASE + ('' if p['file'] == 'index.html' else p['file'])
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p['title'])}</title>
<meta name="description" content="{e(p['desc'])}">
{'<meta name="robots" content="noindex">' if p.get('noindex') else ''}
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:locale" content="de_DE"><meta property="og:site_name" content="Ritter Immobilien">
<meta property="og:title" content="{e(p['title'])}"><meta property="og:description" content="{e(p['desc'])}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b2256">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="fonts/schibsted-grotesk-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
{p.get('preload', '')}
<link rel="stylesheet" href="styles.css?v={V}">
{ld}
</head>
<body class="{p.get('body', '')}" data-page="{p['file'].replace('.html', '')}">
<div class="curtain intro" aria-hidden="true"><div class="intro-in">{LOGO}</div></div>
<div class="curtain leave" aria-hidden="true"></div>
'''

def scripts(p):
    s = ['<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js" defer></script>',
         '<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js" defer></script>',
         '<script src="https://cdn.jsdelivr.net/npm/lenis@1.3.11/dist/lenis.min.js" defer></script>',
         f'<script src="angebote.js?v={V}" defer></script>',
         f'<script src="main.js?v={V}" defer></script>']
    for x in p.get('js', []):
        s.append(f'<script src="{x}?v={V}" defer></script>')
    return '\n'.join(s)

PAGES = []
def page(p, body):
    out = head(p) + header(p) + f'\n<main id="main">\n{body}\n</main>\n' + footer(p) + '\n' + scripts(p) + '\n</body>\n</html>\n'
    with open(os.path.join(ROOT, p['file']), 'w', encoding='utf-8') as f:
        f.write(out)
    PAGES.append(p)

# ---------------------------------------------------------------- Unterseiten-Kopf „Hausschild“
def schild(title, lead, photo, alt, kicker=''):
    crumb = f'<p class="crumb"><a href="index.html">Ritter Immobilien</a><span>/</span>{e(kicker)}</p>' if kicker else ''
    return f'''<section class="kopf">
 <div class="wrap">
  {crumb}
  <div class="kopf-row">
   <h1 class="split">{e(title)}</h1>
   <p class="lead">{lead}</p>
  </div>
 </div>
 <figure class="kopf-foto">{img(photo, alt, '', '100vw', True)}</figure>
</section>'''

def cta(title='Sprechen wir über Ihre Immobilie.', text='Ein unverbindliches Gespräch, gern bei Ihnen vor Ort. Wir melden uns schnellstmöglich zurück.', thema=''):
    q = f'?thema={thema}' if thema else ''
    return f'''<section class="cta-end">
 <div class="wrap cta-in">
  <h2 class="split">{e(title)}</h2>
  <p>{e(text)}</p>
  <div class="btns">
   <a class="btn light mag" href="kontakt.html{q}">Anfrage senden</a>
   <a class="btn ghost light mag" href="tel:{TEL_L}">{ICON['phone']} {TEL}</a>
  </div>
 </div>
</section>'''

THEMEN = [('verkauf', 'Ich möchte verkaufen'), ('bewertung', 'Kostenlose Bewertung'), ('vermietung', 'Ich möchte vermieten'),
          ('objekt', 'Frage zu einem Angebot'), ('suche', 'Suchauftrag: ich suche eine Immobilie'), ('finanzierung', 'Finanzierung'),
          ('hausverwaltung', 'Hausverwaltung'), ('foehr', 'Ferienhaus auf Föhr'), ('sonstiges', 'Sonstiges')]

def form(thema_default='', titel='Ihre Nachricht'):
    opts = ''.join(f'<option value="{v}"{" selected" if v == thema_default else ""}>{t}</option>' for v, t in THEMEN)
    return f'''<form class="form" name="anfrage" method="POST" action="danke.html" data-netlify="true" netlify-honeypot="firma_web" novalidate>
  <input type="hidden" name="form-name" value="anfrage">
  <input type="hidden" name="objekt" value="">
  <p class="hp"><label>Bitte leer lassen <input name="firma_web" tabindex="-1" autocomplete="off"></label></p>
  <h3>{e(titel)}</h3>
  <label>Anliegen<select name="thema" data-thema>{opts}</select></label>
  <p class="form-objekt" data-form-objekt hidden></p>
  <div class="row2"><label>Name*<input name="name" autocomplete="name" required></label><label>Telefon<input name="telefon" type="tel" autocomplete="tel"></label></div>
  <label>E-Mail*<input name="email" type="email" autocomplete="email" required></label>
  <label>Nachricht<textarea name="nachricht" rows="4" placeholder="Zum Beispiel: Einfamilienhaus in Stolberg-Breinig, Baujahr 1975, Verkauf im Frühjahr geplant."></textarea></label>
  <label class="check"><input type="checkbox" name="datenschutz" required> <span>Ich bin einverstanden, dass meine Angaben zur Bearbeitung der Anfrage gespeichert werden (<a href="datenschutz.html">Datenschutz</a>).*</span></label>
  <p class="form-err" role="alert" hidden></p>
  <button class="btn mag" type="submit">Absenden</button>
 </form>'''

# ---------------------------------------------------------------- Suchaufträge (Stand der alten Seite 12.09.2025)
SUCH = [
 {'text': 'Für eine sympathische Familie (Bonität geprüft) suchen wir ein gepflegtes, geräumiges Einfamilienhaus im Raum Stolberg oder Eschweiler.', 'typ': ['efh'], 'orte': ['stolberg', 'eschweiler'], 'max': 350000, 'wer': 'Familie'},
 {'text': 'Für ein Beamtenehepaar suchen wir ein Haus in etwas ruhiger Lage – eine Garage ist nicht unbedingt nötig.', 'typ': ['efh', 'zfh', 'dhh'], 'orte': ['alle'], 'max': None, 'wer': 'Ehepaar'},
 {'text': 'Für bonitätsgeprüfte Anleger suchen wir ständig gepflegte Mehrfamilienhäuser. Standort egal.', 'typ': ['mfh'], 'orte': ['alle'], 'max': None, 'wer': 'Anleger'},
 {'text': 'Freistehendes Einfamilienhaus oder gepflegte Doppelhaushälfte mit Garten und Garage in Randlage Aachen (Eschweiler, Stolberg, Aachen) schnellstmöglich zu kaufen gesucht.', 'typ': ['efh', 'dhh'], 'orte': ['stolberg', 'eschweiler', 'aachen'], 'max': None, 'wer': 'Käufer'},
 {'text': 'Für mehrere seriöse Familien suchen wir gepflegte Ein- oder Zweifamilienhäuser, freistehend oder angebaut, in Breinig, Büsbach, Kornelimünster, Mausbach, Vicht oder Zweifall.', 'typ': ['efh', 'zfh', 'dhh'], 'orte': ['stolberg', 'aachen'], 'max': None, 'wer': 'Familien'},
 {'text': 'Für einen Junggesellen mit Erspartem suchen wir ein gemütliches Einfamilienhaus mit Garten oder Wiese bis ca. 150.000 €.', 'typ': ['efh'], 'orte': ['alle'], 'max': 150000, 'wer': 'Einzelperson'},
 {'text': 'Handwerker suchen über uns ältere, renovierungsbedürftige Häuser mit Garten im Großraum Aachen – der Standort spielt keine Rolle.', 'typ': ['efh', 'zfh', 'dhh', 'mfh'], 'orte': ['alle'], 'max': None, 'wer': 'Handwerker', 'zustand': 'renovierung'},
 {'text': 'Für eine junge Familie suchen wir ein älteres, renovierungsbedürftiges Haus mit Garten oder Hof/Terrasse im Raum Stolberg/Eschweiler bis Roetgen.', 'typ': ['efh', 'zfh', 'dhh'], 'orte': ['stolberg', 'eschweiler', 'roetgen'], 'max': None, 'wer': 'Familie', 'zustand': 'renovierung'},
 {'text': 'Für naturverbundene Familien suchen wir im Raum Breinig ein Ein- bis Zweifamilienhaus mit Garage, Kaufpreis bis ca. 600.000 €.', 'typ': ['efh', 'zfh'], 'orte': ['stolberg'], 'max': 600000, 'wer': 'Familien'},
 {'text': 'Für seriöse Anleger suchen wir ständig Garagen und Garagenhöfe – der Standort ist egal.', 'typ': ['garage'], 'orte': ['alle'], 'max': None, 'wer': 'Anleger'},
]

def matcher(ident='abgleich'):
    typen = [('efh', 'ein Einfamilienhaus'), ('dhh', 'eine Doppelhaushälfte'), ('zfh', 'ein Zweifamilienhaus'), ('mfh', 'ein Mehrfamilienhaus'), ('etw', 'eine Eigentumswohnung'), ('grund', 'ein Grundstück'), ('garage', 'Garagen')]
    orte = [('stolberg', 'Stolberg'), ('eschweiler', 'Eschweiler'), ('aachen', 'Aachen'), ('roetgen', 'Roetgen und der Eifel'), ('andere', 'einem anderen Ort')]
    preise = [('150000', 'bis 150.000 €'), ('350000', 'bis 350.000 €'), ('600000', 'bis 600.000 €'), ('999999999', 'über 600.000 €')]
    sel = lambda name, opts, v: f'<select data-m="{name}" aria-label="{name}">' + ''.join(f'<option value="{k}"{" selected" if k == v else ""}>{t}</option>' for k, t in opts) + '</select>'
    return f'''<div class="matcher" id="{ident}" data-matcher>
  <p class="m-satz">Ich möchte {sel('typ', typen, 'efh')} in {sel('ort', orte, 'stolberg')} verkaufen, meine Preisvorstellung liegt {sel('preis', preise, '350000')}.</p>
  <label class="m-reno"><input type="checkbox" data-m-reno> Die Immobilie ist renovierungsbedürftig</label>
  <div class="m-out" aria-live="polite">
   <p class="m-num"><b data-m-n>0</b> <span data-m-label>vorgemerkte Suchaufträge passen</span></p>
   <ul class="m-list" data-m-list></ul>
   <p class="m-foot"><a class="btn" data-m-cta href="kontakt.html?thema=verkauf">Verkauf besprechen</a><span class="muted small">Auszug unserer Suchaufträge, Stand 12.09.2025. Viele Anfragen erreichen uns nur telefonisch.</span></p>
  </div>
 </div>'''

def suchjs():
    with open(os.path.join(ROOT, 'data', 'suchauftraege.js'), 'w', encoding='utf-8') as f:
        f.write('window.RI_SUCH=' + json.dumps({'stand': '2025-09-12', 'auftraege': SUCH}, ensure_ascii=False) + ';\n')

# ---------------------------------------------------------------- Kundenstimmen (von der alten Seite, wörtlich gekürzt)
STIMMEN = [
 ('Stolberg', 'Anfangs wollte ich meine Wohnung ohne Makler verkaufen und bin im Nachhinein sehr froh, dass ich die Ritters hatte. Abgesehen von meiner Anwesenheit beim Notar brauchte ich nichts zu machen.', 'T. L.'),
 ('Stolberg-Schevenhütte', 'Besonders angenehm war, dass alle Besichtigungstermine durchgeführt werden konnten, während wir selbst geurlaubt haben – als wir wiederkamen, waren bereits mehrere ernsthafte Interessenten gefunden.', 'Eheleute Beek'),
 ('Stolberg', 'Wir als Erbengemeinschaft fühlten uns von Herrn Ritter von Anfang an sehr kompetent beraten. Der erzielte Verkaufspreis hat unsere Erwartungen übertroffen. Eine 1A Betreuung bis hin zum Notartermin.', 'Franz Gillessen'),
 ('Stolberg-Donnerberg', 'Wir möchten uns ganz herzlich für Herrn Ritters Engagement (auch der Einsatz der Rosenschere), das sofortige Reagieren und immer Erreichbar-Sein bedanken.', 'Jürgen Burzlaff'),
 ('Stolberg-Münsterbusch', 'Frau Ritter hat sich persönlich dafür eingesetzt, dass wir am Ende den passenden Mieter gefunden haben.', 'H. und M. Delasauce'),
 ('Eschweiler-Bergrath', 'Er ist freundlich, zuvorkommend, hilfsbereit, fast immer erreichbar (selbst im Urlaub) und kümmert sich auch hilfreich um viele Dinge im Umfeld des reinen Immobilienverkaufs.', 'Dr. Horst Martin Stubenrauch'),
 ('Stolberg-Liester', 'Sehr gute Marktkenntnis, sehr realistische Einschätzungen, großer Erfahrungsschatz. Ausgesprochen gute Einschätzung und Vorauswahl von qualifizierten Kaufinteressenten.', 'Dr. Erwin Königs'),
 ('Stolberg-Zweifall', 'Von Anfang bis Ende kompetente Beratung und Betreuung. Sehr professionelle Bearbeitung. Man fühlte sich nie alleine gelassen.', 'B. F.'),
 ('Aachen-Hahn', 'Der Verkauf unserer Immobilie wurde, trotz bestehender Probleme, zu unserer vollsten Zufriedenheit abgewickelt.', 'Bernd K.'),
 ('Stolberg', 'Sein Umgang mit unserer Immobilie war so gewissenhaft, als sei es seine eigene gewesen. Für uns war der Verkauf ein angenehmes „Rund-um-Sorglos-Paket“.', 'Hillemanns-Förster'),
 ('Stolberg-Zweifall', 'Von den Besichtigungsterminen bis zum Notartermin war alles sehr gut organisiert. Ein wirklich gutes Team.', 'Simone & Axel Löhrer'),
 ('Hamich', 'Herr Ritter hat uns mit seiner ruhigen, einfühlsamen, kompetenten Art überzeugt. Er hat unsere Immobilie sehr gut in Szene gesetzt und optimal vermarktet.', 'Rau Eich'),
 ('Stolberg-Mausbach', 'Herr Ritter war sehr engagiert, hilfsbereit, transparent in seinem Vorgehen und flexibel in der Termingestaltung. Unser Haus hat er in relativ kurzer Zeit verkauft.', 'Hedi Müllejans'),
 ('Stolberg-Büsbach', 'Wir wurden stets über den aktuellen Status informiert und die weiteren Schritte wurden abgestimmt. Von Anfang bis zum Ende hat alles wirklich sehr gut geklappt.', 'C. C.'),
 ('Stolberg-Werth', 'Herr Ritter hat auf jedes Telefonat reagiert, das für mich sehr wichtig war. Gute Sach- und Fachkenntnisse, gute Zusammenarbeit!', 'Peter Bremen'),
 ('Alsdorf', 'Herr Ritter hat einen ausgezeichneten Job gemacht und konnte das Haus innerhalb kurzer Zeit verkaufen. Er ist erfahren, setzt sich ein und stand mit Rat und Tat zur Verfügung.', 'Greta Klee'),
]

def stimmen_karussell():
    items = ''.join(f'<figure class="st-item" data-i="{i}"{"" if i == 0 else " hidden"}><blockquote>„{e(t)}“</blockquote><figcaption><b>{e(n)}</b> · {e(o)}</figcaption></figure>' for i, (o, t, n) in enumerate(STIMMEN[:10]))
    return f'''<div class="stimmen" data-stimmen>
   <div class="st-stage">{items}</div>
   <div class="st-nav"><button type="button" class="st-prev" aria-label="Vorherige Stimme">‹</button><span data-st-n>1 / 10</span><button type="button" class="st-next" aria-label="Nächste Stimme">›</button><a href="kundenstimmen.html">Alle Kundenstimmen</a></div>
  </div>'''

# ---------------------------------------------------------------- Startseite
KAPITEL = [
 ('glas-diele', 'Helle Diele mit Treppe und Blick auf die Haustür', 'Bewertung vor Ort', 'Am Anfang steht immer die exakte, marktgerechte Bewertung – bei Ihnen zu Hause, nicht per Online-Rechner. Lage, Zustand, Ausstattung und Baujahr sieht nur, wer vor Ort ist.'),
 ('wohnen-holz', 'Helles Wohnzimmer mit Holzdecke und Kaminofen', 'Individuelle Vermarktung', 'Jede Immobilie bekommt ihr eigenes Verkaufskonzept: Wir arbeiten die Besonderheiten heraus und präsentieren sie so, dass die richtigen Käufer anfragen. Auf Wunsch diskret, ganz ohne öffentliche Anzeige.'),
 ('essplatz', 'Essplatz mit Bücherwand in einem verkauften Haus', 'Keine Sammelbesichtigungen', 'Open-House-Termine machen wir nicht. Jede Besichtigung ist persönlich begleitet – niemand wird allein durch Ihr Haus geschickt.'),
 ('garten-eifel', 'Großer Garten mit Blick auf bewaldete Hügel der Eifel', 'Vorgemerkte, geprüfte Käufer', 'Viele unserer Kaufinteressenten warten schon auf das passende Haus. Ihre Bonität prüfen wir vorab – so ist die Kaufpreiszahlung abgesichert.'),
 ('glas-wohnen', 'Heller Wohn- und Essbereich mit Parkett und Gartentüren', 'Bis zum Notar – und danach', 'Wir begleiten Sie bis zum Notartermin und sind auch nach der Vertragsunterzeichnung für Sie da. Auf Wunsch kümmern wir uns um Haushaltsauflösungen, zum Beispiel nach einem Erbe.'),
]

def ortsteile():
    from collections import Counter
    c = Counter(r['ort'] for r in REFS)
    top = c.most_common()
    mx = top[0][1]
    rows = ''.join(f'<li><span class="ot-n">{e(o)}</span><span class="ot-bar" aria-hidden="true"><i style="--v:{n / mx:.3f}"></i></span><span class="ot-c">{n}</span></li>' for o, n in top if n >= 2)
    rest = sum(n for o, n in top if n < 2)
    return rows, len(REFS), rest

GR = json.load(open(os.path.join(ROOT, '_quelle', 'bildgroessen.json')))
def srcset(name):
    out = []
    for w in (800, 1600, 2400):
        f = f'{name}-{w}.webp'
        if f in GR and not any(GR[f][0] == GR.get(f'{name}-{x}.webp', [0])[0] for x in (800, 1600) if x < w):
            out.append(f'img/{f} {GR[f][0]}w')
    return ', '.join(out)

def flug():
    return f'''<section class="hero" aria-labelledby="hero-h">
 <picture class="hero-poster"><source media="(max-aspect-ratio: 4/5)" srcset="video/flug-hoch-poster.webp"><img src="video/flug-quer-poster.webp" alt="" width="1920" height="1080" fetchpriority="high"></picture>
 <video class="hero-video" muted loop playsinline preload="metadata"
  data-quer="video/flug-quer.mp4" data-hoch="video/flug-hoch.mp4"
  aria-label="Kamerafahrt durch ein von Ritter Immobilien verkauftes Bruchsteinhaus in Stolberg: Hofweg, Diele, Wohnzimmer, Garten">
  <source src="video/flug-quer.mp4" type="video/mp4">
 </video>
 <div class="hero-scrim" aria-hidden="true"></div>
 <div class="wrap hero-in">
  <h1 id="hero-h">Ritter Immobilien<span>Stolberg, seit 1989. Verkauf, Vermietung, Hausverwaltung.</span></h1>
  <div class="paths">
   <a class="path" href="angebote.html"><span class="p-k">Ich suche ein Zuhause</span><span class="p-t"><b data-live-count>9</b> aktuelle Angebote</span></a>
   <a class="path" href="kaeufer-warten.html"><span class="p-k">Ich möchte verkaufen</span><span class="p-t"><b>{len(SUCH)}</b> Suchaufträge warten</span></a>
  </div>
 </div>
 <button class="hero-pause" type="button" aria-pressed="false" aria-label="Video anhalten"><span aria-hidden="true"></span></button>
 <p class="hero-note">Video: ein von uns verkauftes Bruchsteinhaus in Stolberg</p>
</section>'''

def home():
    rows, total, rest = ortsteile()
    kap_img = ''.join(f'<figure class="sv-img{" on" if i == 0 else ""}" data-i="{i}">' + (img(ph, alt, '', '(max-width: 900px) 100vw, 45vw') if i == 0 else img(ph, alt, '', '(max-width: 900px) 100vw, 45vw').replace(' src=', ' data-src=').replace(' srcset=', ' data-srcset=')) + '</figure>' for i, (ph, alt, t, d) in enumerate(KAPITEL))
    kap_txt = ''.join(f'<article class="sv-k" data-i="{i}"><h3>{e(t)}</h3><p>{e(d)}</p></article>' for i, (ph, alt, t, d) in enumerate(KAPITEL))
    body = flug() + f'''
<section class="offers" id="angebote" aria-labelledby="off-h">
 <div class="wrap">
  <div class="sec-head row"><div><h2 id="off-h" class="split">Gerade zu haben.</h2></div>
   <a class="linkbtn" href="angebote.html">Alle <span data-live-count></span> Angebote</a></div>
  <div class="grid-offers" data-offers="6"><p class="muted">Angebote werden geladen …</p></div>
  <p class="muted small offers-note" data-offers-note></p>
 </div>
</section>

<section class="wait" id="kaeufer" aria-labelledby="wait-h">
 <div class="wrap">
  <div class="sec-head"><h2 id="wait-h" class="split">Käufer warten schon.</h2>
   <p class="lead">Für viele Familien, Paare und Anleger suchen wir bereits. Sagen Sie uns, was Sie verkaufen möchten – und sehen Sie, welche Suchaufträge passen.</p></div>
  {matcher()}
 </div>
</section>

<section class="story" aria-labelledby="story-h">
 <div class="wrap">
  <div class="sec-head"><h2 id="story-h" class="split">Persönlich, von der Bewertung bis zum Notar.</h2></div>
  <div class="sv-grid">
   <div class="sv-sticky">{kap_img}</div>
   <div class="sv-text">{kap_txt}<a class="btn mag" href="verkaufen.html">Mehr zum Verkauf</a></div>
  </div>
 </div>
</section>

<section class="orte dark" aria-labelledby="orte-h">
 <div class="wrap orte-grid">
  <div>
   <h2 id="orte-h" class="split">Zuhause in jedem Ortsteil.</h2>
   <p class="lead">{total} vermittelte Häuser und Wohnungen stehen allein auf unserer Referenzliste – die meisten in Stolberg, von Breinig bis Zweifall. Dazu {rest} weitere in Alsdorf, Inden, Simmerath und anderswo.</p>
   <a class="btn light mag" href="referenzen.html">Alle Referenzen</a>
  </div>
  <ul class="ot-list">{rows}</ul>
 </div>
</section>

<section class="voices" aria-labelledby="voices-h">
 <div class="wrap">
  <div class="sec-head"><h2 id="voices-h" class="split">Was Verkäufer sagen.</h2></div>
  {stimmen_karussell()}
 </div>
</section>

<section class="team-sec" aria-labelledby="team-h">
 <div class="wrap team-grid">
  <div class="team-l">
   <figure class="team-foto">{img('team', 'Rudolf Ritter und seine Tochter Maike Steyns', '', '(max-width: 900px) 100vw, 45vw')}</figure>
   <h2 id="team-h" class="split">Vater und Tochter.</h2>
   <p><b>Rudolf Ritter</b>, Immobilienmakler – Gründer und Inhaber, seit über 35 Jahren am Markt in der StädteRegion Aachen.<br><b>Maike Steyns</b>, Immobilienfachwirtin (IHK) und Immobilienmaklerin (IHK) – seit 2017 im Familienbetrieb, zuständig für Verkauf und Vermietung von Wohnimmobilien.</p>
   <p class="team-kontakt"><a href="tel:{TEL_L}">{ICON['phone']} {TEL}</a><a href="mailto:{MAIL}">{ICON['mail']} {MAIL}</a></p>
  </div>
  <div class="team-r">{form('bewertung', 'Kostenlose Bewertung anfragen')}</div>
 </div>
</section>'''
    page({'file': 'index.html', 'title': 'Ritter Immobilien – Immobilienmakler in Stolberg seit 1989', 'desc': 'Familiengeführter Immobilienmakler in Stolberg: Verkauf, Vermietung, Bewertung und Hausverwaltung in Stolberg, Eschweiler, Aachen und der Eifel.',
          'over': True, 'body': 'home', 'js': ['tools.js', 'home.js'],
          'preload': ''}, body)

# ---------------------------------------------------------------- Angebote + Exposé
def angebote():
    body = schild('Aktuelle Angebote', 'Häuser, Wohnungen und Grundstücke, die wir gerade vermitteln – direkt aus unserem Angebotsbestand, immer aktuell.', 'haus-garten', 'Freistehendes Haus mit Garten', 'Kaufen & Mieten') + f'''
<section class="stock" id="werkzeug">
 <div class="wrap">
  <form class="filters" data-filters role="search" aria-label="Angebote filtern" onsubmit="return false">
   <label>Art<select name="art"><option value="">Alle</option><option value="haus">Häuser</option><option value="wohnung">Wohnungen</option><option value="grund">Grundstücke</option><option value="sonst">Sonstiges</option></select></label>
   <label>Kaufen / Mieten<select name="km"><option value="">Beides</option><option value="kauf">Kaufen</option><option value="miete">Mieten</option></select></label>
   <label>Ort<select name="ort" data-f-ort><option value="">Alle Orte</option></select></label>
   <label>Preis bis<select name="preis"><option value="">egal</option><option value="100000">100.000 €</option><option value="250000">250.000 €</option><option value="400000">400.000 €</option><option value="600000">600.000 €</option></select></label>
   <label>Sortierung<select name="sort"><option value="neu">Neueste zuerst</option><option value="preis-auf">Preis aufsteigend</option><option value="preis-ab">Preis absteigend</option><option value="flaeche">Größte Fläche</option></select></label>
  </form>
  <p class="stock-meta" aria-live="polite"><b data-result-count>Angebote werden geladen …</b> <span class="muted" data-offers-note></span></p>
  <div class="grid-offers" data-offers="all"></div>
  <aside class="hinweis">
   <h2>Nicht alles steht online.</h2>
   <p>Auf Wunsch einiger Eigentümer veröffentlichen wir nicht jedes Angebot – und manche nur ohne Fotos. Bei besonderen Immobilien legen unsere Kunden Wert auf eine diskrete Vermittlung ohne öffentliche Werbung. Sagen Sie uns, was Sie suchen: Wir nehmen Sie in unsere Kartei auf und melden uns, sobald etwas passt.</p>
   <a class="btn mag" href="kontakt.html?thema=suche">Suchauftrag hinterlassen</a>
  </aside>
 </div>
</section>''' + cta('Ihr Traumhaus ist nicht dabei?', 'Viele Objekte vermitteln wir, bevor sie online stehen. Hinterlassen Sie uns Ihren Suchauftrag.', 'suche')
    page({'file': 'angebote.html', 'title': 'Immobilien in Stolberg & Umgebung kaufen | Ritter Immobilien', 'desc': 'Aktuelle Häuser, Wohnungen und Grundstücke von Ritter Immobilien in Stolberg, Eschweiler und Aachen – immer aktuell aus unserem Angebotsbestand.'}, body)

def objekt():
    body = f'''<section class="obj" data-obj>
 <div class="wrap"><a class="back" href="angebote.html">← Alle Angebote</a></div>
 <div class="wrap obj-grid">
  <div class="obj-media">
   <figure class="obj-foto"><div class="obj-ph muted">Exposé wird geladen …</div></figure>
   <p class="obj-more" data-o="fotos"></p>
  </div>
  <aside class="obj-side">
   <div class="obj-card">
    <p class="kicker" data-o="art">&nbsp;</p>
    <h1 data-o="titel">Exposé</h1>
    <p class="obj-price" data-o="preis"></p>
    <dl class="obj-keys" data-o="keys"></dl>
    <div class="btns col"><a class="btn mag" data-o="anfrage" href="kontakt.html?thema=objekt">Besichtigung anfragen</a><a class="btn ghost mag" href="tel:{TEL_L}">{ICON['phone']} {TEL}</a></div>
   </div>
  </aside>
 </div>
 <div class="wrap obj-body">
  <div class="obj-main">
   <div data-o="texte"></div>
   <div class="obj-cols"><div><h2>Objektdaten</h2><dl class="obj-data" data-o="daten"></dl></div><div><h2>Ausstattung</h2><ul class="obj-feat" data-o="merkmale"></ul><h2>Energie</h2><div data-o="energie"></div></div></div>
  </div>
  <aside class="obj-calc" id="werkzeug" data-nk hidden>
   <h2>Kaufnebenkosten</h2>
   <p class="muted small">Für dieses Objekt in NRW gerechnet – Richtwerte.</p>
   <dl data-nk-out></dl>
   <fieldset><legend>Maklerprovision Käufer</legend><div class="seg" data-nk-prov><button type="button" data-v="0">keine</button><button type="button" data-v="2.38">2,38 %</button><button type="button" data-v="3.57" aria-pressed="true">3,57 %</button></div></fieldset>
   <p class="muted small">Provision laut Exposé bzw. Absprache; bei Einfamilienhäusern und Wohnungen teilen Käufer und Verkäufer sie seit 2020 in der Regel hälftig (§ 656c BGB). <a href="finanzierung.html#werkzeug">Mehr zur Finanzierung</a></p>
  </aside>
 </div>
 <div class="wrap"><p class="stock-note muted small">Unsere Angebote sind unverbindlich und freibleibend, Zwischenverkauf vorbehalten. Alle Angaben stammen vom Verkäufer bzw. Vermieter und werden ohne Gewähr weitergegeben (siehe <a href="agb.html">AGB</a>).</p></div>
 <div class="wrap obj-sim"><h2>Weitere Angebote</h2><div class="grid-offers small" data-offers-sim></div></div>
</section>'''
    page({'file': 'objekt.html', 'title': 'Exposé | Ritter Immobilien Stolberg', 'desc': 'Exposé eines Angebots von Ritter Immobilien: Objektdaten, Beschreibung, Lage, Energieausweis und Kaufnebenkosten.', 'group': 'angebote.html', 'js': ['tools.js']}, body)

# ---------------------------------------------------------------- Eigentümer-Seiten
def verkaufen():
    zus = ['Professionelle, kompetente und ehrliche Beratung', 'Vermeidung von Besichtigungstourismus – keine Sammelbesichtigungen (Open House)', 'Persönliche Kundenbetreuung', 'Durchsetzung des maximal möglichen Kaufpreises', 'Schneller Verkauf durch vorgemerkte Kunden', 'Diskreter und lautloser Verkauf auf Wunsch', 'Absicherung der Kaufpreiszahlung durch Bonitätsprüfung der Käufer', 'Service für Senioren: Beratung zu den Möglichkeiten des Wohnens im Alter', 'Haushaltsauflösungen, zum Beispiel nach einer Erbschaft, auf Wunsch', 'Haftungssicherer Verkauf (Vermögensschadenhaftpflicht)']
    body = schild('Immobilie verkaufen', 'Sie möchten Ihr Haus, Ihre Wohnung oder Ihr Grundstück verkaufen? Wir entwerfen für jede Immobilie ein eigenes Verkaufskonzept – und haben oft schon den passenden Käufer.', 'glas-diele', 'Helle Diele mit Treppe', 'Für Eigentümer') + f'''
<section class="text-sec">
 <div class="wrap cols2">
  <div><h2>Das sichern wir Ihnen zu</h2><ul class="ticks">{''.join('<li>' + e(z) + '</li>' for z in zus)}</ul></div>
  <div><h2>Warum mit Makler?</h2><p>Dank unseres großen und solventen Kundenkreises verkaufen wir nahezu alle beauftragten Objekte erfolgreich. Persönliche Begleitung und umfassender Service bis zum Notartermin – und auch danach – sind für uns selbstverständlich.</p>
   <p>Wir sind ein familiengeführtes, unabhängiges Büro. Bei Immobilien geht es um die Vermögenswerte unserer Kunden; dieser Verantwortung sind wir uns bewusst. Gern nennen wir Ihnen hiesige Notare als Referenz, die über unsere Arbeit Auskunft geben.</p>
   <p class="quote-own">„Verkaufen Sie auf keinen Fall, bevor Sie nicht mit uns gesprochen haben!“<br><small>Rudolf Ritter</small></p></div>
 </div>
</section>
<section class="tool" id="werkzeug">
 <div class="wrap"><div class="tool-head"><h2>Käufer warten schon</h2><p class="lead">Wählen Sie Art, Ort und Preisrahmen – wir zeigen Ihnen, welche unserer vorgemerkten Suchaufträge passen.</p></div>
 {matcher('abgleich-v')}</div>
</section>''' + cta('Was ist Ihre Immobilie wert?', 'Wir kommen vorbei und schätzen sie ein – kostenlos und unverbindlich.', 'bewertung')
    page({'file': 'verkaufen.html', 'title': 'Immobilie verkaufen in Stolberg & Aachen | Ritter Immobilien', 'desc': 'Haus oder Wohnung verkaufen mit Ritter Immobilien: Bewertung vor Ort, vorgemerkte Käufer, keine Sammelbesichtigungen, Begleitung bis zum Notar.', 'js': ['tools.js']}, body)

def kaeufer():
    li = ''.join(f'<li><span class="k-wer">{e(s["wer"])}</span><p>{e(s["text"])}</p></li>' for s in SUCH)
    body = schild('Käufer warten schon', 'Für diese Kunden suchen wir gerade. Passt Ihre Immobilie? Dann ist ein schneller, sicherer Verkauf gut möglich.', 'garten-eifel', 'Garten mit Blick auf die bewaldeten Hügel der Eifel', 'Aktuelle Suchaufträge') + f'''
<section class="tool" id="werkzeug">
 <div class="wrap"><div class="tool-head"><h2>Suchaufträge abgleichen</h2><p class="lead">Drei Angaben genügen.</p></div>{matcher('abgleich-k')}</div>
</section>
<section class="text-sec">
 <div class="wrap"><h2>Alle aktuellen Suchaufträge</h2><p class="muted">Stand 12.09.2025. Die Bonität unserer Kaufinteressenten prüfen wir vorab.</p><ul class="such-list">{li}</ul></div>
</section>''' + cta('Ihr Haus passt?', 'Rufen Sie uns unverbindlich an – wir freuen uns auf Ihren Anruf.', 'verkauf')
    page({'file': 'kaeufer-warten.html', 'title': 'Suchaufträge: Käufer warten schon | Ritter Immobilien', 'desc': 'Aktuelle Suchaufträge von Ritter Immobilien: Familien, Paare und Anleger suchen Häuser, Wohnungen und Mehrfamilienhäuser in Stolberg und Umgebung.', 'js': ['tools.js']}, body)

def bewertung():
    body = schild('Immobilie bewerten', 'Eine genaue Wertermittlung ist die erste Voraussetzung für einen erfolgreichen Verkauf. Wir schätzen Ihre Immobilie vor Ort ein – kostenlos und unverbindlich.', 'weisses-haus', 'Freistehendes weißes Einfamilienhaus mit Garten', 'Für Eigentümer') + f'''
<section class="tool" id="werkzeug">
 <div class="wrap">
  <div class="tool-head"><h2>Welches Bewertungsverfahren passt?</h2><p class="lead">Der Verkehrswert wird je nach Immobilie mit einem von drei Verfahren ermittelt. Wählen Sie Ihre Immobilie.</p></div>
  <div class="verf" data-verf>
   <div class="seg" role="group" data-verf-typ>
    <button type="button" data-v="sach" aria-pressed="true">Ein- oder Zweifamilienhaus</button><button type="button" data-v="vergleich">Eigentumswohnung</button><button type="button" data-v="ertrag">Mehrfamilienhaus / Anlageobjekt</button><button type="button" data-v="vergleich-g">Baugrundstück</button>
   </div>
   <div class="verf-out" aria-live="polite">
    <article data-verf-k="sach"><h3>Sachwertverfahren</h3><p>Vorrangig bei Ein- und Zweifamilienhäusern: Aus Grundstückswert, Gebäudewert, Außenanlagen und weiteren wertbeeinflussenden Faktoren wird der Sachwert ermittelt.</p><p class="muted">Was wir vor Ort ansehen: Baujahr und Bauweise, Zustand von Dach, Fenstern, Heizung, Ausstattung, Grundstücksgröße und -zuschnitt, Garage, Garten, Lage im Ortsteil.</p></article>
    <article data-verf-k="vergleich" hidden><h3>Vergleichswertverfahren</h3><p>Häufig bei Eigentumswohnungen: Über mehrere Vergleichsobjekte und den Einsatz von Faktoren wird der Wert ermittelt.</p><p class="muted">Was wir vor Ort ansehen: Lage und Etage, Wohnfläche, Balkon oder Terrasse, Stellplatz, Zustand des Gemeinschaftseigentums, Rücklagen, Hausgeld.</p></article>
    <article data-verf-k="ertrag" hidden><h3>Ertragswertverfahren</h3><p>Vor allem bei Investitionsobjekten: Hier geht es weniger um den reinen Sachwert als darum, welche Erträge mit der Immobilie erzielt werden können.</p><p class="muted">Was wir brauchen: Mieterliste mit Kaltmieten, Wohn- und Nutzflächen, laufende Kosten, Zustand und anstehende Instandhaltungen.</p></article>
    <article data-verf-k="vergleich-g" hidden><h3>Vergleichswertverfahren (Bodenrichtwert)</h3><p>Bei Baugrundstücken dienen Vergleichspreise und der Bodenrichtwert als Grundlage; Zuschnitt, Erschließung und Bebaubarkeit verändern den Wert.</p><p class="muted">Was wir brauchen: Flurstück, Größe, Bebauungsplan oder Lage im Innenbereich, Erschließungszustand.</p></article>
   </div>
  </div>
 </div>
</section>
<section class="text-sec">
 <div class="wrap cols2">
  <div><h2>Warum nicht online bewerten?</h2><p>Online-Rechner fertigen eine unzureichende Wertermittlung auf Grund einfacher, grober Befragungen. Eine realistische Bewertung erfordert die persönliche Begutachtung durch den Fachmann mit Berufserfahrung und Kenntnis des hiesigen Marktes. Verschenken Sie kein Geld.</p></div>
  <div><h2>Wann ein Gutachten nötig ist</h2><p>Steht ein Verkauf wegen einer Scheidung oder eines Erbes bevor, ist der exakte Wert besonders wichtig. Verpflichtend ist ein Verkehrswertgutachten zum Beispiel bei Scheidungs- oder Erbstreitigkeiten oder wenn der Wert vor Gericht belastbar dargelegt werden muss – dann vermitteln wir einen öffentlich bestellten Gutachter.</p></div>
 </div>
</section>''' + cta('Kostenlose Bewertung vereinbaren', 'Wir kommen zu Ihnen und nehmen uns Zeit – ohne Kosten und ohne Verpflichtung.', 'bewertung')
    page({'file': 'bewertung.html', 'title': 'Immobilienbewertung Stolberg – kostenlos vor Ort | Ritter', 'desc': 'Kostenlose, unverbindliche Immobilienbewertung vor Ort in Stolberg, Eschweiler und Aachen. Sachwert-, Vergleichswert- oder Ertragswertverfahren.', 'js': ['tools.js']}, body)

def vermieten():
    body = schild('Immobilie vermieten', 'Wir finden für Ihre Wohnung oder Ihr Haus seriöse, liquide Mieter – vom Inserat über die Besichtigung bis zur Übergabe.', 'wohnen-hell', 'Helles Wohnzimmer mit Holzboden', 'Für Eigentümer') + f'''
<section class="text-sec">
 <div class="wrap cols2">
  <div><h2>Was wir übernehmen</h2><ul class="ticks">
   <li>Einschätzung einer marktgerechten Miete</li><li>Präsentation und Inserat Ihrer Immobilie</li><li>Begleitete Besichtigungen, keine Sammeltermine</li>
   <li>Auswahl seriöser, liquider Mieter</li><li>Abschluss des Mietvertrags (zum Beispiel mit Verträgen von Haus &amp; Grund Aachen)</li><li>Wohnungsabnahme und Übergabe an die Mieter</li></ul></div>
  <div><h2>Und danach?</h2><p>Wenn Sie möchten, bleibt die Immobilie bei uns in guten Händen: Unsere <a href="hausverwaltung.html">Hausverwaltung</a> betreut Mieter, Handwerker und Nebenkostenabrechnung.</p>
   <p class="quote-inline">„Frau Ritter hat sich persönlich dafür eingesetzt, dass wir am Ende den passenden Mieter gefunden haben.“<br><small>H. und M. Delasauce, Stolberg-Münsterbusch</small></p></div>
 </div>
</section>
<section class="tool" id="werkzeug">
 <div class="wrap">
  <div class="tool-head"><h2>Kautions-Rechner</h2><p class="lead">Wie hoch darf die Mietkaution sein? Geben Sie die monatliche Nettokaltmiete ein.</p></div>
  <div class="kaution" data-kaution>
   <label class="big-in">Nettokaltmiete pro Monat in €<input type="text" inputmode="numeric" value="850" data-k-miete></label>
   <dl class="k-out" aria-live="polite" data-k-out></dl>
   <p class="muted small">Nach § 551 BGB darf die Kaution höchstens drei Monatsmieten ohne Nebenkosten betragen. Mieter dürfen sie in drei gleichen monatlichen Teilen zahlen, die erste Rate ist zu Beginn des Mietverhältnisses fällig. Der Vermieter legt sie getrennt von seinem Vermögen bei einer Bank an. Allgemeine Information, keine Rechtsberatung.</p>
  </div>
 </div>
</section>''' + cta('Vermietung besprechen', 'Erzählen Sie uns von Ihrer Immobilie – wir melden uns mit einer Einschätzung.', 'vermietung')
    page({'file': 'vermieten.html', 'title': 'Immobilie vermieten in Stolberg | Ritter Immobilien', 'desc': 'Wohnung oder Haus vermieten mit Ritter Immobilien: Mietpreis, Mieterauswahl, Mietvertrag, Übergabe. Mit Kautions-Rechner nach § 551 BGB.', 'js': ['tools.js']}, body)

def finanzierung():
    body = schild('Finanzierung', 'Eine seriöse, unabhängige Finanzierung ist uns wichtig. Unser unabhängiger Finanzierungsexperte vermittelt Ihnen eine maßgeschneiderte Finanzierung – kostenlos.', 'glas-kueche', 'Küche mit Holzfronten und Essplatz', 'Für Käufer') + f'''
<section class="tool" id="werkzeug">
 <div class="wrap">
  <div class="tool-head"><h2>Kaufnebenkosten in NRW</h2><p class="lead">Zum Kaufpreis kommen Grunderwerbsteuer, Notar und Grundbuch und gegebenenfalls die Maklerprovision. So viel Eigenkapital sollten Sie mindestens einplanen.</p></div>
  <div class="nk" data-nk-page>
   <div class="nk-in">
    <label class="big-in">Kaufpreis in €<input type="text" inputmode="numeric" value="350.000" data-nk-preis></label>
    <fieldset><legend>Maklerprovision Käufer</legend><div class="seg" data-nk-prov><button type="button" data-v="0">keine</button><button type="button" data-v="2.38">2,38 %</button><button type="button" data-v="3.57" aria-pressed="true">3,57 %</button></div></fieldset>
   </div>
   <dl class="nk-out" aria-live="polite" data-nk-out></dl>
  </div>
  <p class="muted small">Grunderwerbsteuer in NRW: 6,5 %. Notar und Grundbuch: Richtwert rund 2 % des Kaufpreises. Maklerprovision laut Exposé; bei Einfamilienhäusern und Eigentumswohnungen tragen Käufer und Verkäufer sie seit 23.12.2020 in der Regel je zur Hälfte (§ 656c BGB). Richtwerte ohne Gewähr.</p>
 </div>
</section>
<section class="text-sec">
 <div class="wrap cols2">
  <div><h2>Unabhängig beraten</h2><p>Wir pflegen Kontakte zu den regionalen Bankhäusern und arbeiten mit einem unabhängigen Finanzierungsexperten zusammen, der die Angebote vieler Banken vergleicht. Für Sie ist die Vermittlung kostenlos.</p></div>
  <div><h2>Ratgeber</h2><p><a href="ratgeber-kaufnebenkosten.html">Kaufnebenkosten in NRW: womit Sie rechnen müssen</a></p></div>
 </div>
</section>''' + cta('Finanzierung anfragen', 'Wir stellen den Kontakt zu unserem Finanzierungsexperten her.', 'finanzierung')
    page({'file': 'finanzierung.html', 'title': 'Immobilienfinanzierung & Kaufnebenkosten NRW | Ritter', 'desc': 'Kostenlose, unabhängige Finanzierungsvermittlung über Ritter Immobilien – mit Rechner für Kaufnebenkosten in NRW (Grunderwerbsteuer 6,5 %).', 'js': ['tools.js']}, body)

def referenzen():
    from collections import OrderedDict
    groups = OrderedDict()
    for r in REFS:
        groups.setdefault(r['ort'], []).append(r['text'])
    order = sorted(groups.items(), key=lambda kv: -len(kv[1]))
    btns = '<button type="button" data-o="" aria-pressed="true">Alle <small>' + str(len(REFS)) + '</small></button>' + ''.join(f'<button type="button" data-o="{e(o)}" aria-pressed="false">{e(o)} <small>{len(v)}</small></button>' for o, v in order)
    items = ''.join(f'<li data-ort="{e(o)}"><span class="r-ort">{e(o)}</span>{e(t)}</li>' for o, v in order for t in v)
    fotos = ['siedlungshaus', 'haus-garten', 'bungalow', 'neubau', 'hof-weiss', 'garten-palmen']
    alts = ['Verkauftes Einfamilienhaus mit Garage', 'Verkauftes Haus mit Garten', 'Verkaufter Bungalow mit großem Garten', 'Verkaufter Neubau', 'Verkauftes weißes Haus mit Hof', 'Garten mit Palmen eines verkauften Hauses']
    strip = ''.join(f'<figure>{img(f, a, "", "(max-width: 700px) 50vw, 33vw")}</figure>' for f, a in zip(fotos, alts))
    body = schild('Referenzen', f'Ein Auszug aus unseren vermittelten Immobilien: {len(REFS)} Häuser und Wohnungen im ganzen Kreis Aachen. Weitere Referenzen nennen wir Ihnen gern auf Anfrage.', 'siedlungshaus', 'Verkauftes Einfamilienhaus mit Garage', 'Verkauft') + f'''
<section class="refs" id="werkzeug">
 <div class="wrap">
  <div class="ref-orte" role="group" aria-label="Nach Ort anzeigen">{btns}</div>
  <ul class="ref-list" data-ref-list>{items}</ul>
  <div class="ref-strip">{strip}</div>
  <p class="muted small">Eigene Fotos verkaufter Häuser. Seit vielen Jahren von ImmobilienScout24 als PremiumPartner (2015–2019) und Experte (seit 2012) ausgezeichnet.</p>
 </div>
</section>''' + cta()
    page({'file': 'referenzen.html', 'title': 'Referenzen: verkaufte Immobilien | Ritter Immobilien', 'desc': f'{len(REFS)} vermittelte Häuser und Wohnungen von Ritter Immobilien in Stolberg, Roetgen, Eschweiler und Aachen – nach Ortsteil.', 'js': ['tools.js']}, body)

def kundenstimmen():
    items = ''.join(f'<figure><blockquote>„{e(t)}“</blockquote><figcaption><b>{e(n)}</b> · {e(o)}</figcaption></figure>' for o, t, n in STIMMEN)
    body = schild('Kundenstimmen', 'Wir leben davon, weiterempfohlen zu werden. Das schreiben Verkäufer und Vermieter nach der Zusammenarbeit.', 'wintergarten', 'Heller Wintergarten mit Korbsesseln', 'Meinungen') + f'''
<section class="voices-all"><div class="wrap"><div class="va-grid">{items}</div>
<p class="muted small">Auszug aus den Kundenmeinungen auf unserer bisherigen Website, teils gekürzt.</p></div></section>''' + cta()
    page({'file': 'kundenstimmen.html', 'title': 'Kundenstimmen | Ritter Immobilien Stolberg', 'desc': 'Was Verkäufer und Vermieter aus Stolberg, Eschweiler, Aachen und Roetgen über Ritter Immobilien sagen.'}, body)

def hausverwaltung():
    aufgaben = ['Kompetente Betreuung Ihrer Mieter', 'Gesamte Kommunikation mit Mietern, Handwerkern und Dienstleistern', 'Schnelle Neuvermietung bei Kündigung oder Leerstand durch eigenen Maklerservice', 'Auswahl seriöser, liquider Mieter bei Erstbezug oder Mieterwechsel', 'Abschluss von Mietverträgen (zum Beispiel Verträge von Haus & Grund Aachen)', 'Wohnungsabnahme und Übergabe mit den Mietern', 'Erstellung der jährlichen Nebenkostenabrechnung', 'Regelmäßige Objektbegehungen und Gespräche mit Mietern und Hausmeistern', 'Überwachung der Hausordnung', 'Koordination anstehender Reparaturen und Wartungen', 'Überwachung von Hausreinigung, Gartenpflege und Winterdienst']
    body = schild('Hausverwaltung', 'Wir verwalten Ein- und Mehrfamilienhäuser in Aachen Stadt und Land – für den bestmöglichen Werterhalt Ihrer Immobilie und eine sichere Rendite.', 'siedlungshaus', 'Gepflegtes Wohnhaus mit Garage', 'Für Vermieter') + f'''
<section class="text-sec">
 <div class="wrap cols2">
  <div><h2>Wir kümmern uns um</h2><ul class="ticks">{''.join('<li>' + e(a) + '</li>' for a in aufgaben)}</ul></div>
  <div><h2>Vertrauenssache</h2><p>Eigentümer und Mieter verlassen sich seit fast 30 Jahren auf die Hausverwaltung von Ritter Immobilien. Auf Basis langjähriger Erfahrung in der Miethausverwaltung bieten wir einen zuverlässigen Rundum-Service – auch bei der Planung von Sanierungen.</p>
   <p class="quote-own">„Nach einem arbeitsreichen Tag ruhen Sie sich aus und bewundern Ihre Immobilie – wir kümmern uns um den Rest.“<br><small>Rudolf Ritter</small></p></div>
 </div>
</section>
<section class="tool" id="werkzeug">
 <div class="wrap">
  <div class="tool-head"><h2>Das Verwaltungsjahr</h2><p class="lead">Was steht in welchem Monat an? Wählen Sie einen Monat.</p></div>
  <div class="season" data-hv>
   <div class="season-m" role="group" aria-label="Monat wählen">{''.join(f'<button type="button" data-m="{i}">{m}</button>' for i, m in enumerate(['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']))}</div>
   <div class="season-out" aria-live="polite"></div>
  </div>
  <p class="muted small">Beispielhafter Jahreslauf; Termine richten sich nach Objekt, Abrechnungszeitraum und Verträgen.</p>
 </div>
</section>''' + cta('Hausverwaltung anfragen', 'Schreiben Sie uns, um welches Objekt es geht – per Mail an info@ritterimmobilien.de oder über das Formular.', 'hausverwaltung')
    page({'file': 'hausverwaltung.html', 'title': 'Hausverwaltung Stolberg & Aachen | Ritter Immobilien', 'desc': 'Miethausverwaltung für Ein- und Mehrfamilienhäuser in Stolberg und Aachen: Mieterbetreuung, Neuvermietung, Nebenkostenabrechnung, Objektbegehungen.', 'js': ['tools.js']}, body)

def ueber():
    body = schild('Über uns', 'Seit 1989 sind wir als familiengeführtes und unabhängiges Immobilienbüro in der StädteRegion Aachen tätig – mit Schwerpunkt auf Einfamilienhäusern, Mehrfamilienhäusern und Eigentumswohnungen.', 'team', 'Rudolf Ritter und Maike Steyns', 'Ritter Immobilien e.K.') + f'''
<section class="about">
 <div class="wrap about-grid">
  <div>
   <h2>Rudolf Ritter</h2><p class="muted">Immobilienmakler · Gründer und Inhaber</p>
   <p>Seit über 35 Jahren führt er das Unternehmen mit Herz und Seele. Durch seine jahrelange Berufserfahrung kennt er den hiesigen Immobilienmarkt genauestens und steht Ihnen bei allen Fragen rund um Ihre Immobilie zur Verfügung.</p>
   <h2>Maike Steyns</h2><p class="muted">Immobilienfachwirtin (IHK) · Immobilienmaklerin (IHK)</p>
   <p>Seit 2017 im Familienbetrieb, zuständig für den Verkauf und die Vermietung von Wohnimmobilien. Im Mai 2020 hat sie ihre Prüfung zur Immobilienfachwirtin (IHK) abgelegt.</p>
   <h2>Unser Versprechen</h2><p>Die Zufriedenheit unserer Kunden steht an erster Stelle. Oberste Maxime ist, Ihnen zu helfen, Ihre Ziele best- und schnellstmöglich zu erreichen. Zu unserem Service gehört auch eine umfassende Beratung für Senioren zu den Möglichkeiten des Wohnens im Alter; Haushaltsauflösungen, etwa nach einer Erbschaft, geben wir auf Wunsch in Auftrag.</p>
  </div>
  <aside>
   <dl class="facts">
    <div><dt>Gegründet</dt><dd>1989</dd></div>
    <div><dt>Auszeichnungen</dt><dd>ImmobilienScout24 PremiumPartner 2015–2019, ImmobilienScout24 Experte seit 2012</dd></div>
    <div><dt>Gebiet</dt><dd>Stolberg, Eschweiler, Würselen, Aachen, Roetgen, Simmerath, Jülich, Düren und die Grenzregion Belgien</dd></div>
    <div><dt>Büro</dt><dd>{STR}, {PLZ} {ORT}</dd></div>
   </dl>
   <figure class="about-burg">{img('burg', 'Die Burg Stolberg', '', '(max-width: 900px) 100vw, 30vw', False, 640, 480)}<figcaption>Zu Hause in Stolberg.</figcaption></figure>
  </aside>
 </div>
</section>
<section class="text-sec">
 <div class="wrap"><h2>Einige unserer Partner</h2>
  <ul class="partner">
   <li><b>Notare Dr. Stefan Schmitz</b><span>Reitmeisterweg 14, 52223 Stolberg</span></li>
   <li><b>Notar Johannes Schneider</b><span>Trierer Str. 821, 52078 Aachen</span></li>
   <li><b>Notar Ralf Ersfeld und Notar Martin Johannes Rudersdorf</b><span>Bahnhofstr. 1, 52064 Aachen</span></li>
   <li><b>Sachverständiger und Gutachter Dipl.-Ing. Gerhard Witte</b><span>Jakobstr. 60, 52064 Aachen</span></li>
   <li><b>SUMMIT IT CONSULT GmbH</b><span>Rue de Wattrelos 23, 52249 Eschweiler</span></li>
  </ul></div>
</section>''' + cta()
    page({'file': 'ueber-uns.html', 'title': 'Über uns – Familienbetrieb seit 1989 | Ritter Immobilien', 'desc': 'Rudolf Ritter und Maike Steyns: familiengeführtes, unabhängiges Immobilienbüro in Stolberg seit 1989. ImmobilienScout24 PremiumPartner.'}, body)

RAT = [
 ('ratgeber-bewertung.html', 'Drei Verfahren der Immobilienbewertung', 'Sachwert, Vergleichswert, Ertragswert: welches Verfahren für welche Immobilie gilt – und warum Online-Rechner nicht reichen.', 'weisses-haus'),
 ('ratgeber-erbe.html', 'Verkaufen nach Erbe oder Scheidung', 'Wenn mehrere Beteiligte entscheiden müssen: Wert, Gutachten, Haushaltsauflösung und ein ruhiger Ablauf.', 'glas-wohnen'),
 ('ratgeber-kaufnebenkosten.html', 'Kaufnebenkosten in NRW', 'Grunderwerbsteuer, Notar, Grundbuch und Provision: womit Käufer rechnen müssen – mit Beispielrechnung.', 'glas-kueche'),
]

def ratgeber():
    items = ''.join(f'<li><a href="{f}">{img(ph, t, "rg-img", "(max-width: 900px) 100vw, 33vw")}<span class="rg-t">{e(t)}</span><span class="rg-d">{e(d)}</span></a></li>' for f, t, d, ph in RAT)
    body = schild('Ratgeber', 'Kurz erklärt: was Eigentümer und Käufer rund um Bewertung, Verkauf und Kauf wissen sollten.', 'garten-palmen', 'Gartenweg mit Palmen', 'Wissen') + f'<section class="rg"><div class="wrap"><ul class="rg-list">{items}</ul></div></section>' + cta()
    page({'file': 'ratgeber.html', 'title': 'Ratgeber Immobilien verkaufen & kaufen | Ritter Immobilien', 'desc': 'Ratgeber von Ritter Immobilien: Immobilienbewertung, Verkauf nach Erbe oder Scheidung, Kaufnebenkosten in NRW.'}, body)

def artikel(i, content):
    f, t, d, ph = RAT[i]
    others = ''.join(f'<li><a href="{x[0]}">{e(x[1])}</a></li>' for j, x in enumerate(RAT) if j != i)
    body = schild(t, d, ph, t, 'Ratgeber') + f'<article class="art"><div class="wrap art-grid"><div class="art-body">{content}</div><aside class="art-side"><h2>Weiterlesen</h2><ul>{others}</ul><a class="btn mag" href="kontakt.html?thema=bewertung">Kostenlose Bewertung</a></aside></div></article>' + cta()
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": t, "description": d, "datePublished": "2026-09-29", "author": {"@type": "Person", "name": "Rudolf Ritter"}, "publisher": {"@id": BASE + "#firma"}, "mainEntityOfPage": BASE + f}]
    page({'file': f, 'title': t + ' | Ritter Immobilien', 'desc': d[:155], 'group': 'ratgeber.html', 'ld': ld, 'js': ['tools.js'] if i == 2 else []}, body)

def artikel_all():
    artikel(0, '''<p class="lead">Der Verkehrswert einer Immobilie wird durch viele Faktoren beeinflusst: Lage, Zustand, Ausstattung, Baujahr. Je nach Art der Immobilie kommt eines von drei anerkannten Verfahren zum Einsatz.</p>
<h2>Sachwertverfahren</h2><p>Vorrangig bei Ein- und Zweifamilienhäusern. Abhängig vom Grundstückswert, dem Gebäudewert, den Außenanlagen und weiteren wertbeeinflussenden Faktoren wird der Sachwert ermittelt.</p>
<h2>Vergleichswertverfahren</h2><p>Häufig bei Eigentumswohnungen. Über mehrere Vergleichsobjekte und den Einsatz von Faktoren wird der Immobilienwert ermittelt. Auch Baugrundstücke werden so bewertet, meist mit dem Bodenrichtwert als Grundlage.</p>
<h2>Ertragswertverfahren</h2><p>Vor allem bei Investitionsobjekten wie Mehrfamilienhäusern. Hier geht es weniger um den reinen Sachwert als darum, welche Erträge mit der Immobilie erzielt werden können.</p>
<h2>Und die Online-Rechner?</h2><p>Sie liefern eine grobe Zahl auf Grund einfacher Fragen. Eine realistische Bewertung erfordert eine persönliche Begutachtung vor Ort – durch jemanden, der den hiesigen Markt kennt. Wir bewerten Ihre Immobilie kostenlos und unverbindlich; bei Streitigkeiten vor Gericht vermitteln wir einen Gutachter für ein Verkehrswertgutachten.</p>
<p><a href="bewertung.html#werkzeug">Welches Verfahren passt zu Ihrer Immobilie?</a></p>''')
    artikel(1, '''<p class="lead">Ein Haus aus einem Erbe oder nach einer Trennung zu verkaufen, ist selten nur eine Rechenaufgabe. Oft müssen mehrere Menschen gemeinsam entscheiden – und der Wert muss für alle nachvollziehbar sein.</p>
<h2>Den Wert klären</h2><p>Am Anfang steht eine realistische Einschätzung. Sind sich alle Beteiligten einig, reicht in der Regel eine fundierte Bewertung durch den Makler vor Ort. Gibt es Streit oder muss der Wert vor Gericht belastbar dargelegt werden, ist ein Verkehrswertgutachten eines Sachverständigen verpflichtend.</p>
<h2>Eine Stimme für alle</h2><p>Bei Erbengemeinschaften hilft es, eine Person als Ansprechpartner zu bestimmen. Wir halten alle Beteiligten auf dem gleichen Stand – auch über größere Entfernungen, per Telefon und E-Mail.</p>
<h2>Das Haus räumen</h2><p>Nach einem Erbfall steht das Haus oft noch voller Möbel und Erinnerungen. Haushaltsauflösungen geben wir auf Wunsch in Auftrag, damit Sie sich darum nicht kümmern müssen.</p>
<h2>Diskret verkaufen</h2><p>Nicht jeder möchte sein Elternhaus öffentlich inseriert sehen. Ein diskreter Verkauf an vorgemerkte, geprüfte Kaufinteressenten ist bei uns möglich – ohne Anzeige im Internet.</p>
<p>„Wir als Erbengemeinschaft fühlten uns von Herrn Ritter von Anfang an sehr kompetent beraten … Der erzielte Verkaufspreis hat unsere Erwartungen übertroffen.“ – Franz Gillessen, Stolberg</p>''')
    artikel(2, '''<p class="lead">Wer eine Immobilie kauft, zahlt mehr als den Kaufpreis. Die Kaufnebenkosten sollten Sie aus Eigenkapital bezahlen können – Banken finanzieren sie meist nicht mit.</p>
<h2>Grunderwerbsteuer: 6,5 %</h2><p>In Nordrhein-Westfalen beträgt die Grunderwerbsteuer 6,5 % des Kaufpreises. Das Finanzamt verschickt den Bescheid nach dem Notartermin; erst nach Zahlung gibt es die Unbedenklichkeitsbescheinigung für die Eintragung ins Grundbuch.</p>
<h2>Notar und Grundbuch: rund 2 %</h2><p>Für die Beurkundung des Kaufvertrags, die Auflassungsvormerkung, die Eigentumsumschreibung und die Eintragung einer Grundschuld fallen zusammen als Richtwert etwa 1,5 bis 2 % des Kaufpreises an.</p>
<h2>Maklerprovision</h2><p>Seit dem 23.12.2020 gilt beim Kauf von Einfamilienhäusern und Eigentumswohnungen durch Verbraucher: Hat der Verkäufer den Makler beauftragt, darf der Käufer höchstens die Hälfte der Provision tragen (§ 656c und § 656d BGB). Die genaue Höhe steht im Exposé.</p>
<h2>Beispiel: Kaufpreis 350.000 €</h2><p>Grunderwerbsteuer 22.750 €, Notar und Grundbuch rund 7.000 €, Provision 3,57 % = 12.495 €. Zusammen rund 42.245 € – etwa 12 % des Kaufpreises.</p>
<p><a href="finanzierung.html#werkzeug">Jetzt mit Ihrem Kaufpreis rechnen</a></p>''')

FAQ = [
 ('Was kostet die Bewertung meiner Immobilie?', 'Nichts. Wir schätzen Ihre Immobilie kostenlos und unverbindlich vor Ort ein. Ein Verkehrswertgutachten für Gerichtsverfahren erstellt ein Sachverständiger; den Kontakt stellen wir her.'),
 ('Machen Sie Sammelbesichtigungen?', 'Nein. Open-House-Termine führen wir nicht durch. Jede Besichtigung ist persönlich begleitet.'),
 ('Kann ich diskret verkaufen?', 'Ja. Auf Wunsch vermitteln wir Ihre Immobilie ohne öffentliche Anzeige an vorgemerkte, geprüfte Kaufinteressenten.'),
 ('Warum sehe ich nicht alle Angebote online?', 'Auf Wunsch einiger Eigentümer veröffentlichen wir nicht jedes Angebot und manche nur ohne Fotos. Hinterlassen Sie uns einen Suchauftrag – wir melden uns, sobald etwas passt.'),
 ('Wie aktuell sind die Angebote auf der Website?', 'Die Angebote kommen direkt aus unserem Angebotsbestand und werden bei jedem Seitenaufruf neu geladen.'),
 ('In welchen Orten sind Sie tätig?', 'In der StädteRegion Aachen, insbesondere Stolberg, Eschweiler, Würselen, Aachen, Roetgen, Simmerath, Jülich und Düren, sowie in der Grenzregion Belgien.'),
 ('Übernehmen Sie auch die Hausverwaltung?', 'Ja, wir verwalten Ein- und Mehrfamilienhäuser in Aachen Stadt und Land – von der Mieterbetreuung bis zur Nebenkostenabrechnung.'),
 ('Helfen Sie bei der Finanzierung?', 'Ja. Unser unabhängiger Finanzierungsexperte vermittelt Ihnen kostenlos eine passende Finanzierung; außerdem pflegen wir Kontakte zu den regionalen Banken.'),
 ('Was brauchen Sie für den Verkaufsauftrag?', 'Nach dem Geldwäschegesetz müssen wir vor Beginn der Geschäftsbeziehung die Identität unseres Vertragspartners feststellen, zum Beispiel mit einer Kopie des Personalausweises. Alle weiteren Unterlagen besprechen wir im Termin.'),
 ('Wer zahlt die Maklerprovision?', 'Beim Verkauf von Einfamilienhäusern und Eigentumswohnungen an Verbraucher tragen Käufer und Verkäufer die Provision seit Ende 2020 in der Regel je zur Hälfte. Die genaue Höhe steht im Exposé.'),
]

def faq():
    items = ''.join(f'<details class="qa"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    ld = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]
    body = schild('Häufige Fragen', 'Bewertung, Besichtigung, Provision, Hausverwaltung – die Antworten auf das, was wir am häufigsten gefragt werden.', 'bungalow', 'Bungalow mit großem Garten', 'FAQ') + f'<section class="faq"><div class="wrap faq-in">{items}</div></section>' + cta()
    page({'file': 'faq.html', 'title': 'Häufige Fragen | Ritter Immobilien Stolberg', 'desc': 'Antworten zu kostenloser Bewertung, diskretem Verkauf, Besichtigungen, Maklerprovision, Hausverwaltung und Finanzierung bei Ritter Immobilien.', 'ld': ld}, body)

def kontakt():
    body = schild('Kontakt', 'Stressfreier und reibungsloser Immobilienverkauf – schreiben Sie uns oder rufen Sie an. Wir melden uns schnellstmöglich.', 'team', 'Rudolf Ritter und Maike Steyns', 'Pfarrer-Gau-Str. 51') + f'''
<section class="book" id="werkzeug">
 <div class="wrap book-grid">
  <div>
   <ul class="contact-list">
    <li><a href="tel:{TEL_L}"><span>Telefon</span><b>{TEL}</b></a></li>
    <li><a href="tel:{MOBIL_L}"><span>Mobil</span><b>{MOBIL}</b></a></li>
    <li><a href="mailto:{MAIL}"><span>E-Mail</span><b>{MAIL}</b></a></li>
    <li><span><span>Fax</span><b>{FAX}</b></span></li>
   </ul>
   <dl class="facts"><div><dt>Büro in Stolberg</dt><dd>{FIRMA}<br>{STR}<br>{PLZ} {ORT}</dd></div><div><dt>Termine</dt><dd>nach Vereinbarung, gern auch bei Ihnen vor Ort</dd></div></dl>
   <div class="mapbox" data-map data-q="Pfarrer-Gau-Straße 51, 52223 Stolberg"><button type="button" class="map-load">{ICON['pin']}<span><b>Karte laden</b><small>Erst beim Klick wird OpenStreetMap geladen (Ihre IP-Adresse geht dabei an die OpenStreetMap Foundation).</small></span></button></div>
  </div>
  <div>{form('', 'Schreiben Sie uns')}</div>
 </div>
</section>'''
    page({'file': 'kontakt.html', 'title': 'Kontakt | Ritter Immobilien, Pfarrer-Gau-Str. 51, Stolberg', 'desc': 'Ritter Immobilien e.K., Pfarrer-Gau-Str. 51, 52223 Stolberg. Telefon 02402 3477, Mobil 0171 7803453, info@ritterimmobilien.de.'}, body)

def foehr():
    body = schild('Ferienhaus auf Föhr', 'Urlaubsreif? Föhr ist immer eine Reise wert – die grüne Insel unter den nordfriesischen Eilanden.', 'garten-palmen', 'Gartenweg', 'Urlaubsreif?') + f'''
<section class="text-sec"><div class="wrap cols2">
 <div><h2>Die Insel</h2><p>Das nach Norden liegende Marschland mit seinen jadeglänzenden Weideflächen gehört allein den Kühen und Seevögeln. 22 Kilometer Ringdeich mit Schafen als lebende Rasenmäher und 15 Kilometer weißer Sand. Das Haus liegt im historischen Ortskern des Dorfes Oldsum an einer alten Dorfstraße mit reetgedeckten Häusern; zum Oldsumer Naturstrand sind es etwa 1.500 Meter.</p>
  <h2>Das Ferienhaus</h2><p>Liebevoll restauriert, rund 100 m² Wohnfläche. Gemütliche gute Stube, kleine Video- und Bibliothek, zwei Schlafzimmer (eines mit Doppelbett und antikem Mobiliar, eines mit zwei Einzelbetten). Küche teils antik mit original Delfter Kacheln, dazu moderne Einbauküche mit Cerankochfeld, Backofen, Mikrowelle, Geschirrspüler, Waschmaschine und Kaffeemaschine.</p>
  <h2>Das Grundstück</h2><p>Eingezäunter Bauerngarten nach Südwesten mit Obstbäumen und windgeschützter Terrasse.</p>
  <a class="btn mag" href="kontakt.html?thema=foehr">Anfrage zum Ferienhaus</a></div>
 <div class="foehr-img"><figure>{img('foehr-1', 'Ferienhaus in Oldsum auf Föhr', '', '(max-width: 800px) 100vw, 45vw', False, 700, 432)}</figure><figure>{img('foehr-2', 'Ferienhaus auf Föhr', '', '(max-width: 800px) 60vw, 25vw', False, 500, 629)}</figure></div>
</div></section>'''
    page({'file': 'ferienhaus-foehr.html', 'title': 'Ferienhaus auf Föhr in Oldsum | Ritter Immobilien', 'desc': 'Liebevoll restauriertes Ferienhaus mit rund 100 m² im historischen Ortskern von Oldsum auf Föhr, 1,5 km zum Naturstrand.'}, body)

def simple(file, title, desc, h1, content, noindex=False):
    page({'file': file, 'title': title, 'desc': desc, 'noindex': noindex}, f'<section class="simple legal"><div class="wrap narrow"><h1>{h1}</h1>{content}</div></section>')

def recht():
    simple('danke.html', 'Danke für Ihre Nachricht | Ritter Immobilien', 'Ihre Nachricht an Ritter Immobilien ist angekommen.', 'Danke! Wir melden uns.',
           f'<p class="lead">Ihre Nachricht ist bei uns angekommen. Wir melden uns schnellstmöglich – oder rufen Sie direkt an: <a href="tel:{TEL_L}">{TEL}</a>.</p><div class="btns"><a class="btn mag" href="angebote.html">Aktuelle Angebote</a><a class="btn ghost mag" href="index.html">Zur Startseite</a></div>', True)
    simple('404.html', 'Seite nicht gefunden | Ritter Immobilien', 'Diese Seite gibt es nicht. Zu den aktuellen Angeboten von Ritter Immobilien.', 'Diese Tür führt ins Leere.',
           f'<p class="lead">Die Seite gibt es nicht (mehr). Vielleicht war es ein Angebot, das inzwischen verkauft ist?</p><div class="btns"><a class="btn mag" href="angebote.html">Aktuelle Angebote</a><a class="btn ghost mag" href="index.html">Zur Startseite</a></div>', True)
    simple('impressum.html', 'Impressum | Ritter Immobilien e.K.', 'Impressum der Ritter Immobilien e.K., Pfarrer-Gau-Str. 51, 52223 Stolberg. Inhaber Rudolf Ritter, HRA 9345 Amtsgericht Aachen.', 'Impressum', f'''
<h2>Angaben gemäß § 5 DDG</h2><p>{FIRMA}<br>{STR}<br>{PLZ} {ORT}</p>
<p><b>Inhaber und Vertretungsberechtigter:</b> Rudolf Ritter</p>
<h2>Kontakt</h2><p>Telefon: {TEL}<br>Mobil: {MOBIL}<br>Fax: {FAX}<br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a></p>
<h2>Registereintrag</h2><p>Amtsgericht Aachen, HRA 9345</p>
<h2>Umsatzsteuer-ID</h2><p>Umsatzsteuer-Identifikationsnummer nach § 27a UStG: DE 121824998</p>
<h2>Aufsichtsbehörde und Erlaubnis</h2><p>Erlaubnis nach § 34c Gewerbeordnung. Zuständige Aufsichtsbehörde: StädteRegion Aachen, Amt für Ordnungsangelegenheiten, Zollernstraße 20, 52070 Aachen.</p>
<h2>Kammer</h2><p>Industrie- und Handelskammer Aachen, Theaterstraße 6–10, 52062 Aachen</p>
<h2>Verbraucherstreitbeilegung</h2><p>Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
<h2>Bildnachweis</h2><p>Fotos: Ritter Immobilien e.K. Angebotsfotos: aus dem jeweiligen Inserat.</p>''')
    simple('agb.html', 'Allgemeine Geschäftsbedingungen | Ritter Immobilien', 'Allgemeine Geschäftsbedingungen der Ritter Immobilien e.K., Verkauf von Haus- und Grundbesitz.', 'Allgemeine Geschäftsbedingungen', '''
<p>Unsere Angebote sind unverbindlich, freibleibend, Zwischenverkauf vorbehalten.</p>
<p>Alle Angaben, die der Makler von Verkäufer- bzw. Vermieterseite erhält, werden vom Makler ohne Verbindlichkeiten weitergegeben. Sollten diese Irrtümer enthalten, haftet der Makler hierfür nicht.</p>
<p>Mit dem Abschluss eines durch unseren Nachweis oder unsere Vermittlung zustande gekommenen Kaufvertrages ist die ortsübliche Nachweis- bzw. Vermittlungsgebühr zzgl. Mehrwertsteuer zu zahlen. Die Maklerprovision ist beim Vertragsabschluss verdient und zahlbar.</p>
<p>Unsere Angebote dürfen nicht ohne unsere schriftliche Einwilligung an Dritte weitergegeben werden. Zuwiderhandlung verpflichtet zur Schadensersatzleistung in Höhe der ortsüblichen Nachweis- bzw. Vermittlungsprovision.</p>
<p>Eine von uns schriftlich oder mündlich mitgeteilte Gelegenheit zum Vertragsabschluss wird – wenn nicht unverzüglich (schriftlich mit Quellenangabe) Widerspruch erfolgt – als bisher unbekannt anerkannt.</p>
<p>Gerichtsstand ist Aachen.</p>
<h2>Geldwäschegesetz (GwG)</h2><p>Als Maklerunternehmen ist Ritter Immobilien nach §§ 1, 2 Abs. 1 Nr. 10, 4 Abs. 3 GwG verpflichtet, vor Begründung einer Geschäftsbeziehung die Identität des Vertragspartners festzustellen und zu überprüfen. Hierzu halten wir die relevanten Daten Ihres Personalausweises fest, beispielsweise mittels einer Kopie. Das Gesetz sieht vor, dass der Makler die Unterlagen fünf Jahre aufbewahrt.</p>''')
    simple('widerruf.html', 'Widerrufsbelehrung | Ritter Immobilien', 'Widerrufsbelehrung für Verbraucher und Muster-Widerrufsformular der Ritter Immobilien e.K.', 'Widerrufsbelehrung', f'''
<h2>Widerrufsrecht für Verbraucher</h2><p>Sie haben das Recht, binnen vierzehn Tagen ohne Angabe von Gründen diesen Vertrag zu widerrufen. Die Widerrufsfrist beträgt vierzehn Tage ab dem Tag des Vertragsabschlusses.</p>
<p>Um Ihr Widerrufsrecht auszuüben, müssen Sie uns ({FIRMA}, {STR}, {PLZ} {ORT}, Tel. {TEL}, Fax {FAX}, E-Mail: {MAIL}) mittels einer eindeutigen Erklärung (z. B. ein mit der Post versandter Brief, Telefax oder E-Mail) über Ihren Entschluss, diesen Vertrag zu widerrufen, informieren. Sie können dafür das Muster-Widerrufsformular verwenden, das jedoch nicht vorgeschrieben ist.</p>
<p>Zur Wahrung der Widerrufsfrist reicht es aus, dass Sie die Mitteilung über die Ausübung des Widerrufsrechts vor Ablauf der Widerrufsfrist absenden.</p>
<h2>Vorzeitiges Erlöschen</h2><p>Ihr Widerrufsrecht erlischt bei einem Vertrag zur Erbringung von Dienstleistungen vorzeitig, wenn wir die Dienstleistung vollständig erbracht haben und mit der Ausführung erst begonnen haben, nachdem Sie dazu Ihre ausdrückliche Zustimmung gegeben und gleichzeitig Ihre Kenntnis davon bestätigt haben, dass Sie Ihr Widerrufsrecht bei vollständiger Vertragserfüllung durch uns verlieren.</p>
<h2>Muster-Widerrufsformular</h2><p>(Wenn Sie den Vertrag widerrufen wollen, füllen Sie bitte dieses Formular aus und senden Sie es zurück.)</p>
<p>An: {FIRMA}, {STR}, {PLZ} {ORT}, Fax {FAX}, E-Mail: {MAIL}</p>
<p>Hiermit widerrufe(n) ich/wir (*) den von mir/uns (*) abgeschlossenen Vertrag über die Erbringung der folgenden Dienstleistung (*)<br>Bestellt am (*) / erhalten am (*)<br>Name des/der Verbraucher(s)<br>Anschrift des/der Verbraucher(s)<br>Unterschrift des/der Verbraucher(s) (nur bei Mitteilung auf Papier)<br>Datum</p><p>(*) Unzutreffendes streichen.</p>''')
    simple('datenschutz.html', 'Datenschutz | Ritter Immobilien e.K.', 'Datenschutzerklärung der Ritter Immobilien e.K.: keine Cookies, kein Tracking, Angebote über immowelt, Kontaktformular, Karte per Klick.', 'Datenschutzerklärung', f'''
<h2>1. Verantwortlicher</h2><p>{FIRMA}, Inhaber Rudolf Ritter, {STR}, {PLZ} {ORT}, Telefon {TEL}, E-Mail <a href="mailto:{MAIL}">{MAIL}</a>.</p>
<h2>2. Grundsätze</h2><p>Diese Website verwendet keine Cookies, kein Tracking und keine Analyse-Werkzeuge. Schriften werden von unserem eigenen Server geladen.</p>
<h2>3. Hosting</h2><p>[Hoster eintragen.] Beim Aufruf verarbeitet der Hoster technisch notwendige Daten (IP-Adresse, Zeitpunkt, aufgerufene Seite, Browser). Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO.</p>
<h2>4. Skript-Bibliotheken (jsDelivr)</h2><p>Für Animationen laden wir GSAP und Lenis über das Content-Delivery-Netzwerk jsDelivr. Dabei wird Ihre IP-Adresse an dessen Betreiber übermittelt. Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO.</p>
<h2>5. Immobilienangebote über immowelt</h2><p>Unsere aktuellen Angebote und Exposés werden beim Aufruf der Seiten „Angebote“, „Exposé“ und der Startseite direkt vom Homepagemodul der immowelt GmbH (Nordostpark 3–5, 90411 Nürnberg) geladen, die Angebotsfotos vom Bildserver ms.immowelt.org. Dabei wird Ihre IP-Adresse an immowelt übermittelt; wir setzen dabei keine Cookies. Rechtsgrundlage ist unser berechtigtes Interesse an einer stets aktuellen Darstellung unserer Angebote (Art. 6 Abs. 1 lit. f DSGVO). Datenschutzerklärung der immowelt: <a href="https://www.immowelt.de/immoweltag/datenschutz" rel="noopener">immowelt.de/immoweltag/datenschutz</a>.</p>
<h2>6. Kontaktformular, E-Mail, Telefon</h2><p>Wenn Sie uns anfragen, verarbeiten wir Ihre Angaben (Name, Kontaktdaten, Nachricht, ggf. Objekt) zur Bearbeitung und für Anschlussfragen. Rechtsgrundlage: Art. 6 Abs. 1 lit. b DSGVO (vorvertragliche Maßnahmen) bzw. lit. f. [Formular-Dienst eintragen.] Ihre Angaben werden nicht verkauft oder unbefugt an Dritte weitergegeben. Wir löschen sie, sobald die Anfrage erledigt ist und keine gesetzlichen Aufbewahrungspflichten bestehen.</p>
<h2>7. Geldwäschegesetz</h2><p>Kommt ein Maklervertrag zustande, sind wir nach dem Geldwäschegesetz verpflichtet, Ihre Identität festzustellen und die Unterlagen fünf Jahre aufzubewahren (Art. 6 Abs. 1 lit. c DSGVO).</p>
<h2>8. Karte</h2><p>Die Karte auf der Kontaktseite wird erst geladen, wenn Sie auf „Karte laden“ klicken. Dann werden Daten von der OpenStreetMap Foundation abgerufen und Ihre IP-Adresse dorthin übermittelt (Art. 6 Abs. 1 lit. a DSGVO).</p>
<h2>9. Ihre Rechte</h2><p>Auskunft, Berichtigung, Löschung, Einschränkung, Datenübertragbarkeit, Widerspruch (Art. 15–21 DSGVO) sowie Beschwerde bei einer Aufsichtsbehörde, z. B. der Landesbeauftragten für Datenschutz und Informationsfreiheit NRW.</p>
<p class="muted small">Stand: September 2026</p>''')

def sitemap():
    urls = [p for p in PAGES if not p.get('noindex') and p['file'] not in ('objekt.html',)]
    today = datetime.date.today().isoformat()
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f' <url><loc>{BASE}{"" if p["file"] == "index.html" else p["file"]}</loc><lastmod>{today}</lastmod></url>\n' for p in urls) + '</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(xml)
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nDisallow: /danke.html\n\nSitemap: {BASE}sitemap.xml\n')

if __name__ == '__main__':
    suchjs()
    home(); angebote(); objekt(); verkaufen(); kaeufer(); bewertung(); vermieten(); finanzierung(); referenzen(); kundenstimmen()
    hausverwaltung(); ueber(); ratgeber(); artikel_all(); faq(); kontakt(); foehr(); recht()
    sitemap()
    print(len(PAGES), 'Seiten gebaut, Version', V)
