"""ZUNOX custom wordmark letterforms. Cap height = 100, y down, origin top-left."""
import math
from zx import rounded_poly, capsule

CAP = 100.0

def _p(pts, r=0):
    return rounded_poly(pts, r) if r else _poly(pts)

def _poly(pts):
    return "M" + "L".join(f"{x:.3f},{y:.3f}" for x, y in pts) + "Z"

def ring_slots(cx, cy, ro, ri, angles, sw):
    """Annulus split by constant-width radial slots at the given angles (deg)."""
    def edge(a, sign, R):
        t = math.radians(a)
        u = (math.cos(t), -math.sin(t))
        n = (-u[1], u[0])
        h = sw/2.0
        L = math.sqrt(max(R*R - h*h, 0.0))
        return (cx + sign*h*n[0] + L*u[0], cy + sign*h*n[1] + L*u[1])
    angs = sorted(a % 360 for a in angles)
    out = []
    for i, a in enumerate(angs):
        b = angs[(i+1) % len(angs)]
        span = (b - a) % 360
        large = 1 if span > 180 else 0
        p1, p2 = edge(a, -1, ro), edge(b, +1, ro)
        p3, p4 = edge(b, +1, ri), edge(a, -1, ri)
        out.append(f"M{p1[0]:.3f},{p1[1]:.3f}"
                   f"A{ro:.3f},{ro:.3f} 0 {large} 0 {p2[0]:.3f},{p2[1]:.3f}"
                   f"L{p3[0]:.3f},{p3[1]:.3f}"
                   f"A{ri:.3f},{ri:.3f} 0 {large} 1 {p4[0]:.3f},{p4[1]:.3f}Z")
    return out

# ------------------------------------------------------------------ glyphs
def Z(W=88, bar=22, dw=27, s=0.0, r=2.0, H=CAP):
    m = -(W - dw)/H
    p3 = W + m*(H - bar)
    p7 = (W - dw) + m*bar
    pts = [(0,0), (W,0), (p3, H-bar), (W - s*bar, H-bar),
           (W,H), (0,H), (p7, bar), (s*bar, bar)]
    return [rounded_poly(pts, r)], W

def U(W=88, stem=22, ro=None, ri=None, H=CAP):
    """Geometric U with a fully rounded (semicircular) bowl, as the reference."""
    ro = W/2.0 if ro is None else ro
    ri = max(ro - stem, 2.0) if ri is None else ri
    return [f"M0,0L0,{H-ro:.3f}"
            f"A{ro:.3f},{ro:.3f} 0 0 0 {ro:.3f},{H:.3f}"
            f"L{W-ro:.3f},{H:.3f}"
            f"A{ro:.3f},{ro:.3f} 0 0 0 {W:.3f},{H-ro:.3f}"
            f"L{W:.3f},0L{W-stem:.3f},0"
            f"L{W-stem:.3f},{H-ro:.3f}"
            f"A{ri:.3f},{ri:.3f} 0 0 1 {W-stem-ri:.3f},{H-stem:.3f}"
            f"L{stem+ri:.3f},{H-stem:.3f}"
            f"A{ri:.3f},{ri:.3f} 0 0 1 {stem:.3f},{H-ro:.3f}"
            f"L{stem:.3f},0Z"], W

def N(W=90, stem=22, dw=29, H=CAP):
    return [_poly([(0,0),(stem,0),(stem,H),(0,H)]),
            _poly([(W-stem,0),(W,0),(W,H),(W-stem,H)]),
            _poly([(0,0),(dw,0),(W,H),(W-dw,H)])], W

def O(W=104, stem=23, slots=(180.0, -22.0), sw=5.5, H=CAP):
    ro = W/2; ri = ro - stem; cx = ro; cy = H/2
    if not slots:
        return [f"M{cx-ro},{cy}A{ro},{ro} 0 1 0 {cx+ro},{cy}A{ro},{ro} 0 1 0 {cx-ro},{cy}Z"
                f"M{cx-ri},{cy}A{ri},{ri} 0 1 1 {cx+ri},{cy}A{ri},{ri} 0 1 1 {cx-ri},{cy}Z"], W
    return ring_slots(cx, cy, ro, ri, slots, sw), W

def _clip(poly, a, b, c):
    """Sutherland-Hodgman: keep the side where a*x + b*y + c >= 0."""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i+1) % n]
        fp = a*p[0] + b*p[1] + c
        fq = a*q[0] + b*q[1] + c
        if fp >= 0: out.append(p)
        if (fp >= 0) != (fq >= 0):
            t = fp/(fp - fq)
            out.append((p[0] + t*(q[0]-p[0]), p[1] + t*(q[1]-p[1])))
    return out

def X(W=98, dw=29, gap=5.0, H=CAP):
    """Descending stroke continuous; ascending stroke sliced by it (reference)."""
    desc = [(0,0), (dw,0), (W,H), (W-dw,H)]
    asc  = [(W-dw,0), (W,0), (dw,H), (0,H)]
    out = [_poly(desc)]
    if gap:
        k = (W - dw)/H
        upper = _clip(asc,  1.0, -k, -(dw + gap))   # right of the descending stroke
        lower = _clip(asc, -1.0,  k, -gap)          # left of it
        out += [_poly(pp) for pp in (upper, lower) if len(pp) >= 3]
    else:
        out.append(_poly(asc))
    return out, W

# ------------------------------------------------------------------ lockup
def zunox(track=14.0, widths=None):
    """Returns (groups, total_width). groups = [(char, [paths], x, w)]"""
    w = widths or {}
    specs = [("Z", Z(**w.get("Z", {}))), ("U", U(**w.get("U", {}))),
             ("N", N(**w.get("N", {}))), ("O", O(**w.get("O", {}))),
             ("X", X(**w.get("X", {})))]
    out = []; x = 0.0
    for ch, (paths, ww) in specs:
        out.append((ch, paths, x, ww))
        x += ww + track
    return out, x - track

def render(groups, fills):
    g = []
    for ch, paths, x, w in groups:
        f = fills.get(ch, fills.get("*", "#fff"))
        inner = "".join(f'<path d="{d}" fill="{f}" fill-rule="evenodd"/>' for d in paths)
        g.append(f'<g transform="translate({x:.3f},0)">{inner}</g>')
    return "".join(g)
