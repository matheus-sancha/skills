#!/usr/bin/env python3
"""Runtime probe for the brand-identity skill (throwaway prototype).

Answers two questions on whatever surface runs it (Claude Code, claude.ai, Cowork):
  1. Does the pinned drawing stack install and work?   ->  probe.py install
  2. Can the model genuinely view a PNG it rendered?   ->  probe.py challenge / probe.py check
Then prints one line to paste back:                    ->  probe.py report

The vision challenge uses only the standard library (its own PNG writer and bitmap
font), so it runs even where the install fails. Its answer is stored only as a salted
hash, so a model cannot pass by reading files instead of looking at the image.
"""
import hashlib
import json
import os
import platform
import random
import secrets
import struct
import subprocess
import sys
import time
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATE = Path.cwd() / ".probe"
LOCK = HERE / "requirements.lock"

SHAPES = ("circle", "square", "triangle")
CORNERS = ("top-left", "top-right", "bottom-left", "bottom-right")
# Unambiguous characters only: no 0/O, 1/I/L, 2/Z, 5/S, 8/B.
ALPHABET = "34679ACDEFGHJKMNPQRTUVWXY"


# --------------------------------------------------------------------------- state

def _load():
    try:
        return json.loads((STATE / "result.json").read_text())
    except (OSError, ValueError):
        return {}


def _save(result):
    STATE.mkdir(exist_ok=True)
    (STATE / "result.json").write_text(json.dumps(result, indent=2))


# --------------------------------------------------------------------------- install

def _venv_dir():
    if os.environ.get("BRAND_PROBE_VENV"):
        return Path(os.environ["BRAND_PROBE_VENV"])
    cache = Path.home() / ".cache" / "brand-identity-probe" / "venv"
    try:
        cache.parent.mkdir(parents=True, exist_ok=True)
        test = cache.parent / ".write-test"
        test.write_text("ok")
        test.unlink()
        return cache
    except OSError:
        return Path.cwd() / ".venv"


def _venv_python(venv):
    return venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


SMOKE = r"""
import json, time
out = {}
t = time.time()
import pathops
a = pathops.Path(); a.moveTo(0, 0); a.lineTo(10, 0); a.lineTo(10, 10); a.lineTo(0, 10); a.close()
b = pathops.Path(); b.moveTo(5, 5); b.lineTo(15, 5); b.lineTo(15, 15); b.lineTo(5, 15); b.close()
u = pathops.op(a, b, pathops.PathOp.UNION)
out["pathops_union_bounds"] = list(u.bounds)
from fontTools.pens.svgPathPen import SVGPathPen
pen = SVGPathPen(None); u.draw(pen)
d = pen.getCommands()
out["svg_path"] = d
import uharfbuzz, fontTools
out["uharfbuzz"] = uharfbuzz.__version__ if hasattr(uharfbuzz, "__version__") else "ok"
import resvg_py
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 15 15"><path d="%s"/></svg>' % d
png = bytes(resvg_py.svg_to_bytes(svg_string=svg, width=48, height=48))
out["resvg_png_bytes"] = len(png)
out["resvg_png_magic_ok"] = png[:8] == b"\x89PNG\r\n\x1a\n"
import shapely, svgpathtools, numpy, scipy, skimage, PIL
out["imports_ok"] = True
out["smoke_seconds"] = round(time.time() - t, 2)
print(json.dumps(out))
"""


def cmd_install(_args):
    result = _load()
    result.update({
        "python": platform.python_version(),
        "platform": f"{platform.system()}-{platform.machine()}",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
    })
    venv = _venv_dir()
    result["venv"] = str(venv)
    py = _venv_python(venv)
    t0 = time.time()
    steps = []
    if not py.exists():
        r = subprocess.run([sys.executable, "-m", "venv", str(venv)], capture_output=True, text=True)
        steps.append(("venv", r.returncode, r.stderr[-400:]))
        if r.returncode != 0:
            result.update(install="FAIL", install_error="venv creation failed: " + r.stderr[-300:])
            _save(result)
            print(json.dumps({"install": "FAIL", "step": "venv", "stderr": r.stderr[-300:]}))
            return 1
    r = subprocess.run(
        [str(py), "-m", "pip", "install", "--disable-pip-version-check", "--only-binary=:all:",
         "-q", "-r", str(LOCK)],
        capture_output=True, text=True, timeout=900)
    result["install_seconds"] = round(time.time() - t0, 1)
    if r.returncode != 0:
        tail = (r.stderr or r.stdout)[-600:]
        # Classify the most useful failure causes for the report line.
        low = tail.lower()
        cause = ("network" if any(k in low for k in ("connection", "resolve", "proxy", "403", "timed out"))
                 else "no-wheel" if "no matching distribution" in low else "other")
        result.update(install="FAIL", install_cause=cause, install_error=tail)
        _save(result)
        print(json.dumps({"install": "FAIL", "cause": cause, "stderr_tail": tail}))
        return 1
    s = subprocess.run([str(py), "-c", SMOKE], capture_output=True, text=True, timeout=300)
    if s.returncode != 0:
        result.update(install="OK", smoke="FAIL", smoke_error=s.stderr[-600:])
        _save(result)
        print(json.dumps({"install": "OK", "smoke": "FAIL", "stderr_tail": s.stderr[-600:]}))
        return 1
    smoke = json.loads(s.stdout.strip().splitlines()[-1])
    result.update(install="OK", smoke="OK", smoke_detail=smoke)
    _save(result)
    print(json.dumps({"install": "OK", "smoke": "OK", "install_seconds": result["install_seconds"],
                      "venv": str(venv)}))
    return 0


