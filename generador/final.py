"""Genera todas las artes finales del kit Zunox en 02-final/."""
import sys, os, json, subprocess, math
sys.path.insert(0, os.path.dirname(__file__))
import zx, word, brand
from brand import C

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
def d(*p):
    q = os.path.join(ROOT, *p); os.makedirs(q, exist_ok=True); return q

# ---------------------------------------------------------------- lockups
def build(kind, fill, accent, muted, cap=100.0, pad=0.55):
    """Devuelve (svg_string, w, h) con margen de respeto incluido."""
    if kind == "simbolo":
        ps, w, h = brand.Zpaths(cap)
        body = "".join(f'<path d="{x}" fill="{fill}"/>' for x in ps)
    else:
        wm, w, h = brand.wordmark(cap, fill=fill, accent=accent)
        if kind == "compacto":
            body = wm
        elif kind == "principal":
            tg, tw = brand.tagline(w, cap*0.185, muted)
            body = f'{wm}<g transform="translate(0,{h+cap*0.42:.3f})">{tg}</g>'
            h = h + cap*0.42 + cap*0.185
        elif kind == "vertical":
            zc = cap*1.75
            zp, zw, zh = brand.Zpaths(zc)
            zg = "".join(f'<path d="{x}" fill="{fill}"/>' for x in zp)
            tg, tw = brand.tagline(w, cap*0.185, muted)
            W = max(zw, w)
            body = (f'<g transform="translate({(W-zw)/2:.3f},0)">{zg}</g>'
                    f'<g transform="translate({(W-w)/2:.3f},{zh+cap*0.52:.3f})">{wm}</g>'
                    f'<g transform="translate({(W-tw)/2:.3f},{zh+cap*0.52+h+cap*0.42:.3f})">{tg}</g>')
            w, h = W, zh + cap*0.52 + h + cap*0.42 + cap*0.185
        else:
            raise ValueError(kind)
    m = cap*pad
    return (zx.svg(round(w+2*m, 3), round(h+2*m, 3),
                   f'<g transform="translate({m:.3f},{m:.3f})">{body}</g>'),
            w+2*m, h+2*m)

VERSIONS = {
    "oscuro": (C["ink"],   C["g500"], C["g400"]),   # sobre fondo oscuro
    "claro":  (C["ground"], C["g500"], C["g700"]),  # sobre fondo claro
    "blanco": ("#FFFFFF",  "#FFFFFF", "#FFFFFF"),   # una tinta
    "negro":  (C["deep"],  C["deep"], C["deep"]),
    "verde":  (C["g500"],  C["g500"], C["g500"]),
}
LOCKUPS = ["principal", "compacto", "vertical", "simbolo"]

def gen_vectors():
    svgdir, pdfdir, epsdir = d("svg"), d("pdf"), d("eps")
    index = []
    for lk in LOCKUPS:
        for v, (f, a, m) in VERSIONS.items():
            s, w, h = build(lk, f, a, m)
            name = f"zunox-{lk}-{v}"
            p = os.path.join(svgdir, name + ".svg")
            open(p, "w").write(s)
            for fmt, folder in (("pdf", pdfdir), ("eps", epsdir)):
                subprocess.run(["rsvg-convert", "-f", fmt, p, "-o",
                                os.path.join(folder, f"{name}.{fmt}")], check=True)
            index.append((name, round(w, 1), round(h, 1)))
    return index

def gen_png(index):
    for name, w, h in index:
        src = os.path.join(ROOT, "svg", name + ".svg")
        for px in (512, 1024, 2048, 4096):
            out = d("png", f"{px}px")
            subprocess.run(["rsvg-convert", src, "-w", str(px), "-o",
                            os.path.join(out, f"{name}-{px}.png")], check=True)

