"""Kit for 'Escalera SOLID': symbol versions, lockups, LinkedIn banner, guide. All text outlined (Geist + IBM Plex Mono)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typo import Face, lay, f

OUT = r"D:\projects\me\branding\logo"
os.makedirs(OUT, exist_ok=True)

# palette
PIZARRA, SUPERFICIE, HUESO, NIEBLA = "#12151a", "#1d222a", "#e8e4dc", "#9aa0a8"
PERVINCA, PERVINCA_OSC = "#949fd8", "#55609c"

G600 = Face("sora.ttf", {"wght": 600})
G400 = Face("sora.ttf", {"wght": 400})
MONO = Face("jetbrains.ttf", {"wght": 600})


# ------------------------------------------------------------------ symbol geometry (unit grid)
CELLS = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)]      # (col, level) S O L I D ; index 2 = L
S, GAP = 60.0, 12.0                                    # block and joint (gap = block / 5)
SIDE = 3 * S + 2 * GAP                                 # 204: square footprint


def stair(fg, acc, s=S, g=GAP, x=0.0, y=0.0, k=1.0, circle_k=1.04, animate=False):
    """Symbol at (x, y) top-left, scale k. Returns svg elements."""
    side = 3 * s + 2 * g
    els, sq = [], []
    for i, (c, lv) in enumerate(CELLS):
        cx, cy = x + c * (s + g) * k, y + (2 - lv) * (s + g) * k
        if i == 2:
            d = s * circle_k * k
            ox, oy = cx + (s * k - d) / 2, cy + (s * k - d) / 2
            if animate:  # the L block is a square that becomes a circle: Liskov substitution
                els.append(
                    f'<rect x="{f(ox)}" y="{f(oy)}" width="{f(d)}" height="{f(d)}" rx="0" fill="{fg}">'
                    f'<animate attributeName="rx" values="0;0;{f(d/2)};{f(d/2)}" keyTimes="0;0.35;0.6;1" dur="4s" repeatCount="indefinite"/>'
                    f'<animate attributeName="fill" values="{fg};{fg};{acc};{acc}" keyTimes="0;0.35;0.6;1" dur="4s" repeatCount="indefinite"/></rect>')
            else:
                els.append(f'<circle cx="{f(ox + d/2)}" cy="{f(oy + d/2)}" r="{f(d/2)}" fill="{acc}"/>')
        else:
            sq.append(f"M{f(cx)} {f(cy)}h{f(s*k)}v{f(s*k)}h{f(-s*k)}Z")
    return f'<path fill="{fg}" d="{"".join(sq)}"/>' + "".join(els), side * k


def doc(body, w, h, title, bg=None):
    b = f'<rect width="{f(w)}" height="{f(h)}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(w)} {f(h)}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{b}{body}</svg>\n')


def save(name, s):
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(s)


# ------------------------------------------------------------------ text helper (outlined)
def txt(face, text, size, x, base, fill, tracking=0, anchor="start"):
    els, _, (x0, y0, x1, y1), adv = lay(face, text, size=size, tracking=tracking, fg=fill)
    if anchor == "middle":
        x -= adv / 2
    elif anchor == "end":
        x -= adv
    g = f'<g transform="translate({f(x)} {f(base)})">' + "".join(f'<path fill="{c}" d="{d}"/>' for c, d in els) + "</g>"
    return g, adv


def cap_size(face, cap):
    return cap * face.upm / face.cap


def xh_size(face, xh):
    return xh * face.upm / face.xh


# ------------------------------------------------------------------ 1. symbol files
def symbols():
    pad = (256 - SIDE) / 2
    save("symbol.svg", doc(stair(HUESO, PERVINCA, x=pad, y=pad)[0], 256, 256, "Jeremi A. — símbolo (fondo oscuro)"))
    save("symbol-light.svg", doc(stair(PIZARRA, PERVINCA_OSC, x=pad, y=pad)[0], 256, 256, "Jeremi A. — símbolo (fondo claro)"))
    # small-size cut: wider joints so the 5 pieces stay apart at 16-24 px
    s2, g2 = 56.0, 22.0
    side2 = 3 * s2 + 2 * g2
    p2 = (256 - side2) / 2
    save("symbol-small.svg", doc(stair(HUESO, PERVINCA, s=s2, g=g2, x=p2, y=p2, circle_k=1.0)[0], 256, 256, "Jeremi A. — símbolo para tamaños pequeños"))
    save("symbol-animated.svg", doc(stair(HUESO, PERVINCA, x=pad, y=pad, animate=True)[0], 256, 256, "Jeremi A. — símbolo animado"))
    # avatar master (on its own tile, dark)
    save("avatar.svg", doc(f'<rect width="256" height="256" fill="{PIZARRA}"/>' + stair(HUESO, PERVINCA, x=128 - SIDE * 0.62 / 2, y=128 - SIDE * 0.62 / 2, k=0.62)[0],
                                  256, 256, "Jeremi A. — avatar"))


# ------------------------------------------------------------------ 2. lockups: the name stands on the first step
def lockup(text, face, fg, acc, title, file, mono=False):
    sym, side = stair(fg, acc)
    gap = S * 0.9
    if mono:
        size = xh_size(face, S * 0.92)
    else:
        size = cap_size(face, S * 1.1)
    g, adv = txt(face, text, size, side + gap, SIDE, fg)
    els, _, (x0, y0, x1, y1), _ = lay(face, text, size=size)
    w = side + gap + x1
    save(file, doc(sym + g, w, SIDE + max(0, y1), title))


def lockups():
    lockup("Jeremi A.", G600, HUESO, PERVINCA, "Jeremi A. — logo con nombre (fondo oscuro)", "lockup.svg")
    lockup("Jeremi A.", G600, PIZARRA, PERVINCA_OSC, "Jeremi A. — logo con nombre (fondo claro)", "lockup-light.svg")
    lockup("lisk0vian", MONO, HUESO, PERVINCA, "lisk0vian — logo con alias (fondo oscuro)", "lockup-lisk0vian.svg", mono=True)
    lockup("lisk0vian", MONO, PIZARRA, PERVINCA_OSC, "lisk0vian — logo con alias (fondo claro)", "lockup-lisk0vian-light.svg", mono=True)


# ------------------------------------------------------------------ 3. LinkedIn banner 1584 x 396
def banner():
    W, H = 1584, 396
    out = [f'<rect width="{W}" height="{H}" fill="{PIZARRA}"/>']
    # blueprint joints: a faint grid built from the symbol's own module (block 60 + joint 12 -> pitch 72 at k=0.5)
    pitch = 36
    dots = "".join(f"M{x} {y}h3v3h-3Z" for x in range(1080, W, pitch) for y in range(18, H, pitch))
    out.append(f'<path fill="{SUPERFICIE}" d="{dots}"/>')
    # the symbol, large, on the right; its circle is the only colour on the banner
    k = 280 / SIDE
    sym, side = stair(HUESO, PERVINCA, x=W - 120 - SIDE * k, y=(H - SIDE * k) / 2, k=k)
    out.append(sym)
    # text block, clear of the profile photo (bottom-left on desktop and mobile)
    x = 470
    g, _ = txt(G600, "Full-stack Developer", cap_size(G600, 46), x, 168, HUESO)
    out.append(g)
    g, _ = txt(G400, "TypeScript · JavaScript · Software Architecture", cap_size(G400, 19), x, 214, NIEBLA)
    out.append(g)
    out.append(f'<circle cx="{x + 7}" cy="{262 - 7}" r="7" fill="{PERVINCA}"/>')
    g, _ = txt(MONO, "github.com/lisk0vian", xh_size(MONO, 13), x + 26, 262, PERVINCA)
    out.append(g)
    svg = doc("".join(out), W, H, "Jeremi A. — banner de LinkedIn")
    save("linkedin-banner.svg", svg)


# ------------------------------------------------------------------ 4. one-page guide
def guide():
    W, H = 1600, 1500
    o = [f'<rect width="{W}" height="{H}" fill="{PIZARRA}"/>']
    T = lambda face, s, size, x, y, col=HUESO, **kw: o.append(txt(face, s, size, x, y, col, **kw)[0])
    card = lambda x, y, w, h: o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#181c22"/>')
    H1, BODY, SMALL = 15.5, 10.5, 9.0     # cap heights

    o.append(stair(HUESO, PERVINCA, x=60, y=50, k=0.36)[0])
    T(G600, "Jeremi A. — guía de marca", cap_size(G600, 26), 150, 92)
    T(G400, "Símbolo Escalera SOLID · Sora + JetBrains Mono · modo oscuro primero", cap_size(G400, 11), 150, 122, NIEBLA)

    # --- historia
    card(40, 160, 740, 300)
    T(G600, "La historia", cap_size(G600, H1), 70, 205)
    lines = ["Cinco bloques, uno por principio de SOLID, puestos en escalera:",
             "aprender paso a paso. El tercero es la L de Liskov — de ahí viene",
             "lisk0vian — y fue sustituido por un círculo. Es otra forma que",
             "cumple el mismo contrato, y la escalera sigue en pie."]
    for i, l in enumerate(lines):
        T(G400, l, cap_size(G400, BODY), 70, 248 + i * 26, "#c9c5bd")
    for i, lbl in enumerate("SOLID"):
        x = 70 + i * 44
        o.append(f'<rect x="{x}" y="372" width="32" height="32" fill="{PERVINCA if i == 2 else HUESO}" rx="{16 if i == 2 else 0}"/>')
        T(MONO, lbl, xh_size(MONO, 8), x + 16, 430, NIEBLA, anchor="middle")

    # --- construcción
    card(800, 160, 760, 300)
    T(G600, "Construcción", cap_size(G600, H1), 830, 205)
    k = 0.9
    sx, sy = 860, 230
    o.append(stair(HUESO, PERVINCA, x=sx, y=sy, k=k)[0])
    gl = "".join(f'<line x1="{f(sx + v*k)}" y1="{sy-8}" x2="{f(sx + v*k)}" y2="{f(sy + SIDE*k + 8)}"/>' for v in (0, 60, 72, 132, 144, 204))
    o.append(f'<g stroke="{PERVINCA}" stroke-opacity="0.35" stroke-width="1">{gl}</g>')
    notes = ["Retícula 3 × 3: bloque = s", "Junta = s / 5", "Círculo = s (+4 % de corrección óptica)",
             "Huella cuadrada: 3s + 2 juntas", "Un solo color de acento: el círculo"]
    for i, n in enumerate(notes):
        o.append(f'<circle cx="1110" cy="{252 + i*40 - 5}" r="4" fill="{PERVINCA}"/>')
        T(G400, n, cap_size(G400, BODY), 1124, 252 + i * 40, "#c9c5bd")

    # --- colores
    card(40, 480, 740, 300)
    T(G600, "Colores", cap_size(G600, H1), 70, 525)
    sw = [(PIZARRA, "Pizarra", "fondo principal"), (SUPERFICIE, "Superficie", "tarjetas, fichas"),
          (HUESO, "Hueso", "texto y bloques"), (PERVINCA, "Pervinca", "el círculo, acento"),
          (PERVINCA_OSC, "Pervinca oscuro", "acento sobre claro")]
    for i, (c, n, u) in enumerate(sw):
        x = 70 + i * 138
        o.append(f'<rect x="{x}" y="550" width="120" height="120" rx="12" fill="{c}" stroke="#2a303a"/>')
        T(G600, n, cap_size(G600, 9), x, 696)
        T(MONO, c.upper(), xh_size(MONO, 7), x, 718, NIEBLA)
        T(G400, u, cap_size(G400, 7.5), x, 740, NIEBLA)

    # --- tipografía
    card(800, 480, 760, 300)
    T(G600, "Tipografía", cap_size(G600, H1), 830, 525)
    T(G600, "Aa", cap_size(G600, 54), 830, 620)
    T(G600, "Sora", cap_size(G600, 13), 960, 572)
    T(G400, "Nombre, títulos y textos. 600 títulos · 400 texto.", cap_size(G400, 9), 960, 600, NIEBLA)
    T(G600, "Jeremi A. — Full-stack Developer", cap_size(G600, 12), 960, 636)
    T(MONO, "Aa", xh_size(MONO, 36), 830, 740, PERVINCA)
    T(MONO, "JetBrains Mono", xh_size(MONO, 10), 960, 690)
    T(G400, "Alias, código, etiquetas y datos técnicos.", cap_size(G400, 9), 960, 718, NIEBLA)
    T(MONO, "lisk0vian · const solid = true;", xh_size(MONO, 9.5), 960, 752, "#c9c5bd")

    # --- versiones
    card(40, 800, 1520, 300)
    T(G600, "Versiones", cap_size(G600, H1), 70, 845)
    kv, top = 0.42, 892
    def ver(x, fg, acc, face, text, mono=False):
        sym_v, side_v = stair(fg, acc, x=x, y=top, k=kv)
        o.append(sym_v)
        size = xh_size(face, S * 0.92 * kv) if mono else cap_size(face, S * 1.1 * kv)
        T(face, text, size, x + side_v + S * 0.9 * kv, top + SIDE * kv, fg)
    ver(70, HUESO, PERVINCA, G600, "Jeremi A.")
    o.append(f'<rect x="440" y="868" width="400" height="134" rx="12" fill="{HUESO}"/>')
    ver(470, PIZARRA, PERVINCA_OSC, G600, "Jeremi A.")
    ver(880, HUESO, PERVINCA, MONO, "lisk0vian", mono=True)
    o.append(f'<rect x="1300" y="868" width="110" height="110" rx="24" fill="{SUPERFICIE}"/>')
    o.append(stair(HUESO, PERVINCA, x=1355 - SIDE * 0.33 / 2, y=923 - SIDE * 0.33 / 2, k=0.33)[0])
    o.append(f'<rect x="1430" y="868" width="110" height="110" rx="24" fill="{SUPERFICIE}"/>')
    o.append(stair(HUESO, HUESO, x=1485 - SIDE * 0.33 / 2, y=923 - SIDE * 0.33 / 2, k=0.33)[0])
    T(G400, "Nombre · oscuro", cap_size(G400, 8), 70, 1060, NIEBLA)
    T(G400, "Nombre · claro", cap_size(G400, 8), 440, 1060, NIEBLA)
    T(G400, "Alias · GitHub", cap_size(G400, 8), 880, 1060, NIEBLA)
    T(G400, "Avatar · un color", cap_size(G400, 8), 1300, 1060, NIEBLA)

    # --- uso
    card(40, 1120, 740, 340)
    T(G600, "Espacio y tamaños", cap_size(G600, H1), 70, 1165)
    k = 0.6
    bx, by = 130, 1225
    o.append(f'<rect x="{f(bx - S*k)}" y="{f(by - S*k)}" width="{f(SIDE*k + 2*S*k)}" height="{f(SIDE*k + 2*S*k)}" fill="none" stroke="{PERVINCA}" stroke-dasharray="5 4" stroke-opacity="0.6"/>')
    o.append(stair(HUESO, PERVINCA, x=bx, y=by, k=k)[0])
    for i, l in enumerate(["Espacio libre alrededor: un bloque (s).",
                           "Tamaño mínimo: 24 px de alto.",
                           "Debajo de 24 px: usa la versión 'small'",
                           "(juntas más anchas), hasta 16 px.",
                           "El círculo siempre es el único acento."]):
        T(G400, l, cap_size(G400, BODY), 390, 1215 + i * 32, "#c9c5bd")

    card(800, 1120, 760, 340)
    T(G600, "No hacer", cap_size(G600, H1), 830, 1165)
    k = 0.42
    ex = [("rotar", f'<g transform="rotate(20 {f(870 + SIDE*k/2)} {f(1200 + SIDE*k/2)})">{stair(HUESO, PERVINCA, x=870, y=1200, k=k)[0]}</g>'),
          ("mover el círculo", None), ("otro color", stair(HUESO, "#e07a5f", x=1230, y=1200, k=k)[0]),
          ("deformar", f'<g transform="translate(1410 1200) scale(1.45 0.75)">{stair(HUESO, PERVINCA, k=k)[0]}</g>')]
    # moved circle: put the accent on the top block instead of the L
    cells_bad = []
    for i, (c, lv) in enumerate(CELLS):
        cx, cy = 1050 + c * (S + GAP) * k, 1200 + (2 - lv) * (S + GAP) * k
        if i == 4:
            cells_bad.append(f'<circle cx="{f(cx + S*k/2)}" cy="{f(cy + S*k/2)}" r="{f(S*k/2)}" fill="{PERVINCA}"/>')
        else:
            cells_bad.append(f'<rect x="{f(cx)}" y="{f(cy)}" width="{f(S*k)}" height="{f(S*k)}" fill="{HUESO}"/>')
    ex[1] = ("mover el círculo", "".join(cells_bad))
    for i, (lbl, body) in enumerate(ex):
        x = 870 + i * 180
        o.append(body)
        o.append(f'<path d="M{x-6} {1325}l{SIDE*k+12} -{SIDE*k*0+0}" stroke="none"/>')
        o.append(f'<line x1="{x - 4}" y1="1196" x2="{f(x + SIDE*k + 4)}" y2="{f(1204 + SIDE*k)}" stroke="#e07a5f" stroke-width="3"/>')
        T(G400, lbl, cap_size(G400, 8.5), x, 1330, NIEBLA)
    o.append(f'<circle cx="836" cy="1375" r="6" fill="{PERVINCA}"/>')
    T(G400, "El círculo pervinca también firma por sí solo: viñetas, el punto", cap_size(G400, 9), 852, 1380, "#c9c5bd")
    T(G400, "final de un título, el indicador de 'disponible'.", cap_size(G400, 9), 852, 1406, "#c9c5bd")

    save("guia.svg", doc("".join(o), W, H, "Jeremi A. — guía de marca"))


if __name__ == "__main__":
    symbols()
    lockups()
    banner()
    guide()
    print("kit ok")