# --------------------------------------------------------------------------- vision challenge

# 5x7 bitmap glyphs for ALPHABET (rows top to bottom, '#' = ink).
FONT = {
    "3": ["#####", "    #", "   # ", "  ## ", "    #", "#   #", " ### "],
    "4": ["   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "],
    "6": ["  ## ", " #   ", "#    ", "#### ", "#   #", "#   #", " ### "],
    "7": ["#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "],
    "9": [" ### ", "#   #", "#   #", " ####", "    #", "   # ", " ##  "],
    "A": [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "C": [" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "],
    "D": ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    "F": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    "G": [" ### ", "#   #", "#    ", "# ###", "#   #", "#   #", " ####"],
    "H": ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "J": ["  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "],
    "K": ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    "M": ["#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"],
    "P": ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    "R": ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "V": ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"],
    "X": ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    "Y": ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
}


def _png(width, height, pixels):
    """Encode a greyscale image (rows of 0-255 ints) as PNG bytes."""
    raw = b"".join(b"\x00" + bytes(row) for row in pixels)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def _draw_challenge(code, shape, corner, size=512):
    img = [[255] * size for _ in range(size)]
    # Code: 4 glyphs at 12 px per bitmap cell, centred.
    cell, gap = 12, 12
    gw = 5 * cell
    total = len(code) * gw + (len(code) - 1) * gap
    x0, y0 = (size - total) // 2, (size - 7 * cell) // 2
    for i, ch in enumerate(code):
        for r, row in enumerate(FONT[ch]):
            for c, px in enumerate(row):
                if px == "#":
                    for yy in range(y0 + r * cell, y0 + (r + 1) * cell):
                        for xx in range(x0 + i * (gw + gap) + c * cell, x0 + i * (gw + gap) + (c + 1) * cell):
                            img[yy][xx] = 0
    # Shape: 80 px, inset 24 px from the chosen corner.
    s, inset = 80, 24
    left = inset if "left" in corner else size - inset - s
    top = inset if corner.startswith("top") else size - inset - s
    for yy in range(top, top + s):
        for xx in range(left, left + s):
            u, v = (xx - left) / s, (yy - top) / s
            if shape == "square":
                ink = True
            elif shape == "circle":
                ink = (u - 0.5) ** 2 + (v - 0.5) ** 2 <= 0.25
            else:  # upward triangle
                ink = abs(u - 0.5) <= v / 2
            if ink:
                img[yy][xx] = 0
    return _png(size, size, img)


def _digest(salt, code, shape, corner):
    return hashlib.sha256(f"{salt}|{code.upper()}|{shape}|{corner}".encode()).hexdigest()


def cmd_challenge(_args):
    rng = random.SystemRandom()
    code = "".join(rng.choice(ALPHABET) for _ in range(4))
    shape, corner = rng.choice(SHAPES), rng.choice(CORNERS)
    salt = secrets.token_hex(16)
    STATE.mkdir(exist_ok=True)
    (STATE / "challenge.json").write_text(json.dumps({"salt": salt, "digest": _digest(salt, code, shape, corner),
                                                      "issued": time.time(), "attempts": 0}))
    out = Path.cwd() / "probe-challenge.png"
    out.write_bytes(_draw_challenge(code, shape, corner))
    print(json.dumps({"challenge_png": str(out),
                      "instructions": "View the image. Report the 4-character code, the shape "
                                      f"({'/'.join(SHAPES)}) and its corner ({'/'.join(CORNERS)}) with: "
                                      "probe.py check CODE SHAPE CORNER"}))
    return 0


def cmd_check(args):
    if len(args) != 3:
        print("usage: probe.py check CODE SHAPE CORNER", file=sys.stderr)
        return 2
    code, shape, corner = args[0].upper(), args[1].lower(), args[2].lower()
    try:
        ch = json.loads((STATE / "challenge.json").read_text())
    except (OSError, ValueError):
        print(json.dumps({"vision": "NO-CHALLENGE", "hint": "run probe.py challenge first"}))
        return 2
    ch["attempts"] += 1
    (STATE / "challenge.json").write_text(json.dumps(ch))
    ok = ch["attempts"] == 1 and _digest(ch["salt"], code, shape, corner) == ch["digest"]
    result = _load()
    result["vision"] = "OK" if ok else ("FAIL-RETRY" if ch["attempts"] > 1 else "FAIL")
    result["vision_reported"] = f"{code} {shape} {corner}"
    _save(result)
    print(json.dumps({"vision": result["vision"]}))
    return 0 if ok else 1


# --------------------------------------------------------------------------- report

def cmd_report(_args):
    r = _load()
    sd = r.get("smoke_detail", {})
    line = (f"PROBE py={r.get('python', '?')} plat={r.get('platform', '?')} "
            f"install={r.get('install', 'NOT-RUN')}"
            + (f"({r.get('install_cause')})" if r.get("install") == "FAIL" else "")
            + f" t={r.get('install_seconds', '-')}s smoke={r.get('smoke', '-')}"
            + f" pathops={'OK' if sd.get('pathops_union_bounds') else '-'}"
            + f" resvg={'OK' if sd.get('resvg_png_magic_ok') else '-'}"
            + f" vision={r.get('vision', 'NOT-RUN')}")
    print(line)
    return 0


def main(argv):
    cmds = {"install": cmd_install, "challenge": cmd_challenge, "check": cmd_check, "report": cmd_report}
    if not argv or argv[0] not in cmds:
        print(__doc__)
        print("commands: " + ", ".join(cmds))
        return 2
    return cmds[argv[0]](argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
