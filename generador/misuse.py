"""Ejemplos de uso incorrecto para el manual."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import zx, brand, final
from brand import C

OUT = os.path.join(os.path.dirname(__file__), "..", "diagramas", "no")
os.makedirs(OUT, exist_ok=True)

def inner(kind="compacto", fill=None, accent=None, muted=None):
    fill = fill or C["ink"]; accent = accent or C["g500"]; muted = muted or C["g400"]
    s, w, h = final.build(kind, fill, accent, muted, pad=0.0)
    body = s[s.index(">", s.index("<svg"))+1:s.rindex("</svg>")]
    return body, w, h

def frame(content, bg=None, W=560, H=190, extra=""):
    b = f'<rect width="{W}" height="{H}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}">{extra}{b}{content}</svg>')

def place(body, w, h, W=560, H=190, sx=1.0, sy=1.0, rot=0.0, pad=0.80):
    k = min(W*pad/w, H*pad/h)/max(sx, sy, 1.0)
    kx, ky = k*sx, k*sy
    x, y = (W - w*kx)/2, (H - h*ky)/2
    t = f"translate({x:.2f},{y:.2f}) scale({kx:.5f},{ky:.5f})"
    if rot:
        t = f"rotate({rot} {W/2} {H/2}) " + t
    return f'<g transform="{t}">{body}</g>'

def main():
    b, w, h = inner()
    bad = {}
    bad["estirar"]  = frame(place(b, w, h, sx=1.45, sy=0.82), C["ground"])
    bad["rotar"]    = frame(place(b, w, h, rot=-12, pad=0.66), C["ground"])
    bad["recolor"]  = frame(place(*inner("compacto", "#FF7A45", "#F2C230", "#FF7A45")),
                            "#2B0E3A")
    bad["contraste"] = frame(place(*inner("compacto", C["ground"], C["g700"], C["ground"])),
                             C["deep"])
    # fondo ocupado -> usar la versión de una tinta
    noise = ('<defs><pattern id="p" width="26" height="26" patternUnits="userSpaceOnUse" '
             'patternTransform="rotate(35)"><rect width="26" height="26" fill="#5B6B57"/>'
             '<circle cx="7" cy="7" r="8" fill="#9AA37E"/><rect x="14" y="2" width="11" '
             'height="20" fill="#3E4A3C"/></pattern></defs>'
             '<rect width="560" height="190" fill="url(#p)"/>')
    bad["fondo"]    = frame(place(b, w, h), None, extra=noise)
    bad["sombra"]   = frame('<defs><filter id="s" x="-40%" y="-40%" width="180%" height="180%">'
                            '<feDropShadow dx="7" dy="9" stdDeviation="6" flood-color="#000" '
                            'flood-opacity=".75"/></filter></defs>'
                            f'<g filter="url(#s)">{place(b, w, h)}</g>', C["ground"])
    # el símbolo repetido al lado de la palabra
    zb, zw, zh = inner("simbolo")
    W, H = 560, 190
    kz = (H*0.62)/zh
    kw = (W*0.52)/w
    if h*kw > H*0.55: kw = (H*0.55)/h
    gapx = 26
    total = zw*kz + gapx + w*kw
    x0 = (W - total)/2
    g = (f'<g transform="translate({x0:.2f},{(H-zh*kz)/2:.2f}) scale({kz:.5f})">{zb}</g>'
         f'<g transform="translate({x0+zw*kz+gapx:.2f},{(H-h*kw)/2:.2f}) scale({kw:.5f})">{b}</g>')
    bad["desmontar"] = frame(g, C["ground"])
    ok = frame(place(b, w, h), C["ground"])
    bad["ok"] = ok
    for n, s in bad.items():
        open(os.path.join(OUT, f"no-{n}.svg"), "w").write(s)
    return list(bad)

if __name__ == "__main__":
    print(main())
