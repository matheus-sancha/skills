# Calibrating the craft gate: lockup ratios, 16 px, optical centring and UI thresholds

**Question.** Measure published, known-good identities to calibrate the drawing gate's proposed defaults. That means the lockup's mark height, mark–word gap and stem-weight match (mark-craft rule 21, whose proposed defaults were not adopted in "Can a recipe over geometry primitives draw a convincing mark?"). It also covers the other thresholds the craft note marks as proposed: the favicon pass criterion, the optical-centring offset and the absolute-width check rule 15 needs. Finally, it checks the UI rules' contrast and scale thresholds against USWDS, Material and GOV.UK tokens. What ranges do the sources show, and what default should the rubric use for each?

**Method.** Unlike the earlier notes, most of this one is **measured, not read**. Every lockup, mark, favicon and icon below was downloaded from its owner's own site, brand portal or published package. It was rendered with resvg and measured with the two scripts in [`calibration/`](calibration/) (`lockup_measure.py`, `mark16.py`). Each lockup's mark/word split and its baseline and cap lines were checked by eye on [`calibration/lockup-segmentation.png`](calibration/lockup-segmentation.png). "Known-good" here means *an official production lockup from an established brand*. That is a calibration corpus, not a claim that every item is studio tier, and the note names no designers.

## Answer: defaults for the rubric

| Threshold | Old proposed default | Measured on known-good identities | **New default** | Gate |
|---|---|---|---|---|
| Lockup mark height | 1.0–2.0× cap height (prototype used 1.6× ascender) | 1.34–2.46× cap height across 10 brand systems, median **1.55**. One outlier: Pocket sizes its mark to the x-height (0.73× cap) | **1.5× cap height** | Flag outside **1.3–2.5× cap**. For an all-lowercase word with no ascenders, use x-height (Envoy: 3.1× x) |
| Mark–word gap | 0.5–1.0× mark width (prototype used 0.45) | **0.12–0.38× mark width**, median 0.27. Also 0.22–0.65× cap height, median **0.40** | **0.4× cap height** (≈ 0.27× mark width) | Flag a gap > 0.4× mark width or < 0.2× cap height. **Every measured lockup is tighter than the old range**, which explains why the prototype's gap looked too wide |
| Vertical alignment | not specified | 8 of 11 systems centre the mark on the cap band (centre within ±0.07 of cap height), so it overhangs equally above the cap line and below the baseline. Three anchor it instead: GOV.UK sits on the baseline, Pocket on the baseline at x-height, Python spans ascender to descender | **Centre on the cap band** | Model-visual. Anchoring to the baseline or to the ascender–descender span is allowed when declared |
| Stem-weight match | "stroke match" (no number) | Only 4 marks are line-drawn and comparable: mark line = **1.47–1.72×** the wordmark stem (Kubernetes, Envoy, Mozilla Monitor); GOV.UK's heraldic crown is 0.34× | **Mark line weight 1.0–1.75× the wordmark stem** | Info, plus a flag below 1.0×. **Weak evidence** (n = 4). Filled marks have no comparable stem |
| Clear space (rule 18) | ≥ 25 % of mark height | GitHub ≈ 0.17× mark height (measured from its `_Clearspace` files). Spotify 0.5× icon height. Shopify ½ S. Atlassian the capital "A" (≈ 0.65× mark height) | **0.5× mark height**, floor 0.17× | Script, as a named mark unit |
| Min stroke / gap at 16 px (rules 14–15) | ≥ 1 px | Only **5 of 16** known-good *master* marks pass 1 px for both stroke and gap. 10 of 16 pass at 0.75 px. Shipped 16 px favicons are mostly plain downsamples with closed gaps | **Keep ≥ 1 px** (the settled rule), applied **only to the master that ships at 16 px**: the small master if there is one, otherwise the main master. A main master that has a small master is not held to it (**decided by Matheus, 2026-11-20**) | Script. This bar is **stricter than industry practice**, which fits the studio-tier rule |
| SSIM 16 vs 256→16 (rule 15) | ≥ 0.8 as a gate | 0.72–0.999 on known-good masters. Pocket reads well but scores 0.72. Firefox is mush at 16 px but scores 0.82 | **Info only, never a gate** | Absolute width (row above) is the gate |
| Optical centring (rule 6) | flag an offset > 3 % of the container | Published play triangles are offset **3.1–6.2 %** of the container from bbox-centring. The shift goes from the bbox centre toward the area centroid, *t* = 0.30–0.82, median ≈ 0.76 | **t = 0.75** (three-quarters of the way from the bbox centre to the area centroid) | Flag *t* < 0 or *t* > 1. The old 3 % rule would fail every published play icon |
| Mark centroid vs bbox | flag > 3 % | 13 of 16 known-good marks are within 3 %. Firefox (5.6 %), Pocket (4.7 %) and Envoy (3.6 %) exceed it | **Info only** | The old rule would flag 3 known-good marks |
| UI text contrast (U1) | 4.5:1 / 3:1 large | GOV.UK's functional text and link pairs score **5.16–19.6:1**. The lowest are brand, error and link at 5.16–6.08. USWDS and Material encode the same WCAG 2 numbers | **Gate 4.5:1; solver target ≥ 5.0:1** | Script. The 5.0 target is my proposal, inferred from GOV.UK's headroom |
| Focus indicator (U11) | ring ≥ 3:1 on every surface | GOV.UK's focus yellow is **1.35:1 on white**. It works through the black text and underline paired with it (14.6:1 against the yellow) | **Use SC 2.4.13's own test:** ≥ 3:1 *between the same pixels focused vs unfocused*, over an area ≥ a 2 px perimeter | Script. Two-colour indicators pass |
| Type step ratio (U7) | 1.06–1.42 between adjacent steps | GOV.UK desktop steps 1.125–1.67 (80/48 display step). GOV.UK mobile has a **duplicate step** (24 and 27 both 21 px). The USWDS system palette has steps 1.06–1.50 | **1.06–1.42 for text steps ≤ 48 px; ≤ 1.7 for display steps** | Script. "Strictly increasing" holds per theme ramp, not per breakpoint |
| Spacing and line-height base (U7–U8) | everything on 4 px | GOV.UK runs on **5 px** (spacing 5…60, line heights 20/25/30/35/55). USWDS uses an 8 px unit with 4, 2 and 1 px half-steps. Material uses 4 px | **One declared base, 4 px by default** | Script checks values against the declared base, not against 4 specifically |