# ---------------------------------------------------------------- iconos
def icon_svg(bg, fill, radius, size=1024, pad=0.17):
    cap = size*(1-2*pad)
    ps, w, h = brand.Zpaths(cap)
    g = "".join(f'<path d="{x}" fill="{fill}"/>' for x in ps)
    r = f'<rect width="{size}" height="{size}" rx="{radius}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
            f'viewBox="0 0 {size} {size}">{r}'
            f'<g transform="translate({(size-w)/2:.2f},{(size-h)/2:.2f})">{g}</g></svg>')

def gen_icons():
    ic = d("favicon")
    specs = {
        "icon-cuadrado":  icon_svg(C["ground"], C["ink"], 0),
        "icon-redondeado": icon_svg(C["ground"], C["ink"], 224),
        "icon-circulo":   icon_svg(C["ground"], C["ink"], 512),
        "icon-verde":     icon_svg(C["g500"], C["ground"], 224),
        "icon-maskable":  icon_svg(C["ground"], C["ink"], 0, pad=0.26),
    }
    for n, s in specs.items():
        open(os.path.join(ic, n + ".svg"), "w").write(s)
    def png(svgname, px, out):
        subprocess.run(["rsvg-convert", os.path.join(ic, svgname + ".svg"),
                        "-w", str(px), "-h", str(px), "-o", os.path.join(ic, out)], check=True)
    png("icon-cuadrado", 16, "favicon-16.png")
    png("icon-cuadrado", 32, "favicon-32.png")
    png("icon-cuadrado", 48, "favicon-48.png")
    png("icon-redondeado", 180, "apple-touch-icon.png")
    png("icon-cuadrado", 192, "android-chrome-192.png")
    png("icon-cuadrado", 512, "android-chrome-512.png")
    png("icon-maskable", 512, "android-maskable-512.png")
    from PIL import Image
    ims = [Image.open(os.path.join(ic, f"favicon-{n}.png")).convert("RGBA") for n in (48, 32, 16)]
    ims[0].save(os.path.join(ic, "favicon.ico"), format="ICO",
                sizes=[(48, 48), (32, 32), (16, 16)])
    open(os.path.join(ic, "site.webmanifest"), "w").write(json.dumps({
        "name": "Zunox", "short_name": "Zunox",
        "icons": [
            {"src": "/android-chrome-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/android-chrome-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "/android-maskable-512.png", "sizes": "512x512",
             "type": "image/png", "purpose": "maskable"}],
        "theme_color": C["ground"], "background_color": C["ground"],
        "display": "standalone"}, indent=2, ensure_ascii=False))

# ---------------------------------------------------------------- redes
def canvas(W, H, kind, bg, fill, accent, muted, scale=0.52, dy=0.0):
    inner, w, h = build(kind, fill, accent, muted, pad=0.0)
    body = inner[inner.index(">", inner.index("<svg"))+1:inner.rindex("</svg>")]
    k = (W*scale)/w
    if h*k > H*0.72:
        k = (H*0.72)/h
    x, y = (W - w*k)/2, (H - h*k)/2 + dy*H
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{bg}"/>'
            f'<g transform="translate({x:.2f},{y:.2f}) scale({k:.5f})">{body}</g></svg>')

def gen_social():
    so = d("social")
    jobs = {
        "avatar-400":            (400, 400, "simbolo", 0.62),
        "avatar-1000":           (1000, 1000, "simbolo", 0.62),
        "og-1200x630":           (1200, 630, "principal", 0.62),
        "linkedin-portada-1128x191": (1128, 191, "compacto", 0.42),
        "x-cabecera-1500x500":   (1500, 500, "principal", 0.46),
        "youtube-2560x1440":     (2560, 1440, "vertical", 0.34),
    }
    for n, (W, H, kind, sc) in jobs.items():
        s = canvas(W, H, kind, C["ground"], C["ink"], C["g500"], C["g400"], scale=sc)
        p = os.path.join(so, n + ".svg"); open(p, "w").write(s)
        subprocess.run(["rsvg-convert", p, "-w", str(W), "-h", str(H),
                        "-o", os.path.join(so, n + ".png")], check=True)

