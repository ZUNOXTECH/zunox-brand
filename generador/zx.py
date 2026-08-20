"""ZUNOX brand toolkit — vector primitives."""
import math, subprocess, os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

FONTS = os.path.join(os.path.dirname(__file__), "_fonts")

# ---------------------------------------------------------------- geometry
def _norm(v):
    l = math.hypot(*v)
    return (v[0]/l, v[1]/l)

def rounded_poly(pts, r):
    """SVG path for polygon with corner radius r (scalar or per-vertex list)."""
    n = len(pts)
    rs = [r]*n if not isinstance(r, (list, tuple)) else list(r)
    d = []
    for i in range(n):
        p0, p1, p2 = pts[(i-1) % n], pts[i], pts[(i+1) % n]
        v0 = _norm((p0[0]-p1[0], p0[1]-p1[1]))
        v1 = _norm((p2[0]-p1[0], p2[1]-p1[1]))
        ang = math.acos(max(-1, min(1, v0[0]*v1[0] + v0[1]*v1[1])))
        rad = rs[i]
        if ang > 1e-6:
            tan = rad / math.tan(ang/2)
            lim = min(math.dist(p0, p1), math.dist(p1, p2)) / 2
            if tan > lim:
                tan = lim
                rad = tan * math.tan(ang/2)
        else:
            tan = 0
        a = (p1[0]+v0[0]*tan, p1[1]+v0[1]*tan)
        b = (p1[0]+v1[0]*tan, p1[1]+v1[1]*tan)
        cross = v0[0]*v1[1] - v0[1]*v1[0]
        sweep = 0 if cross > 0 else 1
        if i == 0:
            d.append(f"M{a[0]:.3f},{a[1]:.3f}")
        else:
            d.append(f"L{a[0]:.3f},{a[1]:.3f}")
        if rad > 0.01:
            d.append(f"A{rad:.3f},{rad:.3f} 0 0 {sweep} {b[0]:.3f},{b[1]:.3f}")
    d.append("Z")
    return "".join(d)

def capsule(p, q, w):
    """Round-capped stroke as a filled path."""
    ux, uy = _norm((q[0]-p[0], q[1]-p[1]))
    px, py = -uy, ux
    h = w/2
    a = (p[0]+px*h, p[1]+py*h); b = (q[0]+px*h, q[1]+py*h)
    c = (q[0]-px*h, q[1]-py*h); e = (p[0]-px*h, p[1]-py*h)
    return (f"M{a[0]:.3f},{a[1]:.3f}L{b[0]:.3f},{b[1]:.3f}"
            f"A{h:.3f},{h:.3f} 0 0 0 {c[0]:.3f},{c[1]:.3f}"
            f"L{e[0]:.3f},{e[1]:.3f}A{h:.3f},{h:.3f} 0 0 0 {a[0]:.3f},{a[1]:.3f}Z")

# ---------------------------------------------------------------- monogram
# Proportions measured from the reference art (box 142 x 143).
MW, MH = 142.0, 143.0
REF = dict(bar=25.5, dw=29.5, gap_h=13.0, slant=0.623, brow=0.732, m=-0.9315,
           e_top=4.25, e_bot=2.25)

