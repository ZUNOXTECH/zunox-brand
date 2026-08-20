"""ZUNOX — decisiones cerradas. Fuente única de verdad del kit."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import zx, word

# ---------------------------------------------------------------- color · C "Verde MyProtein"
C = {
    "deep":    "#002830",   # tinta más oscura / fondos amplios
    "ground":  "#003942",   # AZUL VERDOSO PRINCIPAL (color MyProtein)
    "surface": "#014E59",   # superficies, tarjetas
    "line":    "#0A6A73",   # filetes
    "g700":    "#00704F",   # verde oscuro — texto/enlaces sobre claro (AA sobre #F4F7F7)
    "g500":    "#00C389",   # VERDE DE MARCA
    "g400":    "#5FE3B4",   # hover, destacados sobre oscuro
    "ink":     "#F0F7F4",   # texto sobre oscuro
    "muted":   "#8FB3AF",   # texto secundario
    "paper":   "#F4F7F7",   # fondo claro
}

# ---------------------------------------------------------------- Z (primera letra + isotipo)
ZP = dict(W=94.0, bar=20.5, dw=24.5, gap_h=10.8)
ZR = 3.2

def Zpaths(cap=100.0):
    k = cap/100.0
    return zx.zmark(H=cap, r=ZR*k, **{a: v*k for a, v in ZP.items()})

# ---------------------------------------------------------------- wordmark
TRACK = 13.0
KERN  = {"Z": 4, "U": -1, "N": 2, "O": 2}          # ajuste óptico
TAGFONT, TAGW = "Sora-var.ttf", 400
TAGLINE = "AGENCIA DE IA"

def glyphs(cap=100.0):
    k = cap/100.0
    zp, zw, _ = Zpaths(cap)
    out = [("Z", zp, zw)]
    for ch, (ps, w) in [("U", word.U()), ("N", word.N()),
                        ("O", word.O()), ("X", word.X())]:
        out.append((ch, ps, w*k))
    return out, k

def wordmark(cap=100.0, fill="#FFFFFF", accent=None):
    accent = accent or fill
    gs, k = glyphs(cap)
    parts, x = [], 0.0
    for ch, ps, w in gs:
        col = accent if ch == "X" else fill
        inner = "".join(f'<path d="{d}" fill="{col}"/>' for d in ps)
        sc = "" if ch == "Z" else f' scale({k:.6f})'
        parts.append(f'<g transform="translate({x:.3f},0){sc}">{inner}</g>')
        x += w + (TRACK + KERN.get(ch, 0))*k
    total = x - (TRACK + KERN.get("X", 0))*k
    return "".join(parts), total, cap

def tagline(width, cap, fill):
    d, w, _ = zx.text_path(TAGFONT, TAGLINE, wght=TAGW, cap_height=cap,
                           tracking=0.4, fit=width)
    return f'<path d="{d}" fill="{fill}"/>', w