# ---------------------------------------------------------------- color
def cmyk(hexc):
    r, g, b = [int(hexc[i:i+2], 16)/255 for i in (1, 3, 5)]
    k = 1 - max(r, g, b)
    if k >= 1: return (0, 0, 0, 100)
    f = lambda v: round((1-v-k)/(1-k)*100)
    return (f(r), f(g), f(b), round(k*100))

NAMES = {
    "ground":  ("Zunox Deep",    "Color principal de marca. Fondos, cabeceras, superficies amplias."),
    "deep":    ("Zunox Ink",     "Tinta más oscura. Texto sobre claro, versión de una tinta."),
    "surface": ("Zunox Surface", "Tarjetas y bloques sobre el fondo principal."),
    "line":    ("Zunox Line",    "Filetes, bordes y separadores."),
    "g500":    ("Zunox Green",   "Verde de marca. La X del logo, botones, acentos."),
    "g700":    ("Green Deep",    "Verde para texto y enlaces sobre fondo claro (AA)."),
    "g400":    ("Green Light",   "Hover y destacados sobre fondo oscuro."),
    "ink":     ("Zunox Paper",   "Texto principal sobre fondo oscuro."),
    "muted":   ("Zunox Muted",   "Texto secundario y bajadas."),
    "paper":   ("Paper",         "Fondo claro de la marca."),
}
PANTONE = {"ground": "3165 C", "g500": "3405 C", "g700": "342 C",
           "deep": "5535 C", "g400": "344 C"}

def gen_color():
    co = d("color")
    rows = []
    for key, hexv in C.items():
        n, desc = NAMES[key]
        r, g, b = [int(hexv[i:i+2], 16) for i in (1, 3, 5)]
        rows.append({"token": key, "nombre": n, "hex": hexv, "rgb": [r, g, b],
                     "cmyk": cmyk(hexv), "pantone_aprox": PANTONE.get(key),
                     "uso": desc})
    open(os.path.join(co, "paleta.json"), "w").write(
        json.dumps({"marca": "Zunox", "colores": rows}, indent=2, ensure_ascii=False))
    css = [":root{"] + [f"  --zx-{r['token']}: {r['hex']};" for r in rows] + ["}"]
    css += ["", "/* tipografía */", ":root{",
            '  --zx-font-display: "Sora", system-ui, sans-serif;',
            '  --zx-font-body: "Manrope", system-ui, sans-serif;', "}"]
    open(os.path.join(co, "tokens.css"), "w").write("\n".join(css) + "\n")
    tw = {"theme": {"extend": {
        "colors": {"zx": {r["token"]: r["hex"] for r in rows}},
        "fontFamily": {"display": ["Sora", "system-ui", "sans-serif"],
                       "sans": ["Manrope", "system-ui", "sans-serif"]}}}}
    open(os.path.join(co, "tailwind.extend.json"), "w").write(
        json.dumps(tw, indent=2, ensure_ascii=False))
    md = ["# Paleta Zunox", "",
          "| Token | Nombre | HEX | RGB | CMYK | Pantone (aprox.) | Uso |",
          "|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| `{r['token']}` | {r['nombre']} | `{r['hex']}` | "
                  f"{', '.join(map(str, r['rgb']))} | {', '.join(map(str, r['cmyk']))} | "
                  f"{r['pantone_aprox'] or '—'} | {r['uso']} |")
    md += ["", "> Los CMYK son conversión directa sin perfil de color: pide una prueba",
           "> impresa antes de una tirada grande. Los Pantone son **orientativos** —",
           "> confírmalos con una guía física antes de mandar a imprenta."]
    open(os.path.join(co, "paleta.md"), "w").write("\n".join(md) + "\n")
    return rows

if __name__ == "__main__":
    idx = gen_vectors(); print("vectores:", len(idx))
    gen_png(idx);        print("png ok")
    gen_icons();         print("iconos ok")
    gen_social();        print("redes ok")
    rows = gen_color();  print("color ok", len(rows))
