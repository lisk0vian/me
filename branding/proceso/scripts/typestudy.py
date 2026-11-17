"""Type study: four pairings applied to the real lockup + banner line + handle."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typo import Face, f
from kit import stair, txt, cap_size, xh_size, S, SIDE, PIZARRA, SUPERFICIE, HUESO, NIEBLA, PERVINCA, Face as _F

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "work13")
os.makedirs(OUT, exist_ok=True)
LABEL = Face("geist.ttf", {"wght": 500})

PAIRS = [
    ("A", "Space Grotesk + Space Mono", "Técnica con carácter: nació de una tipografía monoespaciada. Muy usada por devs y estudios de diseño.",
     Face("spacegrotesk.ttf", {"wght": 600}), Face("spacegrotesk.ttf", {"wght": 400}), Face("spacemono-bold.ttf")),
    ("B", "Sora + JetBrains Mono", "Geométrica y amplia: círculos perfectos y terminales rectos, como tu símbolo. JetBrains Mono es la de los IDE.",
     Face("sora.ttf", {"wght": 600}), Face("sora.ttf", {"wght": 400}), Face("jetbrains.ttf", {"wght": 600})),
    ("C", "Manrope + JetBrains Mono", "Moderna y tranquila, algo condensada; se ve precisa y ordenada sin ser fría.",
     Face("manrope.ttf", {"wght": 700}), Face("manrope.ttf", {"wght": 400}), Face("jetbrains.ttf", {"wght": 600})),
    ("D", "Plus Jakarta Sans + IBM Plex Mono", "Elegante y cálida, con más personalidad en las curvas; la más 'marca personal'.",
     Face("jakarta.ttf", {"wght": 700}), Face("jakarta.ttf", {"wght": 400}), Face("plexmono-semibold.ttf")),
]

W, H = 1628, 1180
CW, CH = 764, 520
o = [f'<rect width="{W}" height="{H}" fill="{PIZARRA}"/>']
T = lambda face, s, size, x, y, col=HUESO: o.append(txt(face, s, size, x, y, col)[0])
T(LABEL, "Tipografía — cuatro opciones aplicadas a tu marca", cap_size(LABEL, 22), 40, 66)
T(LABEL, "Todas gratuitas y de código abierto (OFL). Cada opción: títulos + monoespaciada para código y lisk0vian.", cap_size(LABEL, 10.5), 40, 98, NIEBLA)

for i, (k, name, note, head, body, mono) in enumerate(PAIRS):
    x0 = 40 + (i % 2) * (CW + 20)
    y0 = 130 + (i // 2) * (CH + 20)
    o.append(f'<rect x="{x0}" y="{y0}" width="{CW}" height="{CH}" rx="16" fill="#181c22"/>')
    T(LABEL, f"{k} · {name}", cap_size(LABEL, 13), x0 + 30, y0 + 46)
    # lockup
    kk = 0.6
    sym, side = stair(HUESO, PERVINCA, x=x0 + 30, y=y0 + 80, k=kk)
    o.append(sym)
    T(head, "Jeremi A.", cap_size(head, S * 1.1 * kk), x0 + 30 + side + S * 0.9 * kk, y0 + 80 + SIDE * kk)
    # mini banner
    bx, by, bw, bh = x0 + 30, y0 + 240, CW - 60, 150
    o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#12151a" stroke="#262c36"/>')
    T(head, "Full-stack Developer", cap_size(head, 25), bx + 28, by + 58)
    T(body, "TypeScript · JavaScript · Software Architecture", cap_size(body, 11), bx + 28, by + 90, NIEBLA)
    o.append(f'<circle cx="{bx + 33}" cy="{by + 117}" r="5" fill="{PERVINCA}"/>')
    T(mono, "github.com/lisk0vian", xh_size(mono, 8.5), bx + 46, by + 122, PERVINCA)
    o.append(stair(HUESO, PERVINCA, x=bx + bw - 130, y=by + 25, k=0.5)[0])
    # specimen + note
    T(head, "Aa Bb 0123", cap_size(head, 16), x0 + 30, y0 + 432)
    T(mono, "const solid = true;", xh_size(mono, 10), x0 + 300, y0 + 432, "#c9c5bd")
    words, line, lines = note.split(), "", []
    for wd in words:
        if len(line + " " + wd) > 92:
            lines.append(line); line = wd
        else:
            line = (line + " " + wd).strip()
    lines.append(line)
    for j, ln in enumerate(lines):
        T(LABEL, ln, cap_size(LABEL, 9), x0 + 30, y0 + 472 + j * 22, NIEBLA)

open(os.path.join(OUT, "tipografia.svg"), "w", encoding="utf-8").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{"".join(o)}</svg>')
print("ok")
