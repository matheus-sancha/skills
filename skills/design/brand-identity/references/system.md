# Stage 6: System (colour, type, graphic language, UI)

Everything here derives from the mark. One internal token model, `06-system/tokens.dtcg.json` (DTCG 2025.10), is the **single source**; every other format is generated from it and never edited back.

## 1. Colour

**Two layers.** Identity colours belong to the mark and stay **exact**. Role tokens are what UI and documents use.

Pipeline (`python scripts/run.py palette <slug>`):
1. Identity hues from the mark (user-supplied hexes are kept exactly).
2. Ramps per hue in OKLCH (11 steps, L 98 → 10), gamut-mapped by chroma reduction, plus a neutral ramp tinted toward the primary hue.
3. Roles assigned by measured contrast, Material-style: `primary`, `on-primary`, `primary-container`, `on-primary-container`, `surface`, `on-surface`, `on-surface-variant`, `outline`, `outline-variant`, `focus`, and status (`success`, `warning`, `danger`, `info`) from separate hues — light and dark themes.
4. The brand hex appears **exactly** in at least one fill role (fidelity placement). Text and link roles use contrast-safe siblings solved to **≥ 5.0:1**, gated at 4.5:1.
5. A user-supplied colour that fails is kept, flagged, and given a sibling — never silently altered.
6. Every token gets a `$description` (usage note) and a provenance entry.

Contrast is **WCAG 2.x** on the final hex. APCA may be reported, never gated.

**Print:** the kit is screen-only. No CMYK or Pantone. The brand sheet says: "Screen values only. Ask your printer to specify CMYK or a spot colour from these sRGB and OKLCH values." User-supplied print values are recorded verbatim as "user-supplied, not verified".

## 2. Type

- The route declares type as **derived** (shares features with the mark) or **neutral** (a supporting face).
- Choose from the bundled OFL set (`scripts/fonts/`) or any Google Fonts family: `run.py fonts-search --category Serif --variable`, then `run.py fonts-get <slug> "Family"` (fetches from the google/fonts repo, accepts only OFL, Apache 2 or UFL, saves the licence beside the files). Avoid overused faces (Inter, Roboto, Open Sans, Poppins, Montserrat). Without network, use the bundled set.
- Display face → expressive roles (`display`, `headline`); text face → `title`, `body`, `label`.
- Scale: ratio near 1.2; text steps 1.06–1.42 for ≤ 48 px, display steps ≤ 1.7; line heights on the declared base (4 px default).

## 3. Graphic language

Expose the mark's construction (radius set, grid, parts, colour-mix rule) as `params.json`, then generate with `python scripts/run.py graphic <slug>`:
- **shapes:** reuse the mark's constituent parts and corner radius;
- **parameters:** a seeded pattern bounded by the mark's ratios.

Sample, reject anything mistaken for the logo, keep 3–5 exemplars plus their rules. (Grid, device and principle moves are not built yet; do them by hand if a route needs one.)

## 4. UI design system

**Character knobs** — propose from the brief and the mark, confirm with the user on one specimen screen. This mapping is this skill's own method; no source gives one.

| Knob | Main input | Values |
|---|---|---|
| Radius factor | mark's corner treatment | sharp → 0 (0/2/4); small round → 1 (4/8/12); large round → 1.5 (8/12/16/24); pill/circle-led → buttons `full`. Classic↔Modern or Playful↔Serious may nudge one step. Checkbox never fully round. |
| Density | sliders, attribute words | Serious / Authority / "precise, technical" → compact 0.9; neutral → 1.0; "calm, generous, friendly" → comfortable 1.1. Never below target sizes (U10). |
| Motion family | Quiet↔Loud, Playful↔Serious | productive always for micro-interactions; expressive for page-level moments only when Playful or Loud |
| Depth | attribute words, mark | flat / editorial / technical → borders and layers; tactile / playful / friendly → soft shadows |

**Scales:** spacing 4 8 12 16 24 32 48 64 on the declared base; radius ≤ 7 steps plus `full`.

**Motion** lives in DTCG `duration` and `cubicBezier` tokens, emitted as `--motion-*` in `bundle.css` and a "Motion" section in the README (the Claude Design System `tokens.json` has no motion family). The logo sting uses the same easing.

**Components** (default six): Button, Input, Checkbox/Radio, Card, Navigation bar, Alert. React components in one `bundle.js`; one `preview.html` each showing rest, hover, focus, disabled and error, in both themes. The previews are the render surface for the UI gate.

## 5. UI gate (`python scripts/run.py ui-gate <slug>`)

| # | Rule | Check |
|---|---|---|
| U1 | Text roles ≥ 4.5:1 (3:1 for ≥ 24 px or bold ≥ 18.66 px) on named grounds, every theme | script |
| U2 | Control boundaries, focus and meaningful icons ≥ 3:1; decorative borders exempt | script |
| U3 | Brand hex exact in ≥ 1 fill role; `on-` token passes | script |
| U4 | Same role set in light and dark | script |
| U5 | Status distinguishable without hue and carries a word or icon | script + visual |
| U6 | Ramps monotone in tone, adjacent ΔL* ≥ 2 | script |
| U7 | Type steps increase; ratios as in §2; line heights on base | script |
| U8 | Spacing on one declared base; ≤ 12 steps | script |
| U9 | Radius ≤ 7 steps + full; one factor | script + visual |
| U10 | Targets ≥ 24×24 px (≥ 44–48 touch-first) | script |
| U11 | Focus: ≥ 3:1 between focused and unfocused pixels over ≥ 2 px perimeter (SC 2.4.13) | script |
| U12 | Every token has a usage note; names valid; aliases resolve | script |
| U13 | DTCG validates against 2025.10 | script |
| U14 | Brand fit: specimen beside the brand sheet — "same family?" | visual + user |
| U15 | No AI tropes (purple gradients, emoji decoration, left-border cards, overused fonts) | visual |
| CB | Status and data pairs stay distinguishable under protan, deutan and tritan simulation | script, **hard fail** |

**High-contrast AAA themes** (text ≥ 7:1, light and dark) only on request or when `accessibility_priority: true`; they get the same gate at AAA thresholds.

Checkpoint: the user approves palette, type and the knob settings (on the specimen).
