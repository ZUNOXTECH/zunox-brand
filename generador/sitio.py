# -*- coding: utf-8 -*-
"""Genera index.html (landing de descargas) y manual.html (manual de identidad)."""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(__file__))
R = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ------------------------------------------------------------------ utilidades
def svg(path, cls=""):
    s = open(os.path.join(R, path)).read()
    m = re.match(r'<svg[^>]*>', s)
    root = re.sub(r'\s(width|height)="[^"]*"', '', m.group(0))
    root = root.replace('<svg', f'<svg class="fig {cls}"', 1)
    return root + s[m.end():]

def size(path):
    n = os.path.getsize(os.path.join(R, path))
    return f"{n/1048576:.1f} MB" if n >= 1048576 else f"{max(1, round(n/1024))} KB"

def count(sub):
    p = os.path.join(R, "assets", sub)
    return sum(len(f) for _, _, f in os.walk(p))

import brand as _b

def simbolo_nav():
    ps, w, h = _b.Zpaths(100.0)
    inner = "".join(f'<path d="{d}"/>' for d in ps)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" '
            f'aria-hidden="true" focusable="false">{inner}</svg>')

PAL = json.load(open(os.path.join(R, "assets", "color", "paleta.json")))["colores"]
def col(t): return next(c for c in PAL if c["token"] == t)["hex"]

def lum(h):
    c = [int(h[i:i+2], 16)/255 for i in (1, 3, 5)]
    c = [x/12.92 if x <= .03928 else ((x+.055)/1.055)**2.4 for x in c]
    return .2126*c[0] + .7152*c[1] + .0722*c[2]
def cr(a, b):
    l1, l2 = sorted([lum(a), lum(b)], reverse=True); return (l1+.05)/(l2+.05)

INK, PAPER, DEEP = "#071A1C", "#F0F2F0", col("ground")
GREEN, BRIGHT = col("g700"), col("g500")

