"""Assemble 07-kit/ from the run folder (references/kit.md), and check it.

Inputs (latest revision of each is used):
  05-refine/master.rN.svg, small-master.rN.svg (optional), wordmark.rN.svg,
  05-refine/lockups/horizontal.rN.svg, stacked.rN.svg
  06-system/tokens/ (tokens.dtcg.json, tokens.json, tokens.css, brand_tokens.dart)
  06-system/graphic-language/*.svg + params.json, 06-system/ui/ (components)
  06-system/type/ (fonts + OFL.txt, optional)
"""
import base64
import hashlib
import io
import json
import re
import shutil
from pathlib import Path

import resvg_py
from PIL import Image

from .palette import contrast
from .render_sheet import recolour

LAYOUTS = ["horizontal", "stacked", "mark", "wordmark"]
COLOURWAYS = {"colour": None, "black": "#000000", "white": "#ffffff"}
NOTICE = ("These marks have not been searched against trademark registers. Before using one commercially, "
          "have a trademark search done in each market you'll trade in. Free starting points: WIPO Global "
          "Brand Database (image search), INPI (Brazil), USPTO and EUIPO.")


def latest(folder, name):
    revs = []
    for p in Path(folder).glob(f"{name}.r*.svg"):
        m = re.match(rf"{re.escape(name)}\.r(\d+)\.svg$", p.name)
        if m:
            revs.append((int(m.group(1)), p))
    return max(revs)[1] if revs else None


def png(svg, width, bg=None):
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    h = max(1, round(width * vb[3] / vb[2]))
    kw = {"background": bg} if bg else {}
    return bytes(resvg_py.svg_to_bytes(svg_string=svg, width=width, height=h, **kw))


def _square(svg, px):
    im = Image.open(io.BytesIO(png(svg, px))).convert("RGBA")
    side = max(im.size)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    return sq.resize((px, px), Image.LANCZOS)


