"""Geometry primitives for the brand-identity skill (promoted from the issue-15 prototype).

Every shape is a cubic, winding-normalised ``pathops.Path`` wrapped in a ``Shape``
that carries an id. Every call on a ``Mark`` is appended to ``Mark.log`` with its
parameters, so a rationale can cite the real construction (mark-craft section 2).

Conventions (pick one and keep it):
- SVG user space, y grows DOWN, the mark lives in a ``box`` x ``box`` square (default 100).
- Angles are degrees, 0 = east, positive = counter-clockwise AS SEEN on screen.
"""
import json
import math

import pathops
from fontTools.pens.svgPathPen import SVGPathPen

_OPS = {
    "union": pathops.PathOp.UNION,
    "difference": pathops.PathOp.DIFFERENCE,
    "intersect": pathops.PathOp.INTERSECTION,
    "xor": pathops.PathOp.XOR,
}
_CAPS = {"butt": pathops.LineCap.BUTT_CAP, "round": pathops.LineCap.ROUND_CAP,
         "square": pathops.LineCap.SQUARE_CAP}
_JOINS = {"miter": pathops.LineJoin.MITER_JOIN, "round": pathops.LineJoin.ROUND_JOIN,
          "bevel": pathops.LineJoin.BEVEL_JOIN}


class Shape:
    def __init__(self, path, sid):
        self.path, self.id = path, sid

    @property
    def bounds(self):
        return tuple(round(v, 4) for v in self.path.bounds)

    @property
    def area(self):
        return abs(self.path.area)

    def d(self, ndigits=3):
        pen = SVGPathPen(None, ntos=lambda v: _fmt(v, ndigits))
        self.path.draw(pen)
        return pen.getCommands()


def _fmt(v, ndigits):
    s = f"{round(v, ndigits):.{ndigits}f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _pt(cx, cy, r, a):
    t = math.radians(a)
    return (cx + r * math.cos(t), cy - r * math.sin(t))


def _arc(path, cx, cy, r, a0, a1):
    """Append cubic arc pieces from a0 to a1 (current point must be at a0).

    Splits at every multiple of 90 deg so each horizontal/vertical extremum
    gets an on-curve node (mark-craft rule 7)."""
    step = 1 if a1 > a0 else -1
    cuts = [a0]
    q = math.floor(a0 / 90) * 90 if step > 0 else math.ceil(a0 / 90) * 90
    while True:
        q += 90 * step
        if (q - a1) * step >= 0:
            break
        if (q - a0) * step > 1e-9:
            cuts.append(q)
    cuts.append(a1)
    for s, e in zip(cuts, cuts[1:]):
        th = math.radians(e - s)
        k = 4 / 3 * math.tan(th / 4)
        p0, p3 = _pt(cx, cy, r, s), _pt(cx, cy, r, e)
        # tangent of a CCW-on-screen arc at angle a, in y-down space: (-sin a, -cos a)
        ts, te = math.radians(s), math.radians(e)
        c1 = (p0[0] - k * r * math.sin(ts), p0[1] - k * r * math.cos(ts))
        c2 = (p3[0] + k * r * math.sin(te), p3[1] + k * r * math.cos(te))
        path.cubicTo(*c1, *c2, *p3)  # pathops wants 6 flat floats, not 3 tuples