# ------------------------------------------------------------------ css
CSS = f"""
*{{box-sizing:border-box}}
:root{{
  --paper:{PAPER}; --paper-2:#E3E7E4; --paper-3:#D3D9D5;
  --ink:{INK}; --ink-2:#42544F; --deep:{DEEP}; --green:{GREEN}; --bright:{BRIGHT};
  --gut:clamp(20px,4vw,64px); --max:1320px;
}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0; background:var(--paper); color:var(--ink);
  font-family:"Manrope",system-ui,-apple-system,sans-serif;
  font-size:clamp(17px,1.15vw,19px); line-height:1.6;
  -webkit-font-smoothing:antialiased; font-synthesis:none}}
img{{max-width:100%; height:auto; display:block}}
a{{color:var(--green); text-decoration:none; border-bottom:2px solid currentColor}}
a:hover{{background:var(--green); color:var(--paper); border-color:var(--green)}}
a:focus-visible{{outline:3px solid var(--green); outline-offset:3px}}
.wrap{{max-width:var(--max); margin:0 auto; padding:0 var(--gut)}}

.disp,h1,h2,h3{{font-family:"Sora",system-ui,sans-serif; font-weight:700;
  letter-spacing:-.035em; line-height:1.05; margin:0; text-wrap:balance;
  text-transform:uppercase}}
h1{{font-size:clamp(52px,10.5vw,142px)}}
h2{{font-size:clamp(40px,7vw,96px)}}
h3{{font-size:clamp(22px,2.6vw,34px); letter-spacing:-.025em; text-transform:none;
  line-height:1.12}}
.lab{{font-family:"Sora",sans-serif; font-weight:600; font-size:clamp(11px,.85vw,13px);
  letter-spacing:.2em; text-transform:uppercase; margin:0}}
.lead{{font-size:clamp(20px,1.75vw,27px); line-height:1.42; font-weight:500;
  max-width:26ch; margin:0}}
p{{margin:0}}
.body-col{{max-width:52ch; display:flex; flex-direction:column; gap:1.1em}}
.body-col b,.lead b{{font-weight:700}}
.num{{font-variant-numeric:tabular-nums}}

/* ---------- masthead ---------- */
.top{{border-bottom:5px solid var(--ink); position:sticky; top:0; z-index:20;
  background:var(--paper)}}
.top .wrap{{display:flex; justify-content:space-between; align-items:center;
  gap:16px 24px; padding-top:14px; padding-bottom:14px; flex-wrap:wrap}}
.brand{{display:flex; align-items:center; gap:12px; border:0; color:var(--ink)}}
.brand:hover{{background:none; color:var(--ink)}}
.brand svg{{width:26px; height:auto; flex:none}}
.brand svg path{{fill:var(--ink)}}
.brand span{{font-family:"Sora",sans-serif; font-weight:600; font-size:clamp(11px,.85vw,13px);
  letter-spacing:.2em; text-transform:uppercase}}
.nav{{display:flex}}
.nav a{{font-family:"Sora",sans-serif; font-weight:600; font-size:clamp(11px,.85vw,13px);
  letter-spacing:.14em; text-transform:uppercase; padding:11px clamp(14px,1.6vw,22px);
  border:2px solid var(--ink); color:var(--ink); background:transparent; line-height:1;
  transition:background .1s linear, color .1s linear}}
.nav a + a{{border-left:0}}
.nav a[aria-current="page"]{{background:var(--ink); color:var(--paper)}}
.nav a:hover{{background:var(--green); border-color:var(--green); color:var(--paper)}}
.nav a:hover + a{{border-left:0}}

/* ---------- salto a la otra página ---------- */
.jump{{display:flex; justify-content:space-between; align-items:center; gap:20px;
  flex-wrap:wrap; background:var(--deep); color:var(--paper); border:0;
  padding:clamp(28px,4vw,54px) clamp(24px,3.5vw,54px); margin-top:clamp(34px,4.5vw,64px)}}
.jump:hover{{background:#00252C; color:var(--paper)}}
.jump .k{{font-family:"Sora",sans-serif; font-weight:600; font-size:clamp(11px,.85vw,13px);
  letter-spacing:.2em; text-transform:uppercase; color:var(--bright); display:block;
  margin-bottom:.7em}}
.jump .t{{font-family:"Sora",sans-serif; font-weight:700; text-transform:uppercase;
  letter-spacing:-.03em; line-height:1; font-size:clamp(30px,5vw,66px)}}
.jump .d{{font-size:clamp(15px,1.1vw,18px); color:#A8CBC2; margin-top:.85em; max-width:44ch}}
.jump .arrow{{font-family:"Sora",sans-serif; font-weight:700; font-size:clamp(34px,5vw,64px);
  line-height:1; flex:none}}

/* ---------- secciones ---------- */
section{{border-top:5px solid var(--ink); padding:clamp(48px,6vw,92px) 0}}
section:first-of-type{{border-top:0}}
.head{{display:grid; grid-template-columns:minmax(96px,.9fr) 3.4fr; gap:clamp(16px,3vw,48px);
  align-items:start; margin-bottom:clamp(34px,4.5vw,64px)}}
.head .n{{font-family:"Sora",sans-serif; font-weight:700; font-size:clamp(54px,9vw,132px);
  line-height:.8; letter-spacing:-.05em; color:var(--ink)}}
.head .t{{display:flex; flex-direction:column; gap:clamp(16px,2vw,30px)}}
.rule{{height:2px; background:var(--ink); margin:clamp(30px,4vw,56px) 0}}
.rule.thin{{height:1px; background:var(--paper-3)}}

/* ---------- planchas ---------- */
.plate{{background:var(--deep); padding:clamp(28px,5vw,74px); display:flex;
  align-items:center; justify-content:center}}
.plate.paper{{background:var(--paper-2)}}
.plate.white{{background:#fff}}
.plate.tight{{padding:clamp(18px,2.5vw,34px)}}
.fig{{display:block; width:100%; height:auto}}
.plate .fig{{max-width:920px}}
.plate.hero{{padding:clamp(22px,3.5vw,54px)}}
.plate.hero .fig{{max-width:780px}}
figure{{margin:0}}
figcaption{{font-size:clamp(14px,1vw,16px); color:var(--ink-2); padding-top:14px;
  max-width:62ch; line-height:1.5}}

/* ---------- rejillas ---------- */
.g2{{display:grid; gap:clamp(20px,2.5vw,38px); grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}}
.g3{{display:grid; gap:clamp(18px,2vw,30px); grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}}
.g4{{display:grid; gap:clamp(14px,1.6vw,24px); grid-template-columns:repeat(auto-fit,minmax(165px,1fr))}}
.item h3{{margin-bottom:8px}}
.item p{{color:var(--ink-2); font-size:clamp(15px,1.05vw,17px); line-height:1.5}}
.item .plate{{margin-bottom:16px}}
.item .fig{{max-height:190px}}
code{{font-family:"Sora",monospace; font-weight:600; font-size:.92em;
  background:var(--paper-2); padding:.12em .38em; letter-spacing:-.01em}}
.mark{{font-family:"Sora",sans-serif; font-weight:600; font-size:13px;
  letter-spacing:.12em; text-transform:uppercase; color:var(--green)}}

/* ---------- datos ---------- */
.scroll{{overflow-x:auto; margin-inline:calc(var(--gut)*-1); padding-inline:var(--gut)}}
table{{width:100%; border-collapse:collapse; font-size:clamp(15px,1.1vw,18px)}}
th,td{{text-align:left; padding:clamp(12px,1.3vw,19px) 20px clamp(12px,1.3vw,19px) 0;
  border-bottom:1px solid var(--paper-3); white-space:nowrap; vertical-align:baseline}}
thead th{{border-bottom:2px solid var(--ink); font-family:"Sora",sans-serif;
  font-weight:600; font-size:clamp(11px,.85vw,13px); letter-spacing:.16em;
  text-transform:uppercase; padding-bottom:11px}}
td.n{{font-variant-numeric:tabular-nums}}
td.k{{font-family:"Sora",sans-serif; font-weight:600}}
.pos{{color:var(--green); font-weight:700}} .neg{{color:#B4341B; font-weight:700}}

/* ---------- muestras de color ---------- */
.sw{{display:flex; flex-direction:column}}
.sw .chip{{aspect-ratio:5/3; border:1px solid rgba(7,26,28,.12)}}
.sw dl{{margin:14px 0 0; display:flex; flex-direction:column; gap:3px}}
.sw dt{{font-family:"Sora",sans-serif; font-weight:700; font-size:clamp(17px,1.3vw,21px);
  letter-spacing:-.01em}}
.sw dd{{margin:0; font-size:14.5px; color:var(--ink-2); font-variant-numeric:tabular-nums}}
.sw dd.use{{margin-top:7px; line-height:1.45}}

/* ---------- descargas ---------- */
.hero-dl{{display:grid; grid-template-columns:repeat(auto-fit,minmax(290px,1fr));
  gap:clamp(18px,2vw,28px); align-items:stretch}}
.dl{{display:flex; flex-direction:column; justify-content:space-between; gap:22px;
  border:2px solid var(--ink); padding:clamp(20px,2.4vw,32px); background:var(--paper);
  transition:background .12s linear}}
.dl:hover{{background:var(--paper-2)}}
.dl.main{{background:var(--deep); border-color:var(--deep); color:var(--paper)}}
.dl.main:hover{{background:#00252C}}
.dl.main .meta{{color:#9FC4BC}}
.dl h3{{font-family:"Sora",sans-serif; font-weight:700; text-transform:uppercase;
  letter-spacing:-.02em; font-size:clamp(21px,2vw,30px); line-height:1}}
.dl .meta{{font-size:14.5px; color:var(--ink-2); font-variant-numeric:tabular-nums}}
.dl .go{{font-family:"Sora",sans-serif; font-weight:700; font-size:15px;
  letter-spacing:.1em; text-transform:uppercase; display:flex; justify-content:space-between;
  align-items:center; gap:12px; border-top:2px solid currentColor; padding-top:14px}}
a.dl{{border:2px solid var(--ink); color:var(--ink)}}
a.dl:hover{{color:var(--ink)}}
a.dl.main{{border-color:var(--deep); color:var(--paper)}}
a.dl.main:hover{{color:var(--paper)}}

.files{{display:grid; gap:0}}
.files a{{display:flex; justify-content:space-between; align-items:baseline; gap:18px;
  border:0; border-bottom:1px solid var(--paper-3); padding:15px 0; color:var(--ink);
  font-size:clamp(15px,1.1vw,17.5px)}}
.files a:hover{{background:var(--ink); color:var(--paper); padding-inline:12px}}
.files a span:last-child{{font-variant-numeric:tabular-nums; color:var(--ink-2); flex:none}}
.files a:hover span:last-child{{color:var(--paper-3)}}

/* ---------- pie ---------- */
footer{{border-top:5px solid var(--ink); padding:clamp(40px,5vw,72px) 0 clamp(56px,6vw,88px)}}
footer .wrap{{display:flex; justify-content:space-between; gap:26px; flex-wrap:wrap;
  align-items:flex-end}}
footer p{{color:var(--ink-2); font-size:15.5px; max-width:44ch}}

/* ---------- responsive + impresión ---------- */
@media (max-width:720px){{
  .head{{grid-template-columns:1fr; gap:10px}}
  .head .n{{font-size:clamp(46px,15vw,74px)}}
}}
@media print{{
  body{{background:#fff; font-size:10.5pt}}
  section{{break-inside:avoid; padding:26pt 0; border-top:3pt solid #000}}
  .plate{{padding:14pt; break-inside:avoid}}
  a{{border:0; color:#000}}
  .top,.no-print{{display:none}}
  h1{{font-size:44pt}} h2{{font-size:30pt}}
}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
"""

