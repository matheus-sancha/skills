"""Flatten a hand-written SVG to one filled path per colour, so it can be gated (issue 15, decision 6).

Handles <path>, <rect>, <circle>, <ellipse>, <polygon>, <polyline>, <line>, fills and strokes, and a
simple transform="translate|scale|matrix" on the element. <mask>, <clipPath>, <use>, gradients and
nested transforms are refused: rebuild those parts with the primitives instead.

Usage: python -B -m brandkit.flatten IN.svg OUT.svg
"""
import math
import re
import sys
import xml.etree.ElementTree as ET

import pathops
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.svgLib.path import parse_path

NS = "{http://www.w3.org/2000/svg}"
REFUSE = ("mask", "clipPath", "use", "linearGradient", "radialGradient", "pattern", "text")


def _num(v, d=0.0):
    return float(re.sub(r"[a-z%]+$", "", v)) if v else d


def _matrix(t):
    if not t:
        return (1, 0, 0, 1, 0, 0)
    m = re.match(r"\s*(\w+)\(([^)]*)\)\s*$", t)
    if not m:
        raise SystemExit(f"unsupported transform: {t}")
    k, args = m.group(1), [float(x) for x in re.split(r"[\s,]+", m.group(2).strip())]
    if k == "translate":
        return (1, 0, 0, 1, args[0], args[1] if len(args) > 1 else 0)
    if k == "scale":
        return (args[0], 0, 0, args[1] if len(args) > 1 else args[0], 0, 0)
    if k == "matrix":
        return tuple(args)
    if k == "rotate":
        a = math.radians(args[0]); c, s = math.cos(a), math.sin(a)
        cx, cy = (args[1], args[2]) if len(args) == 3 else (0, 0)
        return (c, s, -s, c, cx - c * cx + s * cy, cy - s * cx - c * cy)
    raise SystemExit(f"unsupported transform: {t}")


def _shape_d(el, tag):
    g = el.get
    if tag == "path":
        return g("d")
    if tag == "rect":
        x, y, w, h = _num(g("x")), _num(g("y")), _num(g("width")), _num(g("height"))
        rx = _num(g("rx"), _num(g("ry")))
        if rx:
            r = min(rx, w / 2, h / 2)
            return (f"M{x + r},{y}H{x + w - r}A{r},{r} 0 0 1 {x + w},{y + r}V{y + h - r}A{r},{r} 0 0 1 {x + w - r},{y + h}"
                    f"H{x + r}A{r},{r} 0 0 1 {x},{y + h - r}V{y + r}A{r},{r} 0 0 1 {x + r},{y}Z")
        return f"M{x},{y}H{x + w}V{y + h}H{x}Z"
    if tag in ("circle", "ellipse"):
        cx, cy = _num(g("cx")), _num(g("cy"))
        rx = _num(g("r")) if tag == "circle" else _num(g("rx"))
        ry = _num(g("r")) if tag == "circle" else _num(g("ry"))
        return f"M{cx - rx},{cy}A{rx},{ry} 0 1 0 {cx + rx},{cy}A{rx},{ry} 0 1 0 {cx - rx},{cy}Z"
    if tag in ("polygon", "polyline"):
        pts = re.split(r"[\s,]+", g("points").strip())
        pairs = [f"{pts[i]},{pts[i + 1]}" for i in range(0, len(pts) - 1, 2)]
        return "M" + "L".join(pairs) + ("Z" if tag == "polygon" else "")
    if tag == "line":
        return f"M{g('x1')},{g('y1')}L{g('x2')},{g('y2')}"
    return None


def _style(el):
    st = dict(kv.split(":", 1) for kv in (el.get("style") or "").replace(" ", "").split(";") if ":" in kv)
    return {k: st.get(k, el.get(k)) for k in ("fill", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin")}


def flatten(svg_text):
    root = ET.fromstring(svg_text)
    for el in root.iter():
        if el.tag.replace(NS, "") in REFUSE:
            raise SystemExit(f"<{el.tag.replace(NS, '')}> found: rebuild that part with the primitives")
    layers = {}
    for el in root.iter():
        tag = el.tag.replace(NS, "")
        d = _shape_d(el, tag)
        if not d:
            continue
        st = _style(el)
        p = pathops.Path()
        parse_path(d, p.getPen())
        m = _matrix(el.get("transform"))
        if m != (1, 0, 0, 1, 0, 0):
            p = p.transform(*m)
        fill = st["fill"] if st["fill"] is not None else "#000000"
        if fill != "none" and tag not in ("polyline", "line"):
            layers.setdefault(fill, []).append(p)
        if st["stroke"] and st["stroke"] != "none":
            sp = pathops.Path()
            parse_path(d, sp.getPen())
            if m != (1, 0, 0, 1, 0, 0):
                sp = sp.transform(*m)
            cap = {"round": pathops.LineCap.ROUND_CAP, "square": pathops.LineCap.SQUARE_CAP}.get(
                st["stroke-linecap"], pathops.LineCap.BUTT_CAP)
            join = {"round": pathops.LineJoin.ROUND_JOIN, "bevel": pathops.LineJoin.BEVEL_JOIN}.get(
                st["stroke-linejoin"], pathops.LineJoin.MITER_JOIN)
            sp.stroke(_num(st["stroke-width"], 1.0), cap, join, 4.0)
            sp.convertConicsToQuads()
            layers.setdefault(st["stroke"], []).append(sp)
    out = []
    painted = pathops.Path()
    for fill, paths in reversed(list(layers.items())):      # later layers paint over earlier ones
        acc = paths[0]
        for q in paths[1:]:
            acc = pathops.op(acc, q, pathops.PathOp.UNION)
        visible = pathops.op(acc, painted, pathops.PathOp.DIFFERENCE)
        painted = pathops.op(painted, acc, pathops.PathOp.UNION)
        pen = SVGPathPen(None, ntos=lambda v: f"{v:.3f}".rstrip("0").rstrip("."))
        visible.draw(pen)
        out.insert(0, f'  <path fill="{fill}" d="{pen.getCommands()}"/>')
    vb = root.get("viewBox")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">\n'
            f'  <!-- flattened from hand-written SVG -->\n' + "\n".join(out) + "\n</svg>\n")


if __name__ == "__main__":
    src = open(sys.argv[1], encoding="utf-8").read()
    open(sys.argv[2], "w", encoding="utf-8").write(flatten(src))
    print(sys.argv[2])
