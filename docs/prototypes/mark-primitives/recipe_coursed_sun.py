"""Route C (unexpected) - ABSTRACT: a sun laid in courses of tiles.

Idea: the product IS the sun. A disc is cut into horizontal courses, and each course
is split by vertical joints in running bond, the way roof tiles are laid. Reads as a
sun from afar and as a tiled roof up close. One colour (amber) on purpose: the joints
carry the idea, so it must survive mono.

Usage: python -B recipe_coursed_sun.py OUT_DIR [r1|r2]
"""
import sys

from brand import AMBER, BOX, PAD
from primitives import Mark

REVS = {
    # r1: first instinct - 5 courses, thin joints, two vertical joints per course.
    "r1": dict(courses=5, joint=3.5, vjoints=2, top_cut=0.0),
    # r2 (after viewing r1): r1 read as a brick ball and collapsed at 16 px. Fewer, fatter courses,
    # joints >= 1 px at 16 px, one vertical joint per course. Parameter-only change, as a test.
    "r2": dict(courses=3, joint=6.5, vjoints=1, top_cut=0.0),
}


def build(rev):
    p = REVS[rev]
    m = Mark(f"coursed_sun_{rev}", BOX, note="disc in running-bond tile courses")
    r = BOX / 2 - PAD
    # rule 1: a lone disc in a square live area looks small; let it overshoot the padding a little
    r += m.overshoot(2 * r, 0.02)
    cx = cy = BOX / 2
    disc = m.circle(cx, cy, r)
    n, j = p["courses"], p["joint"]
    top = cy - r
    h = (2 * r - (n - 1) * j) / n
    cutters = []
    for i in range(1, n):
        y = top + i * h + (i - 1) * j
        cutters.append(m.rect(0, y, BOX, j))
    # vertical joints in running bond: alternate offsets per course
    for i in range(n):
        y0 = top + i * (h + j)
        k = p["vjoints"]
        for v in range(k):
            frac = (v + 1) / (k + 1) + (0.5 / (k + 1) if i % 2 else 0) - 0.25 / (k + 1)
            x = cx - r + frac * 2 * r - j / 2
            cutters.append(m.rect(x, y0 - 0.01, j, h + 0.02))
    sun = m.difference(disc, *cutters)
    return m, [(sun, AMBER)]


if __name__ == "__main__":
    out, rev = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "r1")
    m, layers = build(rev)
    print(m.write(f"{out}/coursed_sun_{rev}", layers))