HEAD = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="/assets/social/og-1200x630.png">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon/favicon.ico" sizes="any">
<link rel="icon" href="/assets/favicon/icon-cuadrado.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/favicon/apple-touch-icon.png">
<link rel="manifest" href="/assets/favicon/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=Manrope:wght@400;500;600;700&display=swap">
<style>{css}</style>"""

def top(active):
    def a(href, txt, cur):
        cu = ' aria-current="page"' if cur else ''
        return f'<a href="{href}"{cu}>{txt}</a>'
    marca = simbolo_nav()
    return f"""<header class="top"><div class="wrap">
      <a class="brand" href="/">{marca}<span>Zunox · Kit de marca</span></a>
      <nav class="nav" aria-label="Secciones">
        {a('/', 'Descargas', active == 'dl')}{a('/manual', 'Manual', active == 'man')}
      </nav>
    </div></header>"""

JUMP_MAN = """<a class="jump" href="/manual">
  <div><span class="k">Siguiente</span>
  <span class="t">Manual de<br>identidad</span>
  <p class="d">Cuánto aire necesita el logo, a partir de qué tamaño deja de leerse,
  qué versión va sobre cada fondo y qué no se hace nunca.</p></div>
  <span class="arrow" aria-hidden="true">&rarr;</span></a>"""

JUMP_DL = """<a class="jump" href="/">
  <div><span class="k">Siguiente</span>
  <span class="t">Descargar<br>los archivos</span>
  <p class="d">Logos, imprenta, favicon, redes, color y tipografías. Sueltos o en un
  único ZIP.</p></div>
  <span class="arrow" aria-hidden="true">&rarr;</span></a>"""

FOOT = """<footer><div class="wrap">
  <p><b>Zunox · Agencia de IA.</b> ¿Necesitas un formato que no está aquí?
  Pídelo antes de convertir un archivo por tu cuenta.</p>
  <p class="lab" style="color:var(--ink-2)">brandkit.zunox.es</p>
