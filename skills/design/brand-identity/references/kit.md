# Stage 7: Kit

Assemble with `python scripts/run.py kit <slug>`, then check with `python scripts/run.py kit-check <slug>`.

## Contents

```
07-kit/
  README.md                  brand book (also the Design System README)
  rationale.md
  brand-sheet.html, brand-sheet.png
  logo/
    svg/<slug>-<layout>-<colourway>.svg    layouts: horizontal, stacked, mark, wordmark
                                          colourways: colour, black, white
    svg/<slug>-mark-small-<colourway>.svg  when a small master exists
    png/   same names at 512 and 1024 px
    favicon/  favicon.svg, favicon.ico (16/32/48), apple-touch-icon.png (180), icon-192.png, icon-512.png
  type/       fonts/*.woff2, OFL.txt, specimen.html
  graphic-language/  *.svg, params.json
  tokens/     tokens.dtcg.json (source), tokens.json (Claude Design System), tokens.css, brand_tokens.dart
  ui/         components/<Comp>/{preview.html, README.md}, bundle.js, bundle.css, index.d.ts, Cover/preview.html
  motion/     logo-sting.mp4, logo-sting/       optional (HyperFrames)
  exports.json                                  optional (Miro board / Figma file link)
  manifest.json   every file, sha256, gate status
```

Favicons come from the master that ships at 16 px.

## Brand sheet (one page, 8 parts)

1. Idea line.
2. Primary lockup + horizontal / stacked / mark in colour, black and white.
3. Clear-space diagram and minimum sizes.
4. 3–4 brand swatches (hex, RGB, OKLCH) with roles, the neutral ramp, approved text pairs with measured ratios, a proportion bar. "Screen values only" line.
5. Type specimen: wordmark lettering vs text family, 5–7 styles.
6. Graphic-language strip showing provenance (mark → part → pattern).
7. Two applications.
8. Three don'ts.

## Design System artifact

When the Artifact tool offers the Design System type: create it with the type's `type_url`, then write `tokens.json` (list shape: every family a list of `{name, value, usage}`; colour values per theme), `README.md`, components and fonts; upload `logo/svg/` files to `assets/Logos/` with **explicit inks** (no `currentColor`) and a group README; write the cover last; write `design-system.json` last of all. Follow the type's own instructions over this summary.

## Exports (optional)

Detect connectors with a probe call (Figma `whoami`, Miro `user_who_am_i`).
- Only one present → use it.
- Both → Miro for review and stakeholder walk-throughs, Figma for continued design or developer hand-off; if unclear, ask once.
- Neither → plain files and the Design System artifact; say how to connect either.

Miro gets a spec board (swatches, scales, SVG component previews, rules). Figma gets native variables and components via write-to-canvas (Pro plan or above, edit access). Exports are generated from the tokens and never edited back. Record links in `exports.json`.

## Motion (optional)

If HyperFrames (Node 22+, FFmpeg) is available, animate the master SVG into a 2–3 s logo sting using the motion tokens' easing; keep the HTML source in `motion/logo-sting/`. Otherwise skip and say so.

## Finish

The README carries the trademark notice (`gate.md`). Checkpoint: the user approves the brand sheet. Then set `stage: complete`.