def zmark(H=100.0, W=None, bar=None, dw=None, gap_h=None, slant=None, r=None,
          gap=True):
    """Parametric ZUNOX Z. Defaults reproduce the reference exactly (IoU .945)."""
    k = H/MH
    W     = MW*k       if W     is None else W
    bar   = REF["bar"]*k    if bar   is None else bar
    dw    = REF["dw"]*k     if dw    is None else dw
    gap_h = REF["gap_h"]*k  if gap_h is None else gap_h
    slant = REF["slant"]    if slant is None else slant
    r     = 4.0*k           if r     is None else r
    m     = REF["m"]
    h     = dw/2.0
    # diagonal: capsule tangent to the top and bottom edges
    p = (W - h - REF["e_top"]*W/MW, h)
    q = (h + REF["e_bot"]*W/MW,     H - h)
    ux, uy = _norm((q[0]-p[0], q[1]-p[1]))
    m = ux/uy
    nx, ny = -uy, ux                       # left-hand normal
    # left boundary line of the diagonal, then shifted left by gap_h
    lx, ly = p[0] + nx*h, p[1] + ny*h
    def bar_edge(y):                       # x of the top bar's right edge at y
        return lx + m*(y - ly) - (gap_h if gap else 0.0)
    top = [(0, 0), (bar_edge(0), 0), (bar_edge(bar), bar), (slant*bar, bar)]
    bot = [(W - x, H - y) for x, y in top]
    return [rounded_poly(top, r), rounded_poly(bot, r), capsule(p, q, dw)], W, H

def monogram(gap=True, r=4.0, box=100.0):
    paths, w, h = zmark(H=box*MH/MW, r=r*box/MW, gap=gap)
    return paths

MONO_RATIO = MH/MW   # height / width

# ---------------------------------------------------------------- type
_cache = {}
def load(name, wght=None, wdth=None):
    key = (name, wght, wdth)
    if key in _cache: return _cache[key]
    f = TTFont(os.path.join(FONTS, name))
    axes = {}
    if "fvar" in f:
        names = [a.axisTag for a in f["fvar"].axes]
        if wght and "wght" in names: axes["wght"] = wght
        if wdth and "wdth" in names: axes["wdth"] = wdth
        if axes: f = instancer.instantiateVariableFont(f, axes, updateFontNames=False)
    _cache[key] = f
    return f

def metrics(font):
    upm = font["head"].unitsPerEm
    try: cap = font["OS/2"].sCapHeight or upm*0.7
    except Exception: cap = upm*0.7
    return upm, cap

def text_path(name, text, wght=700, wdth=None, cap_height=100.0,
              tracking=0.0, kern=True, subst=None, fit=None):
    """Outline text; returns (path_d, width, per_glyph[(char,d,x,adv)])."""
    if fit:
        lo, hi = -0.05, 3.0
        for _ in range(44):
            mid = (lo+hi)/2
            if text_path(name, text, wght, wdth, cap_height, mid, kern)[1] < fit:
                lo = mid
            else:
                hi = mid
        tracking = (lo+hi)/2
    font = load(name, wght, wdth)
    upm, cap = metrics(font)
    s = cap_height / cap
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    kt = {}
    if kern and "kern" in font:
        for st in font["kern"].kernTables: kt.update(st.kernTable)
    x = 0.0
    out, ds = [], []
    for i, ch in enumerate(text):
        gname = cmap.get(ord(ch))
        if gname is None: continue
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.3f}")
        tp = TransformPen(pen, Transform(s, 0, 0, -s, x, 0))
        gs[gname].draw(tp)
        d = pen.getCommands()
        adv = hmtx[gname][0]*s
        if i+1 < len(text):
            nx = cmap.get(ord(text[i+1]))
            if nx and (gname, nx) in kt: adv += kt[(gname, nx)]*s
        adv += tracking*cap_height
        out.append((ch, d, x, adv))
        if d: ds.append(d)
        x += adv
    return " ".join(ds), x - tracking*cap_height, out

# ---------------------------------------------------------------- render
def svg(w, h, body, bg=None, vb=None):
    vb = vb or f"0 0 {w} {h}"
    b = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="{vb}" fill="none">{b}{body}</svg>')

def png(svg_path, out, width=None, height=None):
    cmd = ["rsvg-convert", svg_path, "-o", out]
    if width: cmd += ["-w", str(width)]
    if height: cmd += ["-h", str(height)]
    subprocess.run(cmd, check=True)
    return out


def scale_path(*a, **k):
    raise RuntimeError("scale_path rompe los flags de los arcos SVG: "
                       "usa <g transform=\"scale(k)\"> en su lugar.")
