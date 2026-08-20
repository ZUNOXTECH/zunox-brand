"""Diagramas técnicos del manual: construcción, área de respeto, tamaño mínimo."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import zx, brand, final
from brand import C

OUT = os.path.join(os.path.dirname(__file__), "..", "diagramas")
os.makedirs(OUT, exist_ok=True)
GUIDE, LABEL = C["line"], C["g400"]

def txt(x, y, s, anchor="middle", size=11, fill=None, weight=400):
    return (f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" '
            f'font-family="ui-monospace,Menlo,monospace" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill or LABEL}">{s}</text>')

def dim(x1, y1, x2, y2, label, off=0):
    """Cota con extremos."""
    tick = 4
    if y1 == y2:
        g = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GUIDE}" stroke-width="1"/>'
             f'<line x1="{x1}" y1="{y1-tick}" x2="{x1}" y2="{y1+tick}" stroke="{GUIDE}" stroke-width="1"/>'
             f'<line x1="{x2}" y1="{y2-tick}" x2="{x2}" y2="{y2+tick}" stroke="{GUIDE}" stroke-width="1"/>')
        return g + txt((x1+x2)/2, y1-7+off, label)
    g = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GUIDE}" stroke-width="1"/>'
         f'<line x1="{x1-tick}" y1="{y1}" x2="{x1+tick}" y2="{y1}" stroke="{GUIDE}" stroke-width="1"/>'
         f'<line x1="{x2-tick}" y1="{y2}" x2="{x2+tick}" y2="{y2}" stroke="{GUIDE}" stroke-width="1"/>')
    return g + txt(x1-9+off, (y1+y2)/2+4, label, anchor="end")

def construccion():
    cap = 260.0
    ps, w, h = brand.Zpaths(cap)
    L, T, R, B = 118.0, 70.0, 190.0, 54.0
    k = cap/100.0
    bar = brand.ZP["bar"]*k
    W, H = L + w + R, T + h + B
    g = [f'<rect width="100%" height="100%" fill="{C["ground"]}"/>']
    for i in range(11):
        o = 0.30 if i % 5 else 0.62
        g.append(f'<line x1="{L+i*w/10:.2f}" y1="{T}" x2="{L+i*w/10:.2f}" y2="{T+h}" '
                 f'stroke="{GUIDE}" stroke-width=".7" opacity="{o}"/>')
        g.append(f'<line x1="{L}" y1="{T+i*h/10:.2f}" x2="{L+w}" y2="{T+i*h/10:.2f}" '
                 f'stroke="{GUIDE}" stroke-width=".7" opacity="{o}"/>')
    g.append(f'<g transform="translate({L},{T})">' +
             "".join(f'<path d="{x}" fill="{C["ink"]}"/>' for x in ps) + '</g>')
    g.append(dim(L, T+h+30, L+w, T+h+30, f"ancho {brand.ZP['W']:.0f}", off=20))
    g.append(dim(L-40, T, L-40, T+h, "alto 100"))
    # barra
    g.append(f'<line x1="{L+w+16}" y1="{T}" x2="{L+w+16}" y2="{T+bar}" stroke="{GUIDE}" stroke-width="1"/>'
             f'<line x1="{L+w+12}" y1="{T}" x2="{L+w+20}" y2="{T}" stroke="{GUIDE}" stroke-width="1"/>'
             f'<line x1="{L+w+12}" y1="{T+bar}" x2="{L+w+20}" y2="{T+bar}" stroke="{GUIDE}" stroke-width="1"/>')
    g.append(txt(L+w+28, T+bar/2+4, f"barra {brand.ZP['bar']}", anchor="start"))
    g.append(txt(L+w+28, T+h*0.50, f"diagonal {brand.ZP['dw']}", anchor="start"))
    g.append(txt(L+w+28, T+h*0.50+18, f"ranura {brand.ZP['gap_h']}", anchor="start"))
    g.append(txt(L+w+28, T+h*0.50+36, "remate  0,62", anchor="start"))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">{"".join(g)}</svg>'

def respeto():
    cap = 120.0
    s, w, h = final.build("principal", C["ink"], C["g500"], C["g400"], cap=cap, pad=0.0)
    body = s[s.index(">", s.index("<svg"))+1:s.rindex("</svg>")]
    m = cap*0.55
    P = m + 46
    W, H = w + 2*P, h + 2*P
    g = [f'<rect width="100%" height="100%" fill="{C["ground"]}"/>',
         f'<rect x="{P-m}" y="{P-m}" width="{w+2*m}" height="{h+2*m}" fill="none" '
         f'stroke="{GUIDE}" stroke-width="1.2" stroke-dasharray="7 5"/>',
         f'<rect x="{P}" y="{P}" width="{w}" height="{h}" fill="none" '
         f'stroke="{GUIDE}" stroke-width=".8" opacity=".55"/>',
         f'<g transform="translate({P},{P})">{body}</g>']
    for (x, y) in ((P-m, P-m), (P+w, P-m), (P-m, P+h), (P+w, P+h)):
        g.append(f'<rect x="{x}" y="{y}" width="{m}" height="{m}" fill="{C["g500"]}" opacity=".14"/>')
    g.append(dim(P-m, P-m-16, P, P-m-16, "X"))
    g.append(txt(P+w/2, H-18, "X = 0,55 × la altura de la caja alta", size=12))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">{"".join(g)}</svg>'

def minimos():
    rows = [("principal", 140, "140 px  ·  36 mm"),
            ("compacto",   90, "90 px  ·  22 mm"),
            ("simbolo",    24, "24 px  ·  7 mm")]
    W, H, x = 640, 190, 40
    g = [f'<rect width="100%" height="100%" fill="{C["ground"]}"/>']
    for kind, px, label in rows:
        s, w, h = final.build(kind, C["ink"], C["g500"], C["g400"], pad=0.0)
        body = s[s.index(">", s.index("<svg"))+1:s.rindex("</svg>")]
        k = px/w
        y = 66 - h*k/2
        g.append(f'<g transform="translate({x},{y:.2f}) scale({k:.5f})">{body}</g>')
        g.append(txt(x, 128, label, anchor="start", size=11.5))
        g.append(txt(x, 146, kind, anchor="start", size=10, fill=C["muted"]))
        x += px + 76
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{"".join(g)}</svg>'

def sistema():
    """La ranura como sistema: Z, O y X."""
    import word
    cap = 130.0
    k = cap/100.0
    zp, zw, zh = brand.Zpaths(cap)
    op, ow = word.O(); xp, xw = word.X()
    items = [("Z", "ranura diagonal", zp, zw, C["ink"], 1.0),
             ("O", "dos ranuras radiales", op, ow*k, C["ink"], k),
             ("X", "corte del palo ascendente", xp, xw*k, C["g500"], k)]
    gap, PAD, TOP = 84.0, 52.0, 38.0
    g = [f'<rect width="100%" height="100%" fill="{C["ground"]}"/>']
    x = PAD
    for letra, label, paths, w, col, sc in items:
        inner = "".join(f'<path d="{d}" fill="{col}"/>' for d in paths)
        g.append(f'<g transform="translate({x:.2f},{TOP}) scale({sc:.6f})">{inner}</g>')
        g.append(txt(x + w/2, TOP+cap+32, letra, size=13, fill=C["g400"], weight=500))
        g.append(txt(x + w/2, TOP+cap+50, label, size=11, fill=C["muted"]))
        x += w + gap
    W, H = x - gap + PAD, TOP + cap + 62
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">{"".join(g)}</svg>'

if __name__ == "__main__":
    for n, f in (("construccion", construccion), ("respeto", respeto),
                 ("minimos", minimos), ("sistema", sistema)):
        open(os.path.join(OUT, n + ".svg"), "w").write(f())
        zx.png(os.path.join(OUT, n + ".svg"), os.path.join(OUT, n + ".png"), width=900)
    print("diagramas ok")
