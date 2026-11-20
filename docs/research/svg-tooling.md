# SVG tooling where the skill runs: geometry, booleans, outlining, rendering, viewing, fonts

**Question.** Where the skill runs on Claude (Claude Code, claude.ai, Cowork, and the Claude API as the strictest case), which tools can it rely on for: geometric construction and boolean path operations; converting text to outlines; rendering SVG to PNG at several sizes; and showing images to the user mid-conversation, including through Artifacts? For each candidate: does it install without network surprises, what is its licence, and does a minimal example work? And where can openly licensed typefaces be obtained offline or on demand?

**Purpose.** Input to the spec for a Claude Agent Skill that designs brand identities and delivers an SVG logo system, palette, type pairing, brand sheet and UI design system. The binding decisions are **hybrid drawing** (Python scripts supply the geometry primitives and the agent composes them) and a **render-then-rubric gate** (marks are rendered at 16/32/48/256 px and in mono, then scored by script and by the model). The primitives and script checks those tools must support are listed in [mark-craft.md §10](mark-craft.md). This note is meant to clear four open questions: *the primitive library's interface*, *typography sourcing*, *new capabilities to create*, and *delivery surface*.

> **How these sources were read. Please read this first.**
> **Observed** means I installed and ran it on 2026-11-17 in this Claude Code cloud container (Linux x86_64, Python 3.13.18, outbound HTTPS through an agent proxy). Each package went into a fresh venv in the session scratchpad, never into the repo. Licences come from the installed `*.dist-info/METADATA` and `LICENSE` files, or from Debian `/usr/share/doc/<pkg>/copyright`, as opened here. Every API named below was run. Script source and outputs are in the scratchpad (`issue9/scripts`, `issue9/out`) and are not kept.
> Anthropic product facts come from pages read in full: the [code execution tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool), the [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), the support article [Create and edit files with Claude](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude), [Cowork network access](https://claude.com/docs/cowork/guide/network-access), and the Claude Code [tools reference](https://code.claude.com/docs/en/tools-reference) and [artifacts](https://code.claude.com/docs/en/artifacts) pages.
> **I could not run anything inside claude.ai chat, Cowork or the API sandbox.** Claims about those surfaces rest on their docs and are marked **(docs only)**. Inferences about them are marked **(inference)**.
> `openfontlicense.org`, `scripts.sil.org`, `tug.ctan.org`, `fonts.google.com`, `api.fontsource.org` and `cdn.jsdelivr.net` were blocked by this session's network policy. GitHub *web* URLs were refused because the repo was not attached to the session; `raw.githubusercontent.com` worked. The OFL FAQ was therefore read in an older mirrored copy (§6.3).

---

## 1. Answer

**One pip-installable, wheel-only stack does everything the gate needs, with no system packages:**
- `skia-pathops` + `fontTools` handle geometry, booleans and outlines;
- `uharfbuzz` shapes text;
- `resvg-py` renders;
- `numpy`/`scipy`/`scikit-image` measure.

All installed from PyPI as prebuilt wheels in about 19 s, with no compiler and no system libraries (§2).

**That stack is only reachable where pip can reach PyPI.** That means Claude Code; claude.ai with network egress on, which is the default for Free/Pro/Max/Ultra; and Cowork with "Package managers only" or wider.
**The Claude API sandbox, and claude.ai or Cowork with egress off, cannot install anything** ([code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool); [Skills runtime constraints](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#runtime-environment-constraints)). There, only `matplotlib` + `fontTools` + `Pillow` + `scipy` are available (preinstalled or a declared dependency). I verified a renderer built from exactly those (§3.4). It is a usable degraded mode, not an equal one.

**Fonts.** The one on-demand route reachable on *every* networked surface is the **npm registry** (`@fontsource` / `@fontsource-variable` packages). Every package checked is OFL-1.1, and a plain `curl` to `registry.npmjs.org` works without npm itself. `raw.githubusercontent.com/google/fonts` and the Google Fonts CSS API worked *here*, but neither host is on claude.ai's approved list ([support article, "Approved network domains"](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude)). The only route that always works is **bundling** a curated OFL set inside the skill. The OFL permits this (§6).

| Need | Pick | Licence (as seen) | Install, as observed | Verified example | Fallback without network |
|---|---|---|---|---|---|
| Booleans (union, difference, intersection, xor), overlap removal, stroke→outline | **skia-pathops 0.9.2** | BSD-3-Clause | abi3 wheel; links only libc/libstdc++ | Union of two r=30 circles 30 apart: area 4550.46 vs analytic 4549.3 (curve approximation error 0.03 %); output stays cubic Béziers (§3.1) | **None preinstalled.** Shapely is not on the API list either. Keep booleans out of the offline path, or write winding-correct contours directly |
| Measurement geometry (buffer/offset, min gap, centroid, distance) | **shapely 2.2.0** (GEOS 3.14.1) | BSD-3-Clause | wheel | min gap = 50.0; union centroid (55, 50) vs bbox centre (55, 50) (§3.1) | scipy distance transform on rasters |
| Curve analysis (curvature, tangents, extrema, exact bbox) | **svgpathtools 1.8.0** | MIT | pure Python | κ at t=0.5 on an r=30 arc = 0.03313 (1/r = 0.03333); finds the missing-extremum t=0.5 (§3.1) | Vendor it (pure Python) or use numpy on Bézier polynomials |
| Parse arbitrary SVG (transforms, shapes→paths) | **svgelements 1.9.6**; **picosvg 0.23.0** to normalise (bakes transforms, converts strokes to fills) | MIT; Apache-2.0 | pure Python (picosvg pulls skia-pathops + lxml) | `circle` inside `translate scale` → arc path; picosvg turned a stroked line into a filled outline (§3.1) | svgelements can be vendored; picosvg cannot (needs skia-pathops) |
| Text → outlines | **fontTools 4.68.0** pens + **uharfbuzz 0.57.0** shaping | MIT; Apache-2.0 | wheels | "Acme" in Inter Bold (CFF) and Manrope[wght]@800 (TrueType variable) → one `<path>`. Kerning applied: "AVATAR" advance 6774 with kern vs 7214 without (§4) | fontTools is a declared matplotlib dependency (present on API, **inference**). Without HarfBuzz you get no kerning unless you read GPOS yourself |
| SVG → PNG at N px | **resvg-py 0.5.0** | MIT (wrapper; resvg's own licence not checked) | abi3 wheel with no system deps | 16/32/48/256 px renders in 1.6–15 ms each (§5) | matplotlib Agg path fill: mean abs. difference from resvg 3.3 / 0.9 / 0.2 (of 255) at 16 / 48 / 256 px (§3.4) |
| SVG → PNG, alternatives | cairosvg 2.9.1 (LGPL-3.0-or-later; **needs system libcairo**); `rsvg-convert` 2.58 (LGPL-2+, apt); Inkscape 1.2.2 (GPL, apt, 66 packages); Chromium via Node Playwright 1.63.0 (Apache-2.0, preinstalled here) | — | — | All produced 16/48/256 px PNGs (§5) | — |
| Scoring (SSIM, distance transform, skeleton) | **scikit-image 0.26.0** + **scipy 1.18.1** | BSD-3-Clause | wheels (scipy 109 MB installed) | Hairline ring: stroke 0.35 px at 16 px, **yet SSIM = 0.964**. SSIM alone does not catch it (§5.2) | scipy is preinstalled on the API; SSIM is ~20 lines of numpy |
| Show the model its renders | `Read` on a PNG (Claude Code) | — | built in | Contact sheet viewed in this session (§7) | **Unverified** on claude.ai/Cowork/API |
| Show the user | Artifact page (Claude Code CLI/desktop, claude.ai); `SendUserFile` (Claude Code cloud/Remote Control) | — | — | **Docs only**: no artifact was published and no file was sent | Write files to the outputs folder (claude.ai download) |
| Fonts on demand | `@fontsource-variable/<family>` tarball from `registry.npmjs.org` | OFL-1.1 (package.json and LICENSE) | `curl` or `npm pack` | Manrope variable woff2 → decompressed to TTF → outlined identically to the google/fonts TTF (§6) | Bundle a curated OFL set in `assets/fonts/` |

---

## 2. Installation, observed

**Command:** `python3 -m venv venv && pip install --only-binary=:all: skia-pathops picosvg fonttools shapely svgpathtools svgelements cairosvg resvg-py pillow scikit-image numpy scipy`, followed by `uharfbuzz brotli` and, for the fallback test, `matplotlib`.

- **Wheels only.** `--only-binary=:all:` succeeded for every package, so nothing compiled. The native wheels are `manylinux_2_17`–`2_27` x86_64; skia-pathops, resvg-py and uharfbuzz are `abi3`. `ldd` on `pathops/_pathops.abi3.so` and `uharfbuzz/_harfbuzz.abi3.so` shows only libc, libm, libstdc++ and libgcc_s. resvg-py likewise needs no system graphics library.
- **Hosts contacted:** `pypi.org` and `files.pythonhosted.org` only. Both are on this container's `NO_PROXY` list and on claude.ai's approved list ([support article](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude)).
- **Size:** scipy (109 MB), scikit-image (32 MB) and fontTools (29 MB) dominate. The core drawing set (pathops 9.1 MB, resvg_py 2.9 MB, uharfbuzz 5.0 MB, shapely 3.7 MB) is small.
- **cairosvg is the one network-clean-looking package with a hidden system dependency.** `cairocffi/__init__.py` calls `dlopen` for `libcairo.so.2` (lines 60–62). With that library masked in a mount namespace, `import cairosvg` failed with `cannot load library 'libcairo.so.2'…`. libcairo 1.18.0 happens to be preinstalled in this container. **Do not depend on cairosvg.**
- **System tools.** `rsvg-convert` and `inkscape` were *not* installed here. `apt-get update && apt-get install -y librsvg2-bin inkscape` took 23 s from `archive.ubuntu.com` (66 new packages, about 96 MB for Inkscape). `archive.ubuntu.com` is on claude.ai's approved list, but whether apt runs as root there is **unverified**. ImageMagick 6.9.12 is preinstalled, but its SVG delegate is `rsvg-convert` (`convert -list delegate`), so it adds nothing.
- **Python Playwright is not installed.** Node Playwright 1.63.0 is preinstalled at `/opt/node-tools/node_modules/playwright`, with Chromium 153 under `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`. That is a property of this container image, not of claude.ai or Cowork **(inference)**.

## 3. Geometry and booleans

### 3.1 Verified examples

**skia-pathops (booleans).** Two circles built with a pen (4 cubics each, k = 0.5522847498), then `pathops.op(a, b, PathOp.UNION)` and the same with `DIFFERENCE`, `INTERSECTION` and `XOR`. Results were drawn to `fontTools.pens.svgPathPen.SVGPathPen`:
```
union bounds (10.0, 20.0, 100.0, 80.0) d= M100.0 50.0C100.0 66.568… 86.568… 80.0 70.0 80.0C64.535… 80.0 59.412… 78.539 55.000… 75.986…
intersection bounds (40.0, 24.013…, 70.0, 75.986…)
area union 4550.463712324304
```
The output stays **cubic**, which matters for the extrema and node-count checks in mark-craft rules 7–8.

**skia-pathops (stroke to outline).** `Path.stroke(width, LineCap.ROUND_CAP, LineJoin.ROUND_JOIN, miter)` expands a stroke into an outline. **Pitfall, observed:** drawing the result immediately raised `UnsupportedVerbError: CONIC`. Calling `p.convertConicsToQuads(); p.simplify()` first gave `M10.0 6.0H90.0Q94.0 6.0 94.0 10.0…Z`.

**skia-pathops (overlap removal).** `Path.simplify(fix_winding=True)` is the overlap-removal and winding-normalisation step. On the Manrope variable glyph "A" at wght 800, it reduced the signed area from 983 290 to 906 006 units² with the same contour count. **Variable-font glyphs ship with overlapping contours**, so run `simplify` before any offset, stroke-width measurement or mono union.

**shapely (measurement).** `Point(x,y).buffer(r, quad_segs=64)`, `.union`, `.difference`, `.distance`, `.centroid` and `LineString(...).buffer(4, cap_style="round", join_style="mitre")` all ran. Results: union area 4548.96, with **345 polygon vertices**. Shapely flattens curves to polylines, so it is for *measuring* (min gap for mono separability, centroid vs bbox for optical centring, offsets for stroke compensation). It is not for emitting final paths.

**svgpathtools (curve analysis).** `parse_path(d)`, `seg.curvature(t)`, `seg.unit_tangent(t)`, `path.length()`, `path.bbox()` and `seg.poly()` all ran. Results:
- curvature of the r=30 arc = 0.03313 (the cubic-circle approximation vs 1/30 = 0.03333);
- `np.roots` on the derivative of `CubicBezier(0, 40j, 100+40j, 100).poly()` found the interior y-extremum at t = 0.5. That is the "missing extremum node" check.

**svgelements (parsing).** `SVG.parse()` resolved `translate(10 0) scale(2)` on a `<circle>` and on a `<rect rx>`; `Path(shape).d()` returned arc paths in user space.

**picosvg (normalising).** `picosvg in.svg` (CLI) and `SVG.parse(p).topicosvg()` (API) did the following:
- baked a group `translate`;
- converted `<circle>` to cubic paths;
- turned a 6-unit round-capped stroked line into a filled outline.

It does **not** merge same-colour overlapping shapes. That needs an explicit `pathops` union.

### 3.2 What maps to mark-craft §10

| mark-craft primitive / check | Backed by (all verified above) |
|---|---|
| booleans, `min_gap(shapes)` | `pathops.op`; `shapely.distance` |
| per-axis stroke offsets, `taper_join` | `pathops` stroke + boolean; shapely `buffer` for measurement. Asymmetric (per-axis) offset is **not** a library call: it needs custom code, e.g. scale → buffer → unscale (**inference, not run**) |
| `add_extrema`, `remove_redundant_nodes`, G1 angle, G2 jump, handle triangle | svgpathtools `poly`/`derivative`/`curvature`/`unit_tangent` + numpy. Splitting a segment at t is needed for `add_extrema`; svgpathtools segments have `split(t)` per its API, but **I did not run it** |
| circle/arc/line tangent constructions | No library offers a "construction log". Write it in plain Python and emit cubics with k = 0.5523 per quarter arc (as run above) |
| centroid vs bbox | shapely `centroid`/`bounds` |
| rasterise at N px | resvg-py (§5) |
| distance transform, skeleton, SSIM | `scipy.ndimage.distance_transform_edt`, `skimage.morphology.skeletonize`, `skimage.metrics.structural_similarity` (§5.2) |

### 3.3 Not adopted

**Shapely for output** (it flattens curves). **cairosvg** (system libcairo). **Inkscape actions for booleans**: `--actions="select-all;path-union"` ran but printed only a GTK warning; I did not check its output, so it is **unverified** and in any case too heavy.

### 3.4 Offline fallback (API sandbox, egress-off claude.ai or Cowork)

The API container lists `numpy, scipy, … pillow, … matplotlib … reportlab[pycairo]` and "no internet access" ([code execution tool, Pre-installed libraries](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#pre-installed-libraries)) **(docs only)**. matplotlib's wheel metadata declares `Requires-Dist: fonttools>=4.28.2` (read here), so fontTools should be present wherever matplotlib is **(inference)**.

A ~25-line renderer was verified here. It is a `fontTools.pens.basePen.BasePen` subclass that emits `matplotlib.path.Path` codes, fed by `fontTools.svgLib.path.parse_path(d, pen)` and filled with `PathPatch` on an Agg figure at `dpi = N`. Against resvg, the mean absolute grey difference was **3.32 / 0.93 / 0.21 (of 255) at 16 / 48 / 256 px**.

**Pitfall, observed:** matplotlib fills by non-zero winding. A path whose hole has the same winding as its outer contour rendered filled (difference 35.7). The fix was to normalise winding first; I used `pathops.simplify`, which is not available offline. The offline-safe rule is that **the primitive library must emit holes counter-wound to their outer contour**. `fontTools.pens.reverseContourPen.ReverseContourPen` exists for that, but I did not run it.

## 4. Text to outlines

**Recipe (verified):**
1. Shape the text with HarfBuzz: `hb.Blob.from_file_path` → `hb.Face` → `hb.Font`, `font.set_variations({"wght": 800})`, `hb.Buffer().add_str()`, `guess_segment_properties()`, then `hb.shape(font, buf, {"kern": True, "liga": True})`.
2. Draw each glyph with fontTools: `TTFont(path).getGlyphSet(location={"wght": 800})`, `glyphSet[name].draw(TransformPen(SVGPathPen(gs), (s,0,0,-s,x,y)))`.

The y-flip is in the transform. Glyph names come from `tt.getGlyphOrder()[info.codepoint]`, because after shaping, `codepoint` holds the glyph id.

**Observed:**
- Inter Bold (`.otf`, CFF) → `M2.392578125 72.75390625H18.84765625L24.267578125 55.859375…`, run width 282.0 at size 100.
- Manrope[wght] at 200 vs 800 → widths 253.5 vs 278.0, so the variable instance applied.
- Kerning: "AVATAR" advance sum 6774 with `kern` on vs 7214 off.
- Rendered with resvg using `skip_system_fonts=True`, the outlined SVGs drew correctly. I viewed the PNG; the file contains no `<text>`, so the wordmark is font-independent.

**Pitfall, observed:** `hb.Blob.from_file_path` on a **WOFF2** file shaped garbage: a run width of 100.0 and rectangles in place of glyphs. HarfBuzz does not decompress WOFF2. Decompress first with `t = TTFont(woff2); t.flavor = None; t.save(ttf)`. This needs the `brotli` wheel (MIT). After that, the output was byte-identical to the google/fonts TTF.

**Alternative (verified):** `inkscape t.svg --export-text-to-path --export-plain-svg` turned `<text font-family="Inter" font-weight="700">Acme</text>` into `<path>`s in 0.3 s. It resolves fonts through fontconfig, so the font must be installed system-wide, and it needs apt. It is not recommended as the primary path.

**Implication:** wordmark spacing (mark-craft rule 20) can be measured and adjusted per pair on the shaped glyph positions *before* outlining, because HarfBuzz exposes `x_advance` and `x_offset` per glyph.

## 5. Rendering SVG to PNG

### 5.1 Renderers compared

A test mark (circle with an even-odd triangle hole, plus a `<text>` element) was rendered at 16/32/48/256 px:
- `cairosvg.svg2png(bytestring=…, write_to=…, output_width=n, output_height=n)`;
- `resvg_py.svg_to_bytes(svg_string=…, width=n, height=n)` (also accepts `svg_path`, `background`, `skip_system_fonts`);
- `rsvg-convert -w n -h n in.svg -o out.png`;
- `inkscape in.svg --export-type=png --export-width=48`;
- Chromium via Playwright: `page.setContent(svg)`, `page.screenshot({omitBackground: true})`.

All produced correctly sized RGBA PNGs.

**Mean |Δalpha| between renderers (0–255):**
- at 16 px: cairo–resvg 3.0, cairo–rsvg 0.43, resvg–rsvg 2.7;
- at 256 px: all ≤ 0.23.

At favicon size, **the choice of rasteriser shifts pixel metrics by a few percent**, so the gate must pin one renderer and calibrate its thresholds on it **(inference)**. All three Python-reachable renderers drew the `<text>` with *system* fonts, and their white-pixel counts differed (89/71/73). That is another reason to outline before rendering.

**Recommendation: resvg-py.** It is self-contained (no system libraries), MIT, and fast (1.6–15 ms per size). The wrapper's licence (MIT, © 2024 baseplate-admin) was read in the wheel. The licence of the bundled resvg engine was **not checked** here.

### 5.2 Scoring, and a correction to mark-craft rule 15

`skimage.metrics.structural_similarity`, `scipy.ndimage.distance_transform_edt` and `skimage.morphology.skeletonize` were run on resvg renders:

| Ring | SSIM (16 px vs 256 px downsampled to 16) | Median stroke at 256 → at 16 px |
|---|---|---|
| thick (r 45/30) | 0.998 | 38.0 → 2.38 px |
| hairline (r 45/43) | **0.964** | 5.7 → **0.35 px** |

**SSIM between sizes stays high for a hairline that vanishes at 16 px**, because both images are equally faint. mark-craft rule 15's proposed "SSIM ≥ 0.8" gate would pass it. The absolute width check (rule 14: thinnest stroke ≥ 1 px at 16 px, via distance transform × 2 on the skeleton) is what catches it. **Keep SSIM for "same shape", and rely on width and contrast for "still visible".**

## 6. Typefaces: where to get them, and what the OFL asks

### 6.1 Sources tried (observed)

| Source | Result here | Reachable on claude.ai (network on)? | Notes |
|---|---|---|---|
| `raw.githubusercontent.com/google/fonts/main/ofl/<family>/` | 200: `Manrope[wght].ttf` (164 700 B), `OFL.txt`, `METADATA.pb` (`license: "OFL"`) | **Not on the approved list** ([support article](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude)) **(docs only)** | Full TTF/variable sources with licence beside each family. `github.com/.../raw/...` redirects here; github.com *is* listed, but whether the redirect target is allowed is **unverified** |
| Google Fonts CSS API `fonts.googleapis.com/css2?family=Manrope:wght@700` → `fonts.gstatic.com/s/…ttf` | 200, 96 188 B static TTF (curl's user agent got TTF) | Not listed **(docs only)** | Static instances only. `fonts.google.com` itself was blocked here |
| npm `@fontsource/<f>`, `@fontsource-variable/<f>` (`registry.npmjs.org`) | `npm pack` and plain `curl` of the tarball both worked. `license: "OFL-1.1"` for manrope, inter and fraunces (5.3.0) | **Listed** (registry.npmjs.org); also download-only on Cowork ([Cowork network](https://claude.com/docs/cowork/guide/network-access)) | **WOFF/WOFF2 only, split per Unicode subset** (`latin`, `latin-ext`, …). The variable package keeps the `wght` axis (200–800 for Manrope). Decompress with fontTools + brotli (§4) |
| System fonts (`fc-list`, 119 faces) | Inter + Inter Display (OFL-1.1 and Apache-2.0), JetBrains Mono (Debian says Apache-2), Liberation (OFL), Caladea/Carlito (OFL/Apache), DejaVu (Bitstream Vera), FreeFont (GPL-3+ with font exception) | Container-specific **(inference)** | Licences from `/usr/share/doc/fonts-*/copyright`. Only Inter and the Liberation/Crosextra families are serious brand candidates |
| PyPI font packages (`fonts`, `font-roboto 0.0.1`) | Downloadable, but tiny and stale | PyPI listed | Not a real catalogue |
| `canvas-design` skill's `canvas-fonts/` (~29 families, 27 OFL licences) | Per [claude-design-capabilities.md](claude-design-capabilities.md) | Wherever that skill is installed | A precedent for bundling OFL fonts inside a skill |

Artifacts may load typefaces from Google Fonts in the *page* (the CSP allows it) ([Claude Code artifacts, Page constraints](https://code.claude.com/docs/en/artifacts#page-constraints)) **(docs only)**. So the brand sheet can show live type even where the sandbox cannot download the font files.

### 6.2 What to bundle

A variable TTF is ~100–200 KB per family (Manrope 165 KB). A curated set of 15–25 OFL variable families, each with its `OFL.txt`, fits in a few MB **(inference)**. Skill bundles carry "no practical limit on bundled content" with respect to context ([Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)). A claude.ai *upload* size limit for skill zips was **not found**.

### 6.3 OFL obligations for outlined logos

- **Bundling with the skill is allowed.** "Original or Modified Versions of the Font Software may be bundled, redistributed and/or sold with any software, provided that each copy contains the above copyright notice and this license." Fonts must not be "sold by itself" (OFL 1.1 conditions 1–2, read in `ofl/manrope/OFL.txt` from google/fonts). **Ship each `OFL.txt` next to its font.**
- **The outlined logo is not under the OFL.** OFL-FAQ 1.13: "creating any kind of graphic using a font under OFL does not make the resulting artwork subject to the OFL", and the OFL requirement "does not apply to any document created using the fonts". Read in [OFL-FAQ 1.1-update2 (2010), mirrored by The League of Moveable Type](https://raw.githubusercontent.com/theleagueof/licenses/master/OFL-FAQ.md). The current FAQ (update7) at openfontlicense.org was **blocked here**. A search extract says current FAQ item 1.1 answers "Can I use the fonts for … logos…?" with "Yes. You are very welcome to do so" ([openfontlicense.org/ofl-faq](https://openfontlicense.org/ofl-faq/)) **(unverified: extract only)**.
- **Subsetting or converting the font file creates a Modified Version.** The FAQ says web-optimised versions "are Modified Versions and so must follow OFL requirements like appropriate renaming" (same 2010 copy). This applies only if the skill ships *font files* to the user, for example in the UI design system, not to outlined logo paths. Decompressing fontsource WOFF2 → TTF for internal use is not redistribution **(inference)**.
- **Reserved Font Names** apply only to modified *fonts*, not to artwork (same copy). Attribution in the brand book is a courtesy, not a requirement **(unverified for update7)**.

## 7. Seeing renders and showing them

| Channel | Surface | Status |
|---|---|---|
| **`Read` on PNG/JPEG/GIF/WebP** (the model sees pixels) | Claude Code (CLI, desktop, cloud) | **Verified here.** A Pillow contact sheet (16/32/48 px nearest-upscaled to 256, 256 px, reversed) was read and visibly showed the 16 px stair-stepping. `Read` on an `.svg` returns *text* (verified), matching the docs' image list ([tools reference](https://code.claude.com/docs/en/tools-reference)). **Always rasterise before self-critique.** Large images are downscaled before the model sees them (same page) |
| Model viewing images in the code-execution sandbox | claude.ai chat, Cowork, API | **Unverified.** No primary doc found describing how the model views a PNG it wrote in those sandboxes. The gate's script-only checks must stand on their own there |
| **Artifact** (HTML or Markdown page on claude.ai) | Claude Code CLI ≥ v2.1.281 / desktop; Pro, Max, Ultra, Team, Enterprise; Anthropic API provider only; not with CMEK/HIPAA/ZDR | **Docs only** ([artifacts, Availability](https://code.claude.com/docs/en/artifacts#availability)). The CSP blocks external images, so **images must be inline SVG or data URIs**. Google Fonts are allowed. Rendered size ≤ 16 MiB. The docs advise "Prefer SVG … over embedded raster images" (Page constraints) |
| Artifacts in claude.ai chat | Free → Enterprise; web, desktop; view on mobile | **Docs only**: "single-page websites, images, diagrams…" ([What are artifacts](https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them), via fetch summary) |
| **`SendUserFile`** | Claude Code with Remote Control or in a cloud session; not on Bedrock, Vertex or Foundry | **Docs only**: `display: render` opens inline, `attach` gives a download card ([tools reference](https://code.claude.com/docs/en/tools-reference)). Not called here, per instructions |
| Design System artifact type | claude.ai artifact access | See [claude-design-capabilities.md §1](claude-design-capabilities.md). It shows SVG through `<img>` |

## 8. Surfaces at a glance

| Surface | Network for installs | Python | What the skill can count on |
|---|---|---|---|
| **Claude Code** (local) | "Full network access" like any program; install locally, not globally ([Skills runtime constraints](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#runtime-environment-constraints)) **(docs only)** | the user's | A venv with the full stack (§2). The user's machine may lack libcairo, which is why resvg-py is preferred |
| **Claude Code cloud** (this container) | Proxy; PyPI, npm and apt reachable; many hosts blocked | 3.13 | **Observed**: everything in §1 |
| **claude.ai** (code execution) | Free/Pro/Max/Ultra: network on, "approved sources". Team: the article says both "disabled by default" (§Team plan) and "toggled on with access to package managers only" (§admin) **(disagreement)**. Enterprise: off by default. Approved: pypi.org, files.pythonhosted.org, registry.npmjs.org, github.com, archive.ubuntu.com, crates.io… ([support article](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude)) | **unverified** | Full stack if egress is on. Fallback (§3.4) if off. Custom skills need Pro or above with code execution on ([Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)) |
| **Cowork** | Egress off: only anthropic.com/claude.com. "Package managers only": registries + github.com, download-only. "All domains": any ([Cowork network](https://claude.com/docs/cowork/guide/network-access)) **(docs only)** | **unverified**; preinstalled packages not documented | Same split as claude.ai |
| **Claude API** (code execution / Skills API) | None; "no runtime package installation"; Python 3.11, 1 CPU, 5 GiB RAM ([code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)) **(docs only)** | 3.11 | Fallback only: matplotlib + fontTools (inference) + Pillow + scipy |

---

## 9. Implications for the skill (inference: my reasoning, not sourced)

- **Primitive library interface.**
  - Represent every shape internally as a `pathops.Path` (cubic, winding-normalised).
  - Export with fontTools `SVGPathPen`.
  - Measure with shapely, svgpathtools and numpy.
  - Construct in plain Python, with a construction log.
  - Make the boundary pen-based (`moveTo/lineTo/curveTo/closePath`). fontTools glyphs, pathops paths and the matplotlib fallback all speak it, so text, geometry and rendering compose with no format conversions.
  - Expose `union/difference/intersect/xor`, `stroke_to_outline` (with `convertConicsToQuads`), `remove_overlaps` (= `simplify`), `outline_text(font, text, axes, features, tracking)`, and `render(svg, sizes, mono=False, reversed=False)`.
- **Dependency tiers.**
  - *Tier A* (preferred): `skia-pathops fonttools uharfbuzz brotli resvg-py shapely svgpathtools numpy scipy scikit-image`, all wheels.
  - *Tier B* (offline): matplotlib, fontTools, Pillow and scipy, with SSIM in numpy, no booleans, and pre-wound contours.
  - The skill's first script should probe the tier and say which checks are degraded.
  - Do not depend on cairosvg, Inkscape, rsvg-convert or Playwright.
- **Fonts.**
  - Bundle a curated OFL set (variable TTF + `OFL.txt`) for the offline tier.
  - On demand, fetch `@fontsource-variable/<family>` tarballs from `registry.npmjs.org`, using plain HTTPS so npm isn't needed, then decompress the WOFF2.
  - Use google/fonts raw files only where the host is reachable.
  - Wordmarks are always outlined. Font files ship to the user only in the UI design system, with `OFL.txt`.
- **Gate.**
  - Pin resvg as the gate renderer and calibrate thresholds on it.
  - Outline all text before rendering.
  - Treat SSIM as a shape-identity check, never as a visibility check.
  - Rasterise to PNG for every model-visual check.
- **Delivery.** In Claude Code, present via an Artifact page with inline SVG, falling back to local files or `SendUserFile` in cloud sessions. On claude.ai, use chat artifacts or file downloads. The same inline-SVG HTML can serve both **(inference; untested)**.
- **New capabilities to create:**
  - the pen-based primitive library and construction log;
  - an `outline_text` script with HarfBuzz;
  - a render/contact-sheet script;
  - the measurement scripts from mark-craft §10;
  - a font fetcher and catalogue (family → npm package → licence);
  - a tier probe.

  Nothing on any surface provides these today.

## 10. Open disagreements and gaps

**Disagreements**
1. **Team plan network default.** The same support article says Team network access is "disabled by default" and also "toggled on with access to package managers only" ([support article](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude)). Treat it as unknown and probe at runtime.
2. **JetBrains Mono's licence.** Debian's copyright says Apache-2. Upstream is widely reported as OFL **(unverified)**. Irrelevant unless it is bundled.
3. **The SSIM gate in mark-craft rule 15** is contradicted by the observation in §5.2. It needs to be paired with an absolute-width check.

**Gaps**
- **Nothing was run inside claude.ai, Cowork or the API sandbox.** Python version, preinstalled packages, root/apt access and whether the model can *view* a PNG it wrote there are all unverified. **This is the first thing to test** once the skill exists: upload it, then run the tier probe and a `Read`/view of a PNG.
- Whether `github.com/<org>/<repo>/raw/…` redirects to the unlisted `raw.githubusercontent.com` and so fails on claude.ai is unverified.
- The licence of the resvg engine inside resvg-py, and of matplotlib (its PSF-style licence text was only partly read), were not confirmed from their files.
- The current OFL-FAQ (update7) was blocked. The 2010 text was used.
- No claude.ai upload size limit for custom-skill zips was found. That limit decides how many bundled fonts are feasible.
- Not run: svgpathtools `split(t)`, `ReverseContourPen`, asymmetric offsets, and the output of Inkscape's `path-union` action.