class Mark:
    """One construction. Primitives return Shapes; the log records every call."""

    def __init__(self, name, box=100.0, note=""):
        self.name, self.box, self.note = name, box, note
        self.log, self._n = [], 0

    # -- bookkeeping -----------------------------------------------------
    def _new(self, op, path, **params):
        self._n += 1
        sid = f"s{self._n}"
        clean = {k: (v.id if isinstance(v, Shape) else
                     [x.id if isinstance(x, Shape) else x for x in v] if isinstance(v, (list, tuple)) else v)
                 for k, v in params.items()}
        self.log.append({"id": sid, "op": op, **clean})
        return Shape(path, sid)

    def note_param(self, name, value, why=""):
        """Record a derived/tuned value (e.g. an optical correction) in the log."""
        self.log.append({"op": "param", "name": name, "value": value, "why": why})
        return value

    # -- basic shapes ----------------------------------------------------
    def circle(self, cx, cy, r):
        p = pathops.Path()
        p.moveTo(*_pt(cx, cy, r, 0))
        _arc(p, cx, cy, r, 0, 360)
        p.close()
        return self._new("circle", p, cx=cx, cy=cy, r=r)

    def rect(self, x, y, w, h):
        p = pathops.Path()
        p.moveTo(x, y); p.lineTo(x + w, y); p.lineTo(x + w, y + h); p.lineTo(x, y + h); p.close()
        return self._new("rect", p, x=x, y=y, w=w, h=h)

    def rounded_rect(self, x, y, w, h, r):
        r = min(r, w / 2, h / 2)
        p = pathops.Path()
        p.moveTo(x + r, y)
        p.lineTo(x + w - r, y); _arc(p, x + w - r, y + r, r, 90, 0)
        p.lineTo(x + w, y + h - r); _arc(p, x + w - r, y + h - r, r, 0, -90)
        p.lineTo(x + r, y + h); _arc(p, x + r, y + h - r, r, -90, -180)
        p.lineTo(x, y + r); _arc(p, x + r, y + r, r, 180, 90)
        p.close()
        p.simplify()
        return self._new("rounded_rect", p, x=x, y=y, w=w, h=h, r=r)

    def polygon(self, points):
        p = pathops.Path()
        p.moveTo(*points[0])
        for q in points[1:]:
            p.lineTo(*q)
        p.close()
        p.simplify()
        return self._new("polygon", p, points=[tuple(round(c, 4) for c in q) for q in points])

    def regular_polygon(self, cx, cy, r, n, rotation=90):
        pts = [_pt(cx, cy, r, rotation + i * 360 / n) for i in range(n)]
        s = self.polygon(pts)
        self.log[-1].update(op="regular_polygon", cx=cx, cy=cy, r=r, n=n, rotation=rotation)
        return s

    def annulus_segment(self, cx, cy, r_in, r_out, a0, a1):
        """Ring sector between radii r_in..r_out, angles a0..a1 (CCW). r_in=0 -> pie wedge."""
        p = pathops.Path()
        if abs(a1 - a0) >= 360:
            outer = self.circle(cx, cy, r_out)
            self.log.pop(); self._n -= 1
            if r_in <= 0:
                return self._new("annulus_segment", outer.path, cx=cx, cy=cy, r_in=r_in, r_out=r_out, a0=a0, a1=a1)
            inner = pathops.Path(); inner.moveTo(*_pt(cx, cy, r_in, 0)); _arc(inner, cx, cy, r_in, 0, 360); inner.close()
            path = pathops.op(outer.path, inner, pathops.PathOp.DIFFERENCE)
            return self._new("annulus_segment", path, cx=cx, cy=cy, r_in=r_in, r_out=r_out, a0=a0, a1=a1)
        p.moveTo(*_pt(cx, cy, r_out, a0))
        _arc(p, cx, cy, r_out, a0, a1)
        if r_in > 0:
            p.lineTo(*_pt(cx, cy, r_in, a1))
            _arc(p, cx, cy, r_in, a1, a0)
        else:
            p.lineTo(cx, cy)
        p.close()
        p.simplify()
        return self._new("annulus_segment", p, cx=cx, cy=cy, r_in=r_in, r_out=r_out, a0=a0, a1=a1)

    def stroke(self, points, width, cap="round", join="miter", miter_limit=4.0, closed=False):
        """Expand a polyline centreline into a filled outline.

        Observed: skia's stroker emits CONIC verbs for round caps/joins, which
        SVGPathPen cannot draw, so they are converted to quadratics here. The
        result therefore mixes quads into an otherwise cubic library."""
        p = pathops.Path()
        p.moveTo(*points[0])
        for q in points[1:]:
            p.lineTo(*q)
        if closed:
            p.close()
        p.stroke(width, _CAPS[cap], _JOINS[join], miter_limit)   # mutates in place, returns None
        p.convertConicsToQuads()
        p.simplify()
        return self._new("stroke", p, points=[tuple(q) for q in points], width=width, cap=cap,
                         join=join, miter_limit=miter_limit, closed=closed)

    # -- booleans --------------------------------------------------------
    def _boolean(self, kind, shapes):
        acc = shapes[0].path
        for s in shapes[1:]:
            acc = pathops.op(acc, s.path, _OPS[kind])
        return self._new(kind, acc, inputs=list(shapes))

    def union(self, *shapes):
        return self._boolean("union", shapes)

    def difference(self, a, *cutters):
        return self._boolean("difference", (a,) + cutters)

    def intersect(self, a, b):
        return self._boolean("intersect", (a, b))

    def xor(self, a, b):
        return self._boolean("xor", (a, b))

    # -- transforms ------------------------------------------------------
    def _affine(self, op, s, m, **params):
        p = s.path.transform(*m)
        p.simplify()
        return self._new(op, p, input=s, **params)

    def translate(self, s, dx, dy):
        return self._affine("translate", s, (1, 0, 0, 1, dx, dy), dx=dx, dy=dy)

    def rotate(self, s, deg, about=None):
        cx, cy = about or _centre(s)
        c, sn = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        # CCW on screen in y-down space: x' = c x + s y ; y' = -s x + c y   (about cx,cy)
        m = (c, -sn, sn, c, cx - c * cx - sn * cy, cy + sn * cx - c * cy)
        return self._affine("rotate", s, m, deg=deg, about=(cx, cy))

    def scale(self, s, sx, sy=None, about=None):
        sy = sx if sy is None else sy
        cx, cy = about or _centre(s)
        return self._affine("scale", s, (sx, 0, 0, sy, cx - sx * cx, cy - sy * cy), sx=sx, sy=sy, about=(cx, cy))

    def mirror(self, s, axis="x", about=None):
        """axis='x' flips left-right about the vertical line x=about (default: box centre)."""
        c = self.box / 2 if about is None else about
        m = (-1, 0, 0, 1, 2 * c, 0) if axis == "x" else (1, 0, 0, -1, 0, 2 * c)
        return self._affine("mirror", s, m, axis=axis, about=c)

    # -- optical helpers -------------------------------------------------
    def overshoot(self, ref_height, pct):
        """Overshoot distance for a round form against flat lines `ref_height` apart.
        mark-craft rule 1: 1-3 % per side (unverified source); flag <0.5 % or >4 %."""
        v = ref_height * pct
        self.log.append({"op": "overshoot", "ref_height": ref_height, "pct": pct, "value": round(v, 4)})
        return v

    def fit_overshoot(self, s, top, bottom, pct):
        """Uniformly scale a round shape about its centre so it overshoots the
        flat lines y=top and y=bottom by pct * (bottom-top) on each side."""
        x0, y0, x1, y1 = s.path.bounds
        target = (bottom - top) * (1 + 2 * pct)
        k = target / (y1 - y0)
        cx, cy = (x0 + x1) / 2, (top + bottom) / 2
        p = s.path.transform(k, 0, 0, k, cx - k * cx, cy - k * (y0 + y1) / 2)
        return self._new("fit_overshoot", p, input=s, top=top, bottom=bottom, pct=pct, factor=round(k, 5))


    # -- added for the skill (issue 15, decision 8) ------------------------
    def offset(self, s, d, join="round"):
        """Grow (d > 0) or shrink (d < 0) a shape by distance d."""
        p = s.path.transform(1, 0, 0, 1, 0, 0)
        p.stroke(2 * abs(d), _CAPS["round"], _JOINS[join], 4.0)
        p.convertConicsToQuads()
        kind = pathops.PathOp.UNION if d > 0 else pathops.PathOp.DIFFERENCE
        out = pathops.op(s.path, p, kind)
        return self._new("offset", out, input=s, d=d, join=join)

    def cut_at_line(self, s, p0, p1, keep="left"):
        """Keep the part of s on one side of the infinite line p0->p1 ('left' as seen on screen)."""
        (x0, y0), (x1, y1) = p0, p1
        dx, dy = x1 - x0, y1 - y0
        n = math.hypot(dx, dy)
        ux, uy = dx / n, dy / n
        big = self.box * 100
        # screen-left of the direction in y-down space is (uy, -ux)
        nx, ny = (uy, -ux) if keep == "left" else (-uy, ux)
        a = (x0 - ux * big, y0 - uy * big)
        b = (x0 + ux * big, y0 + uy * big)
        hp = pathops.Path()
        hp.moveTo(*a); hp.lineTo(*b)
        hp.lineTo(b[0] + nx * big, b[1] + ny * big); hp.lineTo(a[0] + nx * big, a[1] + ny * big); hp.close()
        out = pathops.op(s.path, hp, pathops.PathOp.INTERSECTION)
        return self._new("cut_at_line", out, input=s, p0=tuple(p0), p1=tuple(p1), keep=keep)

    def extend(self, points, by):
        """Return the polyline with both end segments extended by `by` (use before stroke/cut)."""
        pts = [tuple(q) for q in points]
        def ext(a, b):
            dx, dy = b[0] - a[0], b[1] - a[1]
            n = math.hypot(dx, dy) or 1.0
            return (b[0] + dx / n * by, b[1] + dy / n * by)
        pts[0], pts[-1] = ext(pts[1], pts[0]), ext(pts[-2], pts[-1])
        self.log.append({"op": "extend", "by": by})
        return pts

    def prune(self, s, min_area=None):
        """Drop contours smaller than min_area (default: (box/16)^2, one 16 px pixel)."""
        from fontTools.pens.recordingPen import RecordingPen
        min_area = (self.box / 16) ** 2 if min_area is None else min_area
        rec = RecordingPen(); s.path.draw(rec)
        contours, cur = [], []
        for op, args in rec.value:
            cur.append((op, args))
            if op in ("closePath", "endPath"):
                contours.append(cur); cur = []
        kept, dropped = pathops.Path(), 0
        for c in contours:
            cp = pathops.Path(); pen = cp.getPen()
            for op, args in c:
                getattr(pen, op)(*args)
            if abs(cp.area) >= min_area:
                pen2 = kept.getPen()
                for op, args in c:
                    getattr(pen2, op)(*args)
            else:
                dropped += 1
        kept.simplify()
        return self._new("prune", kept, input=s, min_area=round(min_area, 3), dropped=dropped)

    # -- export ----------------------------------------------------------
    def svg(self, layers, pad=0.0, size=None):
        """layers: list of (Shape, fill). Returns an SVG string with one <path> per layer."""
        b = self.box
        vb = f"{-pad:g} {-pad:g} {b + 2 * pad:g} {b + 2 * pad:g}"
        sz = f' width="{size}" height="{size}"' if size else ""
        body = "\n".join(f'  <path id="{s.id}" fill="{fill}" d="{s.d()}"/>' for s, fill in layers)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{sz}>\n'
                f'  <!-- {self.name}: generated by recipe; construction log alongside -->\n{body}\n</svg>\n')

    def write(self, out_stem, layers, pad=0.0):
        with open(out_stem + ".svg", "w", encoding="utf-8") as f:
            f.write(self.svg(layers, pad))
        with open(out_stem + ".construction.json", "w", encoding="utf-8") as f:
            json.dump({"mark": self.name, "box": self.box, "note": self.note, "log": self.log}, f, indent=1)
        return out_stem + ".svg"


def _centre(s):
    x0, y0, x1, y1 = s.path.bounds
    return ((x0 + x1) / 2, (y0 + y1) / 2)