def _data_uri(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode()


def assemble(run, slug, name, idea, rationale=""):
    run = Path(run)
    ref, sysd, kit = run / "05-refine", run / "06-system", run / "07-kit"
    kit.mkdir(parents=True, exist_ok=True)
    src = {"mark": latest(ref, "master"), "wordmark": latest(ref, "wordmark"),
           "horizontal": latest(ref / "lockups", "horizontal"), "stacked": latest(ref / "lockups", "stacked")}
    small = latest(ref, "small-master")
    missing = [k for k, v in src.items() if v is None]
    if missing:
        raise SystemExit(f"missing refine outputs: {missing}")
    svgdir, pngdir, fav = kit / "logo/svg", kit / "logo/png", kit / "logo/favicon"
    for d in (svgdir, pngdir, fav):
        d.mkdir(parents=True, exist_ok=True)
    texts = {k: Path(v).read_text(encoding="utf-8") for k, v in src.items()}
    if small:
        texts["mark-small"] = small.read_text(encoding="utf-8")
    for layout, svg in texts.items():
        for cw, ink in COLOURWAYS.items():
            out = svg if ink is None else recolour(svg, ink)
            fn = f"{slug}-{layout}-{cw}"
            (svgdir / f"{fn}.svg").write_text(out, encoding="utf-8")
            for w in (512, 1024):
                (pngdir / f"{fn}-{w}.png").write_bytes(png(out, w))
    fav_svg = texts.get("mark-small", texts["mark"])
    (fav / "favicon.svg").write_text(fav_svg, encoding="utf-8")
    _square(fav_svg, 48).save(fav / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    for px, fn in ((180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")):
        _square(fav_svg, px).save(fav / fn)
    for sub in ("tokens", "graphic-language", "type"):
        if (sysd / sub).exists():
            shutil.copytree(sysd / sub, kit / sub, dirs_exist_ok=True)
    if (sysd / "ui").exists():
        shutil.copytree(sysd / "ui", kit / "ui", dirs_exist_ok=True)
    tokens = json.loads((kit / "tokens/tokens.json").read_text(encoding="utf-8"))
    sheet_svg = brand_sheet(name, idea, texts, tokens, kit / "graphic-language")
    (kit / "brand-sheet.png").write_bytes(png(sheet_svg, 2400, "#ffffff"))
    (kit / "brand-sheet.html").write_text(
        f'<!doctype html><html><head><meta charset="utf-8"><title>{name} brand sheet</title>'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<style>body{{margin:0;background:#fff}}img{{width:100%;height:auto;display:block}}</style></head>'
        f'<body><img alt="{name} brand sheet" src="{_data_uri(sheet_svg)}"></body></html>', encoding="utf-8")
    (kit / "rationale.md").write_text(f"# {name}: rationale\n\n**Idea.** {idea}\n\n{rationale}\n", encoding="utf-8")
    readme(kit, name, idea, tokens, slug, bool(small))
    manifest(kit)
    return kit


def _swatches(tokens):
    roles = {t["name"]: t["value"] for t in tokens["color"]["tokens"] if isinstance(t["value"], dict)}
    ident = [t["value"] for t in tokens["color"]["tokens"] if t["name"].startswith("identity-")]
    return roles, ident


def brand_sheet(name, idea, texts, tokens, gl_dir):
    W = 1200
    roles, ident = _swatches(tokens)
    surf, ink = roles["surface"]["light"], roles["on-surface"]["light"]
    el = [f'<text x="60" y="90" font-family="sans-serif" font-size="44" font-weight="700" fill="{ink}">{name}</text>',
          f'<text x="60" y="135" font-family="sans-serif" font-size="22" fill="{ink}">1 · {idea}</text>']

    def place(svg, x, y, w, h, ink_=None):
        s = svg if ink_ is None else recolour(svg, ink_)
        return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{_data_uri(s)}" preserveAspectRatio="xMidYMid meet"/>'

    def label(x, y, t, size=16):
        return f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" fill="{ink}">{t}</text>'

    el.append(label(60, 190, "2 · Logo system"))
    y = 210
    for row, (cw, bg) in enumerate((("colour", surf), ("black", "#ffffff"), ("white", roles["primary"]["light"]))):
        el.append(f'<rect x="60" y="{y}" width="1080" height="110" fill="{bg}"/>')
        for i, lay in enumerate(("horizontal", "stacked", "mark")):
            el.append(place(texts[lay], 80 + i * 360, y + 10, 320, 90, COLOURWAYS[cw]))
        y += 120
    el.append(label(60, y + 30, "3 · Clear space = 0.5 × mark height · minimum size 16 px (mark), 24 px tall (lockup)"))
    el.append(place(texts["mark"], 120, y + 80, 120, 120))
    el.append(f'<rect x="90" y="{y + 50}" width="180" height="180" fill="none" stroke="{ink}" stroke-dasharray="6 6"/>')
    for i, px in enumerate((16, 24, 32, 48)):
        el.append(place(texts.get("mark-small", texts["mark"]), 340 + i * 80, y + 140 - px / 2, px, px))
    y += 280
    el.append(label(60, y, "4 · Colour (screen values only; ask your printer to specify CMYK or a spot colour from these)"))
    keys = ["primary", "primary-container", "on-surface", "surface", "link"]
    for i, k in enumerate(keys):
        c = roles[k]["light"]
        el.append(f'<rect x="{60 + i * 216}" y="{y + 20}" width="200" height="120" fill="{c}" stroke="{ink}" stroke-width="0.5"/>')
        el.append(label(60 + i * 216, y + 165, f"{k} {c}", 14))
        el.append(label(60 + i * 216, y + 185, f"{contrast(c, surf):.2f}:1 on surface", 13))
    bar = [("surface", 6), ("on-surface", 3), ("primary", 1)]
    x = 60
    for k, f in bar:
        el.append(f'<rect x="{x}" y="{y + 200}" width="{108 * f}" height="16" fill="{roles[k]["light"]}" stroke="{ink}" stroke-width="0.5"/>')
        x += 108 * f
    y += 260
    el.append(label(60, y, "5 · Type"))
    fams = tokens["type"]["families"]
    styles = [s for g in tokens["type"]["groups"] for s in g["styles"]]
    yy = y + 10
    for s in sorted(styles, key=lambda s: -int(s["fontSize"].rstrip("px")))[:5]:
        fs = int(s["fontSize"].rstrip("px"))
        yy += fs + 12
        fam = fams.get("display" if s["name"] in ("display", "headline") else "text", "sans-serif").replace("'", "")
        el.append(f'<text x="60" y="{yy}" font-family="{fam}" font-size="{fs}" font-weight="{s["fontWeight"]}" fill="{ink}">'
                  f'{s["name"]} · {name} {fs}px</text>')
    el.append(place(texts["wordmark"], 760, y + 30, 380, 120))
    y = yy + 50
    el.append(label(60, y, "6 · Graphic language (mark → part → pattern)"))
    gl = sorted(Path(gl_dir).glob("*.svg")) if Path(gl_dir).exists() else []
    if gl:
        el.append(place(gl[0].read_text(encoding="utf-8"), 60, y + 15, 1080, 160))
    y += 200
    el.append(label(60, y, "7 · Applications"))
    p = roles["primary"]["light"]
    el.append(f'<rect x="60" y="{y + 15}" width="160" height="160" rx="36" fill="{p}"/>')
    el.append(place(texts.get("mark-small", texts["mark"]), 90, y + 45, 100, 100, roles["on-primary"]["light"]))
    el.append(f'<rect x="260" y="{y + 15}" width="880" height="160" fill="{roles["surface-raised"]["light"]}"/>')
    el.append(place(texts["horizontal"], 290, y + 55, 360, 80))
    y += 210
    el.append(label(60, y, "8 · Don't"))
    el.append(f'<g transform="translate(60 {y + 15}) scale(1.6 0.8)">{_inner(texts["mark"], 100)}</g>')
    el.append(place(texts["mark"], 460, y + 15, 100, 100, "#7f7f7f"))
    el.append(f'<rect x="760" y="{y + 15}" width="160" height="100" fill="{roles["primary-container"]["light"]}"/>')
    el.append(place(texts["mark"], 790, y + 20, 90, 90, roles["primary"]["light"]))
    el.append(label(60, y + 140, "stretch it · recolour it · place it on a low-contrast ground", 14))
    y += 190
    words, line = NOTICE.split(), ""
    for w in words:
        if len(line) + len(w) > 150:
            el.append(label(60, y, line, 12)); y += 18; line = ""
        line += w + " "
    el.append(label(60, y, line, 12))
    H = y + 40
    el.insert(0, f'<rect width="{W}" height="{H}" fill="{surf}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">{"".join(el)}</svg>'


def _inner(svg, size):
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    body = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", svg, flags=re.S)
    k = size / max(vb[2], vb[3])
    return f'<g transform="scale({k}) translate({-vb[0]} {-vb[1]})">{body}</g>'


def readme(kit, name, idea, tokens, slug, has_small):
    roles, ident = _swatches(tokens)
    rows = "\n".join(f"| `{k}` | {v['light']} / {v['dark']} | {next(t['usage'] for t in tokens['color']['tokens'] if t['name'] == k)} |"
                     for k, v in roles.items())
    txt = f"""## The mark

{idea}

## Logo files

| File | Use |
|---|---|
| `logo/svg/{slug}-horizontal-*.svg` | Default lockup, wide spaces |
| `logo/svg/{slug}-stacked-*.svg` | Narrow or square spaces |
| `logo/svg/{slug}-mark-*.svg` | App icons, avatars, favicons above 32 px |
{"| `logo/svg/" + slug + "-mark-small-*.svg` | 16–32 px only (small master) |" if has_small else ""}
| `logo/svg/{slug}-wordmark-*.svg` | Where the mark is already present |
| `logo/favicon/` | Browser and home-screen icons |

Colourways: `colour` on light grounds, `black` for one-colour printing, `white` reversed on dark or brand grounds.

## Using the logo

- Clear space: half the mark's height on every side.
- Minimum size: 16 px for the mark{" (use the small master)" if has_small else ""}; 24 px tall for lockups.
- Don't stretch, recolour, outline, add effects, or place on low-contrast or busy grounds.

## Colour

Identity colours (exact, used by the mark): {", ".join(f"`{c}`" for c in ident)}.
Screen values only; ask your printer to specify CMYK or a spot colour from these.

| Role | Light / Dark | Use |
|---|---|---|
{rows}

## Type

{", ".join(f"{k}: {v}" for k, v in tokens["type"]["families"].items())}. Text roles in `tokens/tokens.json`.

## Motion

Durations and easings are in `tokens/tokens.dtcg.json` (`motion`) and as `--motion-*` in `tokens/tokens.css`. Use the
standard easing for UI transitions; the logo sting (if present in `motion/`) uses the same curves.

## Trademark

{NOTICE}
"""
    (kit / "README.md").write_text(txt, encoding="utf-8")


REQUIRED = ["README.md", "rationale.md", "brand-sheet.html", "brand-sheet.png",
            "logo/favicon/favicon.svg", "logo/favicon/favicon.ico", "logo/favicon/apple-touch-icon.png",
            "logo/favicon/icon-192.png", "logo/favicon/icon-512.png",
            "tokens/tokens.dtcg.json", "tokens/tokens.json", "tokens/tokens.css", "tokens/brand_tokens.dart"]


def manifest(kit):
    files = []
    for p in sorted(Path(kit).rglob("*")):
        if p.is_file() and p.name != "manifest.json":
            files.append({"path": p.relative_to(kit).as_posix(), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
    (Path(kit) / "manifest.json").write_text(json.dumps({"files": files}, indent=1), encoding="utf-8")


def check(kit, slug):
    kit = Path(kit)
    need = list(REQUIRED)
    for lay in LAYOUTS:
        for cw in COLOURWAYS:
            need += [f"logo/svg/{slug}-{lay}-{cw}.svg", f"logo/png/{slug}-{lay}-{cw}-512.png",
                     f"logo/png/{slug}-{lay}-{cw}-1024.png"]
    missing = [n for n in need if not (kit / n).exists()]
    texty = [p for p in (kit / "logo/svg").glob("*.svg") if "<text" in p.read_text(encoding="utf-8")]
    comps = ["Button", "Input", "Checkbox", "Card", "NavBar", "Alert"]
    missing += [f"ui/components/{c}/preview.html" for c in comps if not (kit / f"ui/components/{c}/preview.html").exists()]
    problems = missing + [f"live <text> in {p.name}" for p in texty]
    return problems
