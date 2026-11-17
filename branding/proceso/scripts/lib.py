"""Tiny geometry kit: shapely shapes -> clean SVG paths (even-odd)."""
from shapely.geometry import Polygon, LineString, box
from shapely.ops import unary_union
from shapely import affinity


def poly(pts):
    return Polygon(pts)


def band(pts, w, cap="flat", join="mitre"):
    cs = {"flat": 2, "round": 1, "square": 3}[cap]
    js = {"mitre": 2, "round": 1, "bevel": 3}[join]
    return LineString(pts).buffer(w / 2, cap_style=cs, join_style=js, mitre_limit=10)


def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def ring_d(coords):
    c = list(coords)[:-1]
    return "M" + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in c) + "Z"


def to_d(g):
    geoms = g.geoms if hasattr(g, "geoms") else [g]
    out = []
    for p in geoms:
        if p.is_empty:
            continue
        out.append(ring_d(p.exterior.coords))
        for i in p.interiors:
            out.append(ring_d(i.coords))
    return "".join(out)


def svg(g, fill="#000", vb="0 0 256 256", extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">'
            f'<path fill="{fill}" fill-rule="evenodd" d="{to_d(g)}"/>{extra}</svg>')


def arc_pts(cx, cy, r, a0, a1, n=48):
    import math
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