</div></footer>"""

# ================================================================== LANDING
PACKS = [
    ("zunox-logos-svg.zip",  "Logos SVG",    "svg",     "El maestro. Web, presentaciones, cualquier cosa digital."),
    ("zunox-imprenta.zip",   "Imprenta",     "pdf",     "PDF y EPS vectoriales. Esto es lo que mandas a la imprenta o al rotulista."),
    ("zunox-logos-png.zip",  "Logos PNG",    "png",     "512 a 4096 px con fondo transparente, para sistemas que no admiten vectores."),
    ("zunox-favicon.zip",    "Favicon",      "favicon", "favicon.ico, apple-touch-icon, iconos Android y el webmanifest listo."),
    ("zunox-redes.zip",      "Redes",        "social",  "Avatar, Open Graph, portadas de LinkedIn, X y YouTube."),
    ("zunox-fuentes.zip",    "Tipografías",  "fonts",   "Sora y Manrope variables con su licencia OFL, para autoalojar."),
    ("zunox-color.zip",      "Color",        "color",   "Paleta en JSON, tokens CSS, config de Tailwind y las equivalencias CMYK."),
]

SUELTOS = [
    ("assets/svg/zunox-principal-oscuro.svg", "Logo principal · fondo oscuro"),
    ("assets/svg/zunox-principal-claro.svg",  "Logo principal · fondo claro"),
    ("assets/svg/zunox-compacto-oscuro.svg",  "Logo compacto · fondo oscuro"),
    ("assets/svg/zunox-simbolo-oscuro.svg",   "Símbolo suelto"),
    ("assets/pdf/zunox-principal-oscuro.pdf", "Logo principal · PDF imprenta"),
    ("assets/favicon/favicon.ico",            "favicon.ico (16/32/48)"),
    ("assets/social/og-1200x630.png",         "Open Graph 1200 × 630"),
    ("assets/color/tokens.css",               "Tokens CSS"),
    ("assets/color/paleta.md",                "Paleta con CMYK y Pantone"),
]

def landing():
    total = sum(len(f) for _, _, f in os.walk(os.path.join(R, "assets")))
    packs = "".join(f"""<a class="dl" href="/descargas/{z}" download>
        <div><h3>{n}</h3><p class="meta" style="margin-top:9px">{d}</p></div>
        <div class="go"><span>{count(sub)} archivos</span><span>{size('descargas/'+z)} ↓</span></div></a>"""
        for z, n, sub, d in PACKS)
    sueltos = "".join(f'<a href="/{p}" download><span>{n}</span><span>{size(p)}</span></a>'
                      for p, n in SUELTOS)
    return f"""<!--zunox-->{HEAD.format(title='Kit de marca Zunox', css=CSS,
      desc='Descarga los logos, colores y tipografías de Zunox. Vectores, PNG, favicon y material para imprenta.')}
{top('dl')}
<main>
<section style="padding-top:clamp(40px,5vw,80px)">
  <div class="wrap">
    <div class="head" style="margin-bottom:clamp(28px,3.5vw,48px)">
      <p class="lab" style="padding-top:.7em">Descargas</p>
      <div class="t">
        <h1>Kit de<br>marca</h1>
        <p class="lead">Los logos, el color y las tipografías de Zunox, en los formatos
        que vas a necesitar. Descarga lo que te haga falta y sigue el manual.</p>
      </div>
    </div>
    <div class="plate hero">{svg('assets/svg/zunox-principal-oscuro.svg')}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head">
      <p class="n">01</p>
      <div class="t"><h2>Descarga</h2>
      <p class="lead">Si no sabes cuál coger, coge el kit completo.</p></div>
    </div>
    <div class="hero-dl" style="margin-bottom:clamp(20px,2.5vw,32px)">
      <a class="dl main" href="/descargas/zunox-kit-completo.zip" download style="grid-column:1/-1">
        <div><h3>Kit completo</h3>
        <p class="meta" style="margin-top:11px">Los {total} archivos: vectores, PNG,
        imprenta, favicon, redes, color y tipografías.</p></div>
        <div class="go"><span>{total} archivos</span><span>{size('descargas/zunox-kit-completo.zip')} ↓</span></div></a>
    </div>
    <div class="hero-dl">{packs}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head">
      <p class="n">02</p>
      <div class="t"><h2>Qué uso<br>para qué</h2>
      <p class="lead">La pregunta que siempre acaba llegando por WhatsApp.</p></div>
    </div>
    <div class="scroll"><table>
      <thead><tr><th>Necesito</th><th>Uso este archivo</th><th>Por qué</th></tr></thead>
      <tbody>
        <tr><td class="k">Web, app, email</td><td>SVG <span style="color:var(--ink-2)">-oscuro / -claro</span></td><td>Nítido a cualquier tamaño y pesa nada.</td></tr>
        <tr><td class="k">Imprenta, rótulo, merch</td><td>PDF</td><td>Vectorial y con color controlado. Nunca mandes PNG.</td></tr>
        <tr><td class="k">Proveedor antiguo</td><td>EPS</td><td>Para software que no abre PDF ni SVG.</td></tr>
        <tr><td class="k">Sistema sin vectores</td><td>PNG del mayor tamaño que quepa</td><td>Fondo transparente, sin recomprimir.</td></tr>
        <tr><td class="k">Favicon del sitio</td><td>favicon.ico + webmanifest</td><td>Probado a 16, 32 y 48 px de verdad.</td></tr>
        <tr><td class="k">Avatar de redes</td><td>social/avatar-400.png</td><td>El símbolo centrado y con el aire correcto.</td></tr>
        <tr><td class="k">Serigrafía o bordado</td><td>SVG <span style="color:var(--ink-2)">-blanco / -negro</span></td><td>Una sola tinta, sin degradados.</td></tr>
      </tbody></table></div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head">
      <p class="n">03</p>
      <div class="t"><h2>Archivos<br>sueltos</h2>
      <p class="lead">Los más pedidos, sin descomprimir nada.</p></div>
    </div>
    <div class="files">{sueltos}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head">
      <p class="n">04</p>
      <div class="t"><h2>Antes de<br>usarlo</h2></div>
    </div>
    <div class="g2">
      <div class="body-col">
        <p><b>Lee el manual antes de usarlo.</b> Son diez minutos y evitan el 90 % de los
        errores: cuánto aire necesita el logo, a partir de qué tamaño deja de leerse y
        qué versión va sobre cada fondo.</p>
      </div>
      <div class="body-col">
        <p><b>El verde de marca no vale para texto sobre blanco.</b> {BRIGHT} tiene
        2,13 de contraste: es ilegible. Para texto y enlaces sobre fondo claro usa
        {GREEN}, que pasa AA con 5,68. Es el mismo tono, solo más oscuro.</p>
        <p><b>Los Pantone son orientativos.</b> Confírmalos con una guía física antes de
        mandar a imprenta, y pide prueba impresa si la tirada es grande.</p>
      </div>
    </div>
    {JUMP_MAN}
  </div>