Gist: **lockups are tighter and their marks a little smaller than the old defaults assumed. The 16 px rule is stricter than what known-good brands ship. SSIM and the 3 % offset rules were miscalibrated and become info-only. The UI thresholds hold, with two fixes: focus is tested the WCAG way, and the base unit is declared rather than fixed at 4.**

## 1. Corpus

Lockups, one *system* counting once when computing the medians above:

| System | Lockups measured | Owner source |
|---|---|---|
| GitHub | GitHub, Copilot, GitHub Copilot (`*_Lockup_Black.svg`, `*_Clearspace.svg`) | [brand.github.com, Logo](https://brand.github.com/foundations/logo) → [GitHub_Logos.zip](https://brand.github.com/GitHub_Logos.zip) |
| Atlassian apps | Jira, Confluence, Trello, Loom (`*_logo_light.svg`) | [atlassian.design, Logos](https://atlassian.design/foundations/logos) (per-app zips) |
| Firefox / Mozilla products | Firefox Browser, Nightly, Developer, Relay, Monitor (`logo-word-hor.svg`) | [`@mozilla-protocol/core` 22.0.0](https://cdn.jsdelivr.net/npm/@mozilla-protocol/core@22.0.0/protocol/img/logos/) |
| Pocket | `pocket/logo-word-hor.svg` | same package |
| Spotify | `Full_Logo_Black_RGB.svg` | [Spotify design guidelines](https://developer.spotify.com/documentation/design) → `2024-spotify-full-logo.zip` |
| Shopify | monotone black logo | [Shopify brand assets](https://www.shopify.com/brand-assets) |
| GOV.UK | crown + logotype, assembled from the template's own SVG | [`govuk-frontend` 6.6.0 `macros/logo.njk`](https://cdn.jsdelivr.net/npm/govuk-frontend@6.6.0/dist/govuk/macros/logo.njk) |
| Python | `python-logo-generic.svg` (its `pt` units were stripped so it would render) | [python.org, Logos](https://www.python.org/community/logos/) |
| Kubernetes, Prometheus, Envoy | `*-horizontal-color.svg` | [cncf/artwork](https://github.com/cncf/artwork) |

Excluded after inspection: Node.js (the hexagon is built into the wordmark, so there is no mark/word split; [nodejs.org branding](https://nodejs.org/en/about/branding)). Mozilla (a wordmark only). Helm (its "horizontal" file is a square). Slack (the published nav file is the mark only). Docker (only a combined lockup was reachable).

## 2. Lockup measurements

The cap line is the 10th-percentile top of the word's letters, so for a lowercase word with ascenders it is the ascender line. The baseline is the median letter bottom. The gap is the widest empty column run between mark and word.

| Lockup | mark h / cap | mark h / x | gap / cap | gap / mark w | mark centre vs cap band (× cap) | mark line / word stem |
|---|---|---|---|---|---|---|
| GitHub | 1.34 | 1.37 | 0.27 | 0.19 | 0.00 | — (filled) |
| Copilot | 1.36 | 1.62 | 0.28 | 0.20 | −0.01 | — |
| GitHub Copilot | 1.35 | 1.45 | 0.27 | 0.19 | −0.01 | — |
| Jira | 1.54 | 2.05 | 0.40 | 0.26 | +0.05 | — (tile) |
| Confluence | 1.45 | 2.01 | 0.42 | 0.29 | +0.06 | — |
| Trello | 1.47 | 1.78 | 0.38 | 0.26 | +0.07 | — |
| Loom | 1.62 | 2.11 | 0.54 | 0.33 | +0.01 | — |
| Firefox Browser | 2.40 | 3.31 | 0.55 | 0.23 | +0.02 | — (filled) |
| Firefox Nightly | 2.46 | 3.27 | 0.56 | 0.23 | −0.01 | — |
| Firefox Developer | 2.46 | 3.29 | 0.56 | 0.23 | −0.01 | — |
| Firefox Relay | 2.37 | 3.39 | 0.73 | 0.34 | +0.03 | — |
| Mozilla Monitor | 2.51 | 3.37 | 0.63 | 0.27 | −0.02 | 1.72 |
| Pocket | **0.73** | 0.99 | 0.29 | 0.35 | +0.13 | — |
| Spotify | 1.86 | 2.63 | 0.38 | 0.21 | +0.02 | — (filled) |
| Shopify | 1.59 | 2.24 | 0.22 | 0.16 | −0.03 | — |
| GOV.UK | 1.34 | 1.36 | 0.46 | 0.32 | **−0.13** | **0.34** |
| Python | 1.34 | 1.94 | 0.39 | 0.28 | +0.14 | — (filled) |
| Kubernetes | 2.21 | 3.17 | 0.60 | 0.27 | +0.02 | 1.47 |
| Prometheus | 1.68 | 2.35 | 0.65 | 0.38 | −0.01 | — |
| Envoy | (x only) | 3.14 | 0.52 × x | 0.12 | −0.09 | 1.62 |

Taking the median within each system first, then across the 10 systems with a cap or ascender line: mark h / cap is 0.73, 1.34, 1.34, 1.35, 1.51, 1.59, 1.68, 1.86, 2.21, 2.46 (median 1.55). Gap / mark width across all 11 systems is 0.12–0.38 (median 0.27).

Readings:
- **Gap.** No measured lockup has a gap wider than 0.38× the mark's width. The old rule 21 range (0.5–1.0×) sits entirely outside practice. The prototype's 0.45× was wider than any lockup measured, which matches the verdict that "the gap was too wide" in the drawing ticket.
- **Height.** Most systems put the mark at 1.3–1.9× cap height. Very round or shield-like marks (Firefox, Kubernetes) go to 2.2–2.5×, so the overshooting form looks as heavy as the type. The prototype's 1.6× *ascender* is about 1.75× cap height. That is inside the range but in its upper half, and with a tall lowercase word it looks large. Default to 1.5× cap.
- **Family consistency.** Each system fixes its ratios across every product lockup: GitHub's three lockups are within ±0.01 of each other, Atlassian's four within ±0.1, Firefox's five within ±0.1. **The ratio is a system constant, and the spec should emit it as a named parameter of the logo system, not per lockup.**
- **Stem match.** The data is thin. Where a mark is drawn in lines, its line is heavier than the word's stem (1.5–1.7×), never lighter, except GOV.UK, whose crown is heraldic detail. Most marks are filled shapes, where "stem match" is not measurable. Treat the 1.0–1.75× band as a proposed default backed by four data points.

**Documented brand rules found along the way** (owner pages, read as text):
- Spotify: "The exclusion zone is equal to half the height of the icon". The logo must not be smaller than 70 px digital / 20 mm print, and the icon not smaller than 21 px / 6 mm ([Spotify design guidelines](https://developer.spotify.com/documentation/design)).
- Shopify: clear space of ½ S around the bag; do not scale the logo below 80 px or 28 mm wide ([Shopify brand assets](https://www.shopify.com/brand-assets)).
- Atlassian: the minimum clearance is the capital "A" of the Atlassian wordmark, and for app logos it comes from the wordmark's height and width ([atlassian.design, Logos](https://atlassian.design/foundations/logos)).
- GitHub: the `_Clearspace` SVGs add 16 units around a 95-unit-tall lockup (≈ 0.17× mark height), and 15–16 units around the 96-unit Invertocat ([GitHub_Logos.zip](https://brand.github.com/GitHub_Logos.zip), measured from the viewBoxes).
- **Minimum sizes are stated per artefact, in px and mm**, which confirms mark-craft rule 19. Spotify's *icon* minimum is 21 px, not 16.

No source states a mark-to-wordmark ratio in words. **The ratios above are measured, not documented**, and the spec should say so.

## 3. Sixteen pixels: masters, small masters and favicons

`mark16.py` fits each mark so its larger side is exactly 16 px, with no padding (the best case). It measures the minimum stroke and gap with the same morphological-opening method as the prototype's `checks.py`, and computes SSIM against a 256 → 16 downsample.

| Mark | min stroke @16 | min gap @16 | SSIM | centroid dx / dy (% of box) |
|---|---|---|---|---|
| GitHub Invertocat | 1.50 | 0.75 | 0.993 | +0.9 / −3.1 |
| Copilot | 1.00 | 2.00 | 0.996 | 0.0 / +1.4 |
| Jira | 0.25 | 1.50 | 0.985 | −0.8 / +0.3 |
| Confluence | 0.25 | 1.50 | 0.998 | 0.0 / 0.0 |
| Trello | 1.50 | 1.50 | 0.999 | +1.0 / +0.8 |
| Loom | 3.00 | 0.75 | 0.993 | −0.1 / −0.2 |
| Spotify | 1.25 | 0.75 | 0.939 | −0.1 / +0.6 |
| Firefox | 0.50 | 0.00 | 0.816 | +0.9 / +5.6 |
| Mozilla Monitor | 1.50 | 1.25 | 0.989 | −0.1 / −1.4 |
| Pocket | 3.00 | 1.50 | 0.720 | 0.0 / −4.7 |
| Kubernetes | 1.25 | 0.50 | 0.913 | 0.0 / +2.4 |
| Prometheus | 0.00 | 1.00 | 0.973 | +0.2 / −1.5 |
| Envoy | 0.75 | 0.25 | 0.958 | +0.6 / +3.6 |
| Helm | 0.75 | 0.75 | 0.987 | +0.1 / +0.1 |
| Node.js JS hexagon | 1.00 | 1.25 | 0.951 | +1.5 / +0.5 |
| Slack | 3.00 | 0.75 | 0.993 | 0.0 / 0.0 |

Sources: the marks come from the same owner downloads as §1, plus [`python-logo-only.svg`](https://www.python.org/community/logos/) (which failed to render and is omitted), the CNCF `icon/color` files, Spotify's `2024-spotify-logo-icon.zip`, Node's `jsIconGreen.svg` and Slack's nav logo ([slack.com media kit](https://slack.com/media-kit)).

- **Five of 16 known-good master marks clear 1 px for both stroke and gap at 16 px.** Ten of 16 clear 0.75 px. The common failure is a gap: the Octocat's tail, Spotify's bars, the Kubernetes wheel, the Envoy outlines.
- **Shipped favicons do not fix this.** The 16 px frames of the `favicon.ico` files served by github.com, open.spotify.com, mozilla.org (Firefox) and gov.uk are near-identical to their own larger frames downsampled (SSIM 0.92–0.99). Pixel crispness is the same, and by eye the Octocat's tail gap and Spotify's bar gaps are closed. Python's 16 px frame does differ (SSIM 0.73), but it looks blurred rather than hinted. *Method: frames extracted from each site's `/favicon.ico` with Pillow on 2026-11-20.*
- **So the settled 1 px-at-16 rule is stricter than what these brands ship.** That suits the studio-tier bar, and the small-master permission is what makes it achievable. **Decision (Matheus, 2026-11-20):** the 1 px stroke and gap gate at 16 px binds **only the master shipped at 16 px**: the small master when there is one, otherwise the main master. A main master that has a small master is not held to it. The 0.75 px figure is reported for information as "industry floor".
- **SSIM fails both ways on real marks.** Pocket reads cleanly at 16 px yet scores 0.72 (partly an artefact: its 16 × 15 fit resamples unevenly). Firefox is unreadable mush yet scores 0.82. This confirms the tooling note's hairline finding (`svg-tooling.md` §5.2) on real data. **SSIM is info only.** "Same shape" is judged by the visual review, and "still visible" by the absolute width check.
- **Centroid vs bbox.** Three well-known marks sit more than 3 % off (Firefox 5.6 %, Pocket 4.7 %, Envoy 3.6 %), all vertically and all deliberately (a flame, a pocket, a perspective stack). The rule-6 3 % flag would be noise on marks, so it stays info only.

## 4. Optical centring of asymmetric glyphs

Play triangles in their owners' published icon sets, rendered in the 24 or 32 unit container:

| Icon | bbox centre offset (% of container) | area centroid offset | *t* (0 = bbox-centred, 1 = centroid-centred) |
|---|---|---|---|
| Material Symbols `play_arrow` (filled, outlined) and classic Material Icons | +6.20 | −1.44 | **0.81** |
| Fluent `play_24_filled` / `_regular` | +5.99 | −2.50 | **0.71** |
| Carbon `play` / `play--filled--alt` (32) | +3.12 | −7.28 | **0.30** |
| Octicons `play-24` (triangle inside a circle) | +3.28 | −0.72 | **0.82** |
| Octicons `triangle-right-24` (disclosure caret) | −0.42 | −4.82 | −0.09 (uncorrected) |

Sources: [google/material-design-icons](https://github.com/google/material-design-icons) (`symbols/web/play_arrow/…`, `src/av/play_arrow/…`), [`@fluentui/svg-icons`](https://www.npmjs.com/package/@fluentui/svg-icons), [`@carbon/icons`](https://www.npmjs.com/package/@carbon/icons) and [`@primer/octicons`](https://www.npmjs.com/package/@primer/octicons), all fetched via jsDelivr or raw GitHub on 2026-11-20.

- Every play icon is shifted **away from bbox-centring toward the area centroid, and never past it**. Material and Octicons go about 80 % of the way, Fluent 70 %, Carbon 30 %. This is the first numeric evidence for rule 6. The craft note had found "no documented offset value". A measured one now exists, though no source states it in words.
- In container terms the shift is 3–6 % of the container. **The old "flag > 3 %" default would have failed all of them.** Express the rule in *t* instead: default 0.75, and flag *t* outside [0, 1].
- The caret is not corrected (*t* ≈ 0). Disclosure carets are aligned to text, not centred in a container, so the rule applies to glyphs centred in a container.

## 5. UI thresholds against USWDS, Material and GOV.UK

**Contrast (U1, U2).** All three systems encode WCAG 2 numbers rather than stricter ones:
- **USWDS.** "A magic number of 40+ results in WCAG 2.0 AA Large Text contrast". 50+ results in AA (or AAA large text), and 70+ in AAA. Grade-50 colours reach Section 508 AA against both pure white and pure black ([USWDS, Color overview](https://designsystem.digital.gov/design-tokens/color/overview/)).
- **Material.** "A difference of 40 in tone guarantees a WCAG contrast ratio ≥ 3.0; a difference of 50 in tone guarantees a contrast ratio ≥ 4.5" ([MCU, contrast_for_accessibility.md](https://github.com/material-foundation/material-color-utilities/blob/main/concepts/contrast_for_accessibility.md)).
- **GOV.UK.** Computed from the hex values in [`_colours-palette--internal.scss`](https://cdn.jsdelivr.net/npm/govuk-frontend@6.6.0/dist/govuk/settings/_colours-palette--internal.scss) and the role map in [`_colours-functional.scss`](https://cdn.jsdelivr.net/npm/govuk-frontend@6.6.0/dist/govuk/settings/_colours-functional.scss): text 19.6, secondary text 9.0, link 6.1, visited 9.1, error 5.2, success 5.4 and brand 5.2 on white. White on brand is 5.2, link on the tinted template background 5.7, and the decorative border (`black tint-80`) 1.57, which GOV.UK uses only decoratively. Input borders are full black.

So the U1/U2 thresholds stand. **GOV.UK's lowest text pair carries about 15 % headroom (5.16 vs 4.5).** I propose that the token solver aim for ≥ 5.0:1 and gate at 4.5:1. That target is my inference from GOV.UK, not a documented rule.

**Focus (U11).** GOV.UK's focus colour is `yellow` (#ffdd00) at `$govuk-focus-width: 3px` ([`_measurements.scss`](https://cdn.jsdelivr.net/npm/govuk-frontend@6.6.0/dist/govuk/settings/_measurements.scss); [`helpers/_focused.scss`](https://cdn.jsdelivr.net/npm/govuk-frontend@6.6.0/dist/govuk/helpers/_focused.scss)). That yellow is **1.35:1 against white**. It works because it pairs with black text and an underline at 14.6:1 against the yellow. USWDS uses a single solid ring: `$theme-focus-color: "blue-40v"`, `$theme-focus-width: 0.5` units ([`_settings-general.scss`](https://cdn.jsdelivr.net/npm/@uswds/uswds@3.14.0/packages/uswds-core/src/styles/settings/_settings-general.scss)). A "ring ≥ 3:1 on every surface" rule would therefore fail GOV.UK's indicator, which is well regarded. The normative test is SC 2.4.13's: an area at least as large as a 2 CSS px perimeter, with "a contrast ratio of at least 3:1 between the same pixels in the focused and unfocused states" ([WCAG 2.2, SC 2.4.13](https://github.com/w3c/wcag/blob/main/guidelines/sc/22/focus-appearance.html)). **U11 should render focused and unfocused states and diff the same pixels**, so that two-colour indicators pass.

**Type scale (U7).** Computed from each system's tokens:
- **GOV.UK** desktop ("tablet") sizes are 16, 19, 24, 27, 36, 48 and 80, giving steps of 1.125–1.67 (geometric mean 1.31). The mobile sizes are 16, 19, 21, 21, 27, 32 and 53: **24 and 27 collapse to 21 px**, a duplicate step ([`_typography-responsive.scss`](https://cdn.jsdelivr.net/npm/govuk-frontend@6.6.0/dist/govuk/settings/_typography-responsive.scss)).
- **USWDS** system sizes are 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 28, 32, 36, 40, 48, 56, 64, 80, 120 and 140, giving steps of 1.06–1.50 ([USWDS, Font tokens](https://designsystem.digital.gov/design-tokens/typesetting/font/)). This is a palette that themes pick from, not a role ramp.
- **Material** steps run 1.09–1.38 (already in `ui-design-system.md` §4).

The 1.42 upper bound fails only at the display end (GOV.UK 48 → 80). Keep 1.06–1.42 for text steps ≤ 48 px and allow up to 1.7 for display steps. "Strictly increasing" applies to one theme's ramp at one breakpoint. GOV.UK shows that a responsive ramp can merge steps on mobile, and the gate should allow that only when it is declared.

**Spacing and line height (U7, U8).** GOV.UK spacing is 0, 5, 10, 15, 20, 25, 30, 40, 50, 60 px ([`_spacing.scss`](https://cdn.jsdelivr.net/npm/govuk-frontend@6.6.0/dist/govuk/settings/_spacing.scss)), and its line heights are multiples of 5 (20, 25, 30, 35, 40, 50, 55). USWDS spacing units are multiples of 8 px with 4, 2 and 1 px half-steps ([USWDS, Spacing units](https://designsystem.digital.gov/design-tokens/spacing-units/)). **A 4 px base is a common default, not a law.** U8 should check against the *declared* base, defaulting to 4 px, so a 5 px or 8 px brand system can still pass.

## 6. What this changes in the earlier notes

- **mark-craft rule 21:** replace "no primary source / 1.0–2.0×, 0.5–1.0× mark width" with the measured ranges in §2. They are still not *documented* anywhere, so they carry the label "measured on N = 11 systems".
- **mark-craft rule 15:** SSIM is demoted to info. The pass criterion is the absolute stroke and gap check (rule 14) on the master rendered at 16 px.
- **mark-craft rule 6:** the 3 % flag is replaced by the *t*-interval rule for glyph centring. Mark centroid offset is info only.
- **mark-craft rule 18:** the default changes from 25 % to 0.5× mark height, with 0.17× as the floor seen in practice.
- **ui-design-system U7, U8, U11:** as in §5. U1 and U2 are unchanged, with a solver target of 5.0:1 added.

## Unverified and open

- **Corpus bias.** Eleven systems, mostly tech and open-source brands, all sans-serif wordmarks. No serif, script or all-caps-heavy lockup except GOV.UK. The ranges should widen if serif or script identities are added. **(open)**
- **Stem-weight match** rests on 4 line-drawn marks. **(weak)**
- **Pocket's SSIM of 0.72** is partly a fitting artefact (a 16 × 15 render). That does not change the conclusion that SSIM is unreliable, because Firefox shows the opposite error.
- **Favicon frames** were read from the sites' `/favicon.ico` on 2026-11-20. Sites may also serve PNG or SVG favicons through `<link rel=icon>`, which were not checked. The atlassian.com favicon is the Atlassian corporate mark, not Jira, so it was left out of the comparison.
- **Python's full lockup** declares its size in `pt`; it was measured after stripping the units, which does not change any ratio.
- **The 5.0:1 solver target** is my proposal, inferred from GOV.UK's headroom. No source sets it.
- **Which master the 1 px rule binds** is settled: only the master shipped at 16 px (Matheus, 2026-11-20, recorded on the rubric ticket). See §3.
