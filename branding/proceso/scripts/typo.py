"""Wordmark kit: shape text with HarfBuzz (real kerning), emit glyph outlines as SVG paths (no live text)."""
import io, os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.recordingPen import DecomposingRecordingPen, RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")


def f(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Face:
    def __init__(self, name, axes=None):
        font = TTFont(os.path.join(FONTS, name))
        if axes:
            font = instantiateVariableFont(font, axes)
        buf = io.BytesIO()
        font.save(buf)
        self.font = font
        self.gs = font.getGlyphSet()
        self.order = font.getGlyphOrder()
        self.upm = font["head"].unitsPerEm
        self.xh = font["OS/2"].sxHeight
        self.cap = font["OS/2"].sCapHeight
        self.hbfont = hb.Font(hb.Face(buf.getvalue()))

    def shape(self, text, tracking=0):
        b = hb.Buffer()
        b.add_str(text)
        b.guess_segment_properties()
        hb.shape(self.hbfont, b, {"kern": True, "liga": False})
        x, out = 0, []
        for info, pos in zip(b.glyph_infos, b.glyph_positions):
            out.append((self.order[info.codepoint], x + pos.x_offset))
            x += pos.x_advance + tracking
        return out, x

    def contours(self, gn):
        rec = DecomposingRecordingPen(self.gs)
        self.gs[gn].draw(rec)
        cs, cur = [], []
        for op, args in rec.value:
            if op == "moveTo" and cur:
                cs.append(cur)
                cur = []
            cur.append((op, args))
        if cur:
            cs.append(cur)
        return cs

    @staticmethod
    def cbounds(c):
        r = RecordingPen()
        r.value = c
        bp = BoundsPen(None)
        r.replay(bp)
        return bp.bounds

    def d(self, cs, m):
        pen = SVGPathPen(None, ntos=f)
        tp = TransformPen(pen, m)
        for c in cs:
            r = RecordingPen()
            r.value = c
            r.replay(tp)
        return pen.getCommands()


def lay(face, text, size=160, tracking=0, square_dots=False, dot_colour=None, fg="#e8e4dc",
        letter_colours=None, line=None, special=None, square_period=False, sq_k=1.0, adjust=None):
    """Return (elements_svg, bbox) with baseline at y=0, x from 0. Optional brass ground line / square tittles."""
    s = size / face.upm
    glyphs, adv = face.shape(text, tracking)
    if adjust:
        cum, g2 = 0, []
        for i, (gn, gx) in enumerate(glyphs):
            g2.append((gn, gx + cum))
            cum += adjust.get(i, 0)
        glyphs, adv = g2, adv + cum
    els, xs0, xs1, ys0, ys1 = [], 1e9, -1e9, 1e9, -1e9
    squares = []
    for i, (gn, gx) in enumerate(glyphs):
        cs = face.contours(gn)
        dot = None
        ch = text[i] if i < len(text) else ""
        if square_dots and ch in "ij" and len(cs) > 1:
            dot = max(cs, key=lambda c: face.cbounds(c)[1])
            cs = [c for c in cs if c is not dot]
            db = face.cbounds(dot)
            side = (db[2] - db[0]) * sq_k
            cx, cy = (db[0] + db[2]) / 2, (db[1] + db[3]) / 2
            squares.append(((gx + cx - side / 2) * s, -(cy + side / 2) * s, side * s))
        if square_period and ch == "." and cs:
            db = face.cbounds(cs[0])
            side = (db[2] - db[0]) * sq_k
            cx, cy = (db[0] + db[2]) / 2, (db[1] + db[3]) / 2
            squares.append(((gx + cx - side / 2) * s, -(cy + side / 2) * s, side * s))
            xs1 = max(xs1, (gx + cx + side / 2) * s)
            cs = []
        if not cs:
            continue
        col = (letter_colours or {}).get(i, fg)
        m = (s, 0, 0, -s, gx * s, 0)
        els.append((col, face.d(cs, m)))
        for c in cs:
            b = face.cbounds(c)
            xs0, xs1 = min(xs0, (gx + b[0]) * s), max(xs1, (gx + b[2]) * s)
            ys0, ys1 = min(ys0, -b[3] * s), max(ys1, -b[1] * s)
    for x, y, side in squares:
        ys0 = min(ys0, y)
    return els, squares, (xs0, ys0, xs1, ys1), adv * s


def to_svg(els, squares, bbox, fg, acc, line_t=0.0, pad=0.0, sq_col=None, extra="", bg=None):
    x0, y0, x1, y1 = bbox
    parts = []
    if line_t:
        parts.append(f'<rect fill="{acc}" x="{f(x0)}" y="0" width="{f(x1-x0)}" height="{f(line_t)}"/>')
        y1 = max(y1, line_t)
    for col, d in els:
        parts.append(f'<path fill="{col}" d="{d}"/>')
    for x, y, side in squares:
        parts.append(f'<rect fill="{sq_col or acc}" x="{f(x)}" y="{f(y)}" width="{f(side)}" height="{f(side)}"/>')
    parts.append(extra)
    w, h = (x1 - x0) + 2 * pad, (y1 - y0) + 2 * pad
    bgr = f'<rect x="{f(x0-pad)}" y="{f(y0-pad)}" width="{f(w)}" height="{f(h)}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f(x0-pad)} {f(y0-pad)} {f(w)} {f(h)}">'
            f'{bgr}{"".join(parts)}</svg>'), (x0 - pad, y0 - pad, w, h)