</section>
</main>
{FOOT}"""

# ================================================================== MANUAL
def sw(c):
    return f"""<div class="sw"><div class="chip" style="background:{c['hex']}"></div>
      <dl><dt>{c['nombre']}</dt>
      <dd>{c['hex']} · rgb {' '.join(str(v) for v in c['rgb'])}</dd>
      <dd>cmyk {' '.join(str(v) for v in c['cmyk'])}{' · pms ' + c['pantone_aprox'] if c['pantone_aprox'] else ''}</dd>
      <dd class="use">{c['uso']}</dd></dl></div>"""

def item(path, title, desc, mark=None, plate=""):
    m = f'<p class="mark" style="margin-bottom:6px">{mark}</p>' if mark else ""
    return (f'<div class="item"><div class="plate {plate}">{svg(path)}</div>'
            f'{m}<h3>{title}</h3><p>{desc}</p></div>')

CONTRASTES = [("ink", "ground"), ("g500", "ground"), ("g400", "ground"), ("muted", "ground"),
              ("ground", "paper"), ("g700", "paper"), ("g500", "paper"), ("deep", "paper")]

def contraste():
    out = []
    for f, b in CONTRASTES:
        cf, cb = col(f), col(b)
        nf = next(c for c in PAL if c["token"] == f)["nombre"]
        nb = next(c for c in PAL if c["token"] == b)["nombre"]
        v = cr(cf, cb)
        g = "AAA" if v >= 7 else ("AA" if v >= 4.5 else ("AA grande" if v >= 3 else "No"))
        cls = "pos" if v >= 4.5 else "neg"
        uso = ("Texto normal y grande" if v >= 4.5 else
               ("Solo texto grande o gráficos" if v >= 3 else "No usar para texto"))
        out.append(f'<tr><td class="k">{nf}</td><td style="color:var(--ink-2)">{cf}</td>'
                   f'<td>{nb}</td><td class="n">{v:.2f}</td><td class="{cls}">{g}</td>'
                   f'<td style="white-space:normal">{uso}</td></tr>')
    return "".join(out)

MALOS = [("estirar", "No lo estires ni lo comprimas"),
         ("rotar", "No lo gires: va siempre horizontal"),
         ("recolor", "No lo recolorees fuera del kit"),
         ("contraste", "No lo dejes sin contraste"),
         ("fondo", "Sobre ruido, usa la versión de una tinta"),
         ("sombra", "Sin sombras, biseles ni contornos"),
         ("desmontar", "No separes la Z ni la repitas al lado")]

def manual():
    swatches = "".join(sw(c) for c in PAL)
    malos = "".join(f'<div class="item"><div class="plate tight">{svg(f"diagramas/no/no-{k}.svg")}</div>'
                    f'<p class="mark" style="color:#B4341B;margin-bottom:5px">No</p>'
                    f'<p style="font-size:clamp(15px,1.05vw,17px);line-height:1.45">{t}</p></div>'
                    for k, t in MALOS)
    return f"""<!--zunox-->{HEAD.format(title='Manual de identidad Zunox', css=CSS,
      desc='Cómo se construye la marca Zunox: símbolo, bloqueos, aire, color, tipografía y usos prohibidos.')}
{top('man')}
<main>

<section style="padding-top:clamp(40px,5vw,80px)">
  <div class="wrap">
    <div class="head" style="margin-bottom:clamp(28px,3.5vw,48px)">
      <p class="lab" style="padding-top:.7em">Identidad · v1.0</p>
      <div class="t">
        <h1>Manual<br>de marca</h1>
        <p class="lead">Cómo se construye Zunox, dónde se pone y qué no se hace nunca.
        Nueve capítulos. Diez minutos.</p>
      </div>
    </div>
    <div class="plate hero">{svg('assets/svg/zunox-principal-oscuro.svg')}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head"><p class="n">01</p>
      <div class="t"><h2>El<br>símbolo</h2>
      <p class="lead">La Z <b>es</b> la primera letra de ZUNOX. No es un icono que se pone
      al lado: donde ves la palabra, ya ves el símbolo.</p></div></div>
    <figure><div class="plate">{svg('diagramas/construccion.svg')}</div>
      <figcaption>Retícula de 10 × 10. Todas las medidas son proporcionales a la altura
      de la caja alta, así que la construcción se mantiene a cualquier escala.</figcaption></figure>
    <div class="rule"></div>
    <div class="g2" style="align-items:start">
      <div class="body-col">
        <h3 style="margin-bottom:.2em">La ranura es el sistema</h3>
        <p>El corte diagonal no es decoración. Es el gesto que se repite en las tres letras
        con carácter y hace que se lean como una familia y no como tres dibujos sueltos.</p>
        <p>En la <b>Z</b> separa las barras del trazo diagonal. En la <b>O</b> son dos ranuras
        radiales, a 180° y a −22°. En la <b>X</b> el palo descendente pasa entero y corta al
        ascendente.</p>
      </div>
      <div class="scroll"><table>
        <thead><tr><th>Parámetro</th><th>Valor</th></tr></thead>
        <tbody>
          <tr><td class="k">Altura de caja alta</td><td class="n">100</td></tr>
          <tr><td class="k">Ancho del símbolo</td><td class="n">94</td></tr>
          <tr><td class="k">Grosor de barra</td><td class="n">20,5</td></tr>
          <tr><td class="k">Trazo diagonal</td><td class="n">24,5</td></tr>
          <tr><td class="k">Ranura (horizontal)</td><td class="n">10,8</td></tr>
          <tr><td class="k">Inclinación del remate</td><td class="n">0,62</td></tr>
        </tbody></table></div>
    </div>
    <div class="plate" style="margin-top:clamp(26px,3vw,44px)">{svg('diagramas/sistema.svg')}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head"><p class="n">02</p>
      <div class="t"><h2>Cuatro<br>bloqueos</h2>
      <p class="lead">Cada uno con su sitio. No inventes otros: si ninguno encaja,
      usa el compacto.</p></div></div>
    <div class="g2">
      {item('assets/svg/zunox-principal-oscuro.svg','Principal','Con bajada. Web, cabeceras de propuesta, firma de correo, presentaciones.','01')}
      {item('assets/svg/zunox-compacto-oscuro.svg','Compacto','Sin bajada. Barras de navegación, pies de página, cualquier sitio con poca altura.','02')}
      {item('assets/svg/zunox-vertical-oscuro.svg','Vertical','Formatos cuadrados o verticales: redes, cartelería, merchandising.','03')}
      {item('assets/svg/zunox-simbolo-oscuro.svg','Símbolo','Solo la Z. Favicon, avatar, app, sello, marca de agua.','04')}
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head"><p class="n">03</p>
      <div class="t"><h2>El aire</h2>
      <p class="lead">Alrededor del logo tiene que haber un margen libre de <b>X</b>,
      donde X = 0,55 × la altura de la caja alta. Ahí no entra nada.</p></div></div>
    <figure><div class="plate">{svg('diagramas/respeto.svg')}</div>
      <figcaption>Ni texto, ni fotos, ni el borde del soporte. El margen es proporcional,
      así que se calcula solo al escalar.</figcaption></figure>
    <div class="rule"></div>
    <figure><div class="plate">{svg('diagramas/minimos.svg')}</div>
      <figcaption>Por debajo de estos anchos la ranura se cierra y el logo deja de leerse.
      Si necesitas ir más pequeño, usa el símbolo.</figcaption></figure>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head"><p class="n">04</p>
      <div class="t"><h2>Sobre<br>cualquier<br>fondo</h2>
      <p class="lead">Cinco versiones. Las de una tinta existen porque la serigrafía,
      el bordado y el grabado no admiten más.</p></div></div>
    <div class="g3">
      {item('assets/svg/zunox-compacto-oscuro.svg','Fondo oscuro','El uso por defecto.','01')}
      {item('assets/svg/zunox-compacto-claro.svg','Fondo claro','Tinta Zunox Deep sobre papel.','02',plate='paper')}
      {item('assets/svg/zunox-compacto-blanco.svg','Negativo','Una tinta blanca, sobre foto o color plano.','03')}
      {item('assets/svg/zunox-compacto-negro.svg','Positivo','Una tinta oscura: facturas, sellos, fax.','04',plate='white')}
      {item('assets/svg/zunox-compacto-verde.svg','Monocromo verde','Marcas de agua y usos sutiles.','05')}
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head"><p class="n">05</p>
      <div class="t"><h2>Color</h2>
      <p class="lead">El azul verdoso {DEEP} es el color de marca. El verde {BRIGHT} es
      el acento: la X del logo, los botones y poco más. Si lo usas en todo, deja de destacar.</p></div></div>
    <div class="g3">{swatches}</div>
    <div class="rule"></div>
    <h3 style="margin-bottom:clamp(18px,2vw,28px)">Contraste comprobado</h3>
    <div class="scroll"><table>
      <thead><tr><th>Color</th><th></th><th>Sobre</th><th>Ratio</th><th>WCAG</th><th>Se puede usar para</th></tr></thead>
      <tbody>{contraste()}</tbody></table></div>
    <p class="lead" style="margin-top:clamp(22px,2.5vw,34px);max-width:44ch">
      El verde de marca es precioso sobre oscuro e <b>ilegible sobre blanco</b>. Para texto
      y enlaces sobre fondo claro está {GREEN}: mismo tono, más oscuro, y pasa AA.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head"><p class="n">06</p>
      <div class="t"><h2>Tipografía</h2>
      <p class="lead">Sora para titular, Manrope para leer. Las dos variables, gratuitas
      y autoalojables.</p></div></div>
    <div class="plate" style="display:block;padding:clamp(30px,5vw,72px)">
      <p style="font-family:Sora,sans-serif;font-weight:700;text-transform:uppercase;
        letter-spacing:-.04em;line-height:.9;color:{PAPER};font-size:clamp(44px,9vw,124px);margin:0">Sora</p>
      <p style="font-family:Sora,sans-serif;font-weight:600;letter-spacing:-.03em;
        line-height:1.02;color:{PAPER};font-size:clamp(24px,4.2vw,58px);margin:.35em 0 0">Inteligencia artificial.<br>Resultados reales.</p>
      <p style="font-family:Sora,sans-serif;color:{BRIGHT};font-size:clamp(13px,1.1vw,17px);
        letter-spacing:.06em;margin:1.4em 0 0">ABCDEFGHIJKLMNÑOPQRSTUVWXYZ abcdefghijklmnñopqrstuvwxyz 0123456789 áéíóú ¿? ¡!</p>
    </div>
    <div class="plate paper" style="display:block;padding:clamp(30px,5vw,72px);margin-top:clamp(16px,2vw,26px)">
      <p style="font-family:Manrope,sans-serif;font-weight:700;letter-spacing:-.035em;
        line-height:.9;font-size:clamp(44px,9vw,124px);margin:0">Manrope</p>
      <p style="font-family:Manrope,sans-serif;font-size:clamp(17px,1.6vw,23px);line-height:1.55;
        max-width:52ch;margin:.7em 0 0">Automatizamos procesos, optimizamos tu negocio y diseñamos
        soluciones de IA a medida para que ahorres tiempo, reduzcas costes y aumentes ingresos.</p>
      <p style="font-family:Manrope,sans-serif;color:var(--ink-2);font-size:clamp(13px,1.1vw,17px);
        margin:1.4em 0 0">ABCDEFGHIJKLMNÑOPQRSTUVWXYZ abcdefghijklmnñopqrstuvwxyz 0123456789 áéíóú ¿? ¡!</p>
    </div>
    <div class="rule"></div>
    <div class="g2" style="align-items:start">
      <div class="body-col">
        <h3 style="margin-bottom:.2em">El logo no usa estas fuentes</h3>
        <p>Las cinco letras de ZUNOX son curvas dibujadas a medida. Nunca escribas
        «ZUNOX» con Sora y lo llames logo: coge el archivo del kit.</p>
        <p>Las dos familias llevan licencia SIL Open Font: puedes usarlas en web,
        impresión y productos de cliente sin pagar nada.</p>
      </div>
      <div class="scroll"><table>
        <thead><tr><th>Nivel</th><th>Tamaño</th><th>Familia</th><th>Interlineado</th><th>Tracking</th></tr></thead>
        <tbody>
          <tr><td class="k">Display</td><td class="n">56–72 px</td><td>Sora 700</td><td class="n">1,05</td><td class="n">−0,02em</td></tr>
          <tr><td class="k">H1</td><td class="n">40 px</td><td>Sora 600</td><td class="n">1,10</td><td class="n">−0,02em</td></tr>
          <tr><td class="k">H2</td><td class="n">30 px</td><td>Sora 600</td><td class="n">1,20</td><td class="n">−0,015em</td></tr>
          <tr><td class="k">H3</td><td class="n">22 px</td><td>Sora 600</td><td class="n">1,30</td><td class="n">−0,01em</td></tr>
          <tr><td class="k">Cuerpo</td><td class="n">16–17 px</td><td>Manrope 400</td><td class="n">1,65</td><td class="n">0</td></tr>
          <tr><td class="k">Etiqueta</td><td class="n">11,5 px</td><td>Sora 600 mayús.</td><td class="n">1,40</td><td class="n">+0,16em</td></tr>
        </tbody></table></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head"><p class="n">07</p>
      <div class="t"><h2>Lo que<br>no se<br>hace</h2>
      <p class="lead">Si dudas, usa un archivo del kit tal cual viene: están hechos
      precisamente para no tener que decidir.</p></div></div>
    <div class="g2" style="margin-bottom:clamp(20px,2.5vw,34px)">
      <div class="item" style="grid-column:span 1">
        <div class="plate tight">{svg('diagramas/no/no-ok.svg')}</div>
        <p class="mark" style="margin-bottom:5px">Sí</p>
        <p style="font-size:clamp(15px,1.05vw,17px);line-height:1.45">Proporciones, colores y aire del kit.</p>
      </div>
    </div>
    <div class="g3">{malos}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head"><p class="n">08</p>
      <div class="t"><h2>Icono<br>y redes</h2>
      <p class="lead">El favicon lleva menos margen que el logo normal para que la Z ocupe
      todo lo posible a 16 px. Está probado a cada tamaño real.</p></div></div>
    <div class="g4">
      <div class="item"><div class="plate tight"><img src="/assets/favicon/apple-touch-icon.png" alt="Icono de app para iOS" style="max-width:150px"></div><p class="mark">apple-touch · 180</p></div>
      <div class="item"><div class="plate tight"><img src="/assets/favicon/android-chrome-512.png" alt="Icono de app para Android" style="max-width:150px"></div><p class="mark">android · 192 · 512</p></div>
      <div class="item"><div class="plate tight"><img src="/assets/favicon/android-maskable-512.png" alt="Icono maskable de Android" style="max-width:150px"></div><p class="mark">maskable · 80 %</p></div>
      <div class="item"><div class="plate tight"><img src="/assets/social/avatar-400.png" alt="Avatar para redes sociales" style="max-width:150px"></div><p class="mark">avatar · 400 · 1000</p></div>
    </div>
    <div class="rule"></div>
    <figure><div class="plate tight"><img src="/assets/social/og-1200x630.png" alt="Imagen Open Graph de Zunox" style="max-width:920px"></div>
      <figcaption>Open Graph 1200 × 630 — lo que se ve al compartir zunox.es en WhatsApp,
      LinkedIn o Slack.</figcaption></figure>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head"><p class="n">09</p>
      <div class="t"><h2>Los<br>archivos</h2>
      <p class="lead">Para web usa SVG. Para imprenta, PDF. PNG solo cuando el sistema
      no admita vectores.</p></div></div>
    <div class="scroll"><table>
      <thead><tr><th>Carpeta</th><th>Contiene</th><th>Cuándo</th></tr></thead>
      <tbody>
        <tr><td class="k">svg/</td><td class="n">{count('svg')} archivos</td><td style="white-space:normal">El maestro. Web, app, email, presentaciones.</td></tr>
        <tr><td class="k">pdf/</td><td class="n">{count('pdf')} archivos</td><td style="white-space:normal">Imprenta, rotulación, merchandising.</td></tr>
        <tr><td class="k">eps/</td><td class="n">{count('eps')} archivos</td><td style="white-space:normal">Proveedores con software antiguo.</td></tr>
        <tr><td class="k">png/</td><td class="n">{count('png')} archivos</td><td style="white-space:normal">512 a 4096 px, fondo transparente.</td></tr>
        <tr><td class="k">favicon/</td><td class="n">{count('favicon')} archivos</td><td style="white-space:normal">Web e iconos de app.</td></tr>
        <tr><td class="k">social/</td><td class="n">{count('social')} archivos</td><td style="white-space:normal">Avatares, portadas y Open Graph.</td></tr>
        <tr><td class="k">color/</td><td class="n">{count('color')} archivos</td><td style="white-space:normal">Tokens para desarrollo y valores para imprenta.</td></tr>
        <tr><td class="k">fonts/</td><td class="n">{count('fonts')} archivos</td><td style="white-space:normal">Sora y Manrope con licencia OFL.</td></tr>
      </tbody></table></div>
    <div class="rule"></div>
    <div class="g2" style="align-items:start">
      <div class="body-col">
        <p><b>No conviertas archivos por tu cuenta.</b> Pasar un PNG a vector o recortar
        un logo a mano estropea las proporciones y las ranuras. Si te falta un formato,
        pídelo: se prepara en un momento y sale correcto.</p>
      </div>
      <div class="body-col">
        <p><b>Usa siempre el archivo, no lo redibujes.</b> Tampoco lo reconstruyas
        escribiendo «ZUNOX» con una fuente parecida.</p>
      </div>
    </div>
    {JUMP_DL}
  </div>
</section>
</main>
{FOOT}"""

if __name__ == "__main__":
    open(os.path.join(R, "index.html"), "w").write(landing())
    open(os.path.join(R, "manual.html"), "w").write(manual())
    print("index.html", os.path.getsize(os.path.join(R, "index.html")))
    print("manual.html", os.path.getsize(os.path.join(R, "manual.html")))
