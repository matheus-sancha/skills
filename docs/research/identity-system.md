# Identity system: deriving colour, type and graphic language from one idea

**Question.** How do designers make the palette, typography, supporting shapes and patterns follow from the same concept as the mark, so that the identity reads as one system? This covers four things: how palettes are built and given roles, how typefaces are paired with a mark, how a graphic language is extracted from a logo, and what a minimal brand sheet contains. It cites well-documented identity systems as examples.

**Purpose.** Input to the spec for a Claude Agent Skill that designs brand identities and delivers an identity kit plus a UI design system derived from it. The binding decisions are the same as in [mark-craft.md](mark-craft.md): hybrid drawing, a render-then-rubric gate, and concept, craft and system researched to equal depth. Every rule below is therefore stated as a check: *script*, *model-visual* or *human*. This note does not repeat what earlier notes settle. The big idea and the routes are in [brief-to-concept.md](brief-to-concept.md). Construction, clear space and minimum size are in [mark-craft.md](mark-craft.md). The Design System artifact's file contract (`tokens.json`, README sections, `fonts/`, asset store) is in [claude-design-capabilities.md §3.1](claude-design-capabilities.md).

> **How these sources were read. Please read this first.**
> `www.w3.org`, `m3.material.io`, `design.google`, `about.google`, `mastercard.com`, `nasa.gov`, `gov.uk`, `england.nhs.uk`, `designsystem.digital.gov`, `carbondesignsystem.com`, `wolffolins.com`, `koto.studio`, `cghnyc.com`, `johnsonbanks.co.uk`, `typography.com`, `typotheque.com`, `fonts.google.com`, `openfontlicense.org`, `blog.mozilla.org` and the design press all failed to resolve or connect in this session.
> **Two routes worked:**
> - **`www.pentagram.com`.** It was blocked in earlier sessions but reachable now. Seven case studies were **read in full**: Mastercard, Slack, MIT Media Lab, Windows, The New School, Verizon and The Public Theater.
> - **`raw.githubusercontent.com`.** Through it I read the **source files** of the specs and design systems themselves:
>   - WCAG's own understanding documents and glossary ([w3c/wcag](https://github.com/w3c/wcag));
>   - the CSS Color 4 Editor's Draft ([w3c/csswg-drafts](https://github.com/w3c/csswg-drafts/blob/main/css-color-4/Overview.bs));
>   - Material Color Utilities and Material Components docs;
>   - USWDS, GOV.UK Design System, Carbon and Primer colour docs;
>   - the SIL OFL and its FAQ;
>   - Google Fonts metadata;
>   - IBM Plex, CNCF and Kubernetes brand READMEs;
>   - USWDS's colour token source.
>
> GitHub source is the text the published page is built from, so these count as full reads. Everything else was reached only through web-search extracts and is marked **(extract)**. A claim is marked **(unverified)** where even the extract was second-hand. **Numbers labelled "proposed default — not a documented standard" are mine.** I computed several numbers by running code. Those are marked **(computed)**, and the scripts are in the session scratchpad, not the repo.

---

## 1. Answer

**Conclusions first.**

- **The documented route is "one source, several extractions".** Pentagram states it outright for Mastercard: "The entire identity is built using the core elements found in the logo: geometry and color." The palette is built "from scales surrounding the red and yellow of the logo", and the patterns are "built parametrically around mathematical principles found in the mark" ([Pentagram, Mastercard](https://www.pentagram.com/work/mastercard/story)). Every system examined does a version of this: it extracts **colour, a geometry (shapes, grid or radius set), a typographic voice and one graphic device** from the mark or its idea, then applies each by rule (§2).
- **Colour has two separate layers, and the documented systems keep them separate.**
  - The **identity palette** is a few named brand colours tied to the mark. Its contrast is *exempt*: WCAG exempts logos and logotypes ([WCAG Understanding 1.4.3](https://github.com/w3c/wcag/blob/main/understanding/20/contrast-minimum.html)).
  - **Role tokens** are derived ramps assigned to jobs such as text, surface, action and status. They must pass WCAG 2.x: 4.5:1 for text, 3:1 for large text and UI.
  - Brand guidelines do *not* exempt ordinary text: "Beyond logos and logotypes, text that has insufficient contrast due to corporate identity or brand guidelines is not exempted" (same source).
  - The mechanism is the same everywhere: tonal ramps per hue, with roles mapped to steps. Material, USWDS, Carbon, Primer and GOV.UK all document it (§3).
- **Build ramps in OKLCH, but check contrast with the WCAG formula.** CSS Color 4 says HSL lightness "does not correspond to the visual perception of lightness" and that Oklab is "designed to be perceptually uniform" ([CSS Color 4 ED](https://github.com/w3c/csswg-drafts/blob/main/css-color-4/Overview.bs)).
  - **(computed)** At equal HSL lightness, contrast against white ranges from 1.07 to 8.59. At equal OKLCH L = 0.55 it ranges only from 4.54 to 5.27.
  - So OKLCH is a good build space but **not** a contrast guarantee. The L that gives 4.5:1 on white varies from 0.556 to 0.582 by hue.
  - **APCA is not a standard.** It is a beta whose own README targets "WCAG3" ([Myndex/apca-w3](https://github.com/Myndex/apca-w3)), and it is reported as removed from the WCAG 3 draft (**unverified**, §3.4).
- **Type pairs with a mark in one of two documented ways.**
  - **Derived**: the type shares the mark's construction. Examples are Mastercard's "rounded letterforms that each contain a portion of the circle", Google's Product Sans, Mozilla's Zilla Slab and The New School's Neue.
  - **Neutral support**: a plain grotesk lets the mark carry the character. Examples are Helvetica reinstated at the MIT Media Lab and Neue Haas Grotesk at Verizon.
  - No primary source gives a pairing *formula*. Font licence is checkable: the OFL FAQ explicitly allows logos (§4).
- **Graphic language is extracted from the mark, never invented beside it.** Five documented extraction moves:
  - **shapes**: Slack's "speech bubble and lozenge … can be extracted and used as graphic elements";
  - **grid**: MIT's 7×7 grid producing 23 group glyphs;
  - **parameters**: Mastercard's parametric circle patterns;
  - **a device**: the GOV.UK dot (**extract**);
  - **a principle**: Windows' perspective.

  Algorithmic generation is documented and works when it is constrained by the mark's parameters, as at Mastercard. The unconstrained 40,000-variant MIT 2011 logo was replaced after three years (§5).
- **The minimal brand sheet** is consistent across public guides. It holds the mark and its variants (layouts × colour versions), clear space and minimum size, colours with values and roles, type with roles, the graphic device, misuse ("don'ts") and the mark in application (§6).
- **Folklore:**
  - colour-psychology tables ("blue = trust"): no primary source in this reading treats them as a method. USWDS says colour effects are "personal and cultural as much as, or more so than, physiological" ([USWDS colour](https://github.com/uswds/uswds-site/blob/main/pages/design-tokens/color/overview.md));
  - "HSL lightness = perceived lightness": contradicted by CSS Color 4;
  - "APCA replaces WCAG 2": APCA is a beta;
  - pairing "rules" from blogs (serif + sans): secondary only.

### Rules table

| # | Rule (stated precisely) | Evidence | Status | Check type | How to check (measurement → threshold) |
|---|---|---|---|---|---|
| C1 | Every text-on-background pair the system defines has contrast ≥ 4.5:1; large text (≥ 18 pt, or 14 pt bold ≈ 24 px / 18.5 px bold) ≥ 3:1. Do not round | [WCAG 1.4.3 Understanding](https://github.com/w3c/wcag/blob/main/understanding/20/contrast-minimum.html) ("4.499:1 would not meet"); [contrast ratio](https://github.com/w3c/wcag/blob/main/guidelines/terms/20/contrast-ratio.html); [relative luminance](https://github.com/w3c/wcag/blob/main/guidelines/terms/20/relative-luminance.html); [large scale](https://github.com/w3c/wcag/blob/main/guidelines/terms/20/large-scale.html) | evidenced (standard) | script | WCAG formula on the **final quantised hex** in every theme. **(computed)** A solver that stops at exactly 4.50 can drop to 4.49 after rounding to hex (teal `#00848c`). So solve to ≥ 4.55 (proposed default — not a documented standard) and re-verify. |
| C2 | Non-text UI (control boundaries needed to find a control, state indicators, focus, meaningful icons) ≥ 3:1 against adjacent colours | [WCAG 1.4.11 Understanding](https://github.com/w3c/wcag/blob/main/understanding/21/non-text-contrast.html) | evidenced | script | Pairs listed in the role map: `border-control`, `focus`, `icon` vs `surface`*. |
| C3 | The logo is exempt from contrast, but brand colours used as text are not | WCAG 1.4.3 Understanding, "Logos" and "Beyond logos and logotypes…" (same link) | evidenced | script | If a brand hex fails C1 on its ground, the script forbids it in `text-*` roles and emits a darker derived role colour instead (§3.3). |
| C4 | Do not use colour as the only signal (status, links, data) | [WCAG 1.4.1 Understanding](https://github.com/w3c/wcag/blob/main/understanding/20/use-of-color.html); [USWDS colour](https://github.com/uswds/uswds-site/blob/main/pages/design-tokens/color/overview.md) | evidenced | script + model-visual | Status roles differ in OKLCH L by ≥ 0.10 (proposed default). A CVD simulation of the role swatches stays distinguishable, which the `dataviz` validator can measure ([claude-design-capabilities.md](claude-design-capabilities.md)). |
| C5 | Build tonal ramps in a perceptual space (OKLab/OKLCH), not HSL | [CSS Color 4](https://github.com/w3c/csswg-drafts/blob/main/css-color-4/Overview.bs) ("HSL… does not correspond to the visual perception of lightness"; Oklab "designed to be perceptually uniform") | evidenced (spec) | script | Ramp L is strictly monotonic. Adjacent steps differ by ΔEOK ≥ 0.04. The JND is 0.02 per CSS Color 4; 2× JND is a proposed default. |
| C6 | Every token is inside sRGB, gamut-mapped by reducing chroma at constant L and h in OKLCH | CSS Color 4 §Gamut mapping ("The gamut mapping color space is OkLCh"; JND = 0.02) | evidenced (spec) | script | After mapping, `0 ≤ r,g,b ≤ 1`. Report any token whose chroma was cut by more than 0.04 (proposed default) so a human sees the loss. |
| C7 | Palette has roles, not just swatches: a neutral base, one primary, few secondaries/accents, and functional (status) colours separate from brand colours | [USWDS theme tokens](https://github.com/uswds/uswds-site/blob/main/pages/design-tokens/color/theme-tokens.md); [GOV.UK colour](https://github.com/alphagov/govuk-design-system/blob/main/src/styles/colour/index.md); [Carbon](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/color/overview.mdx); [Primer](https://github.com/primer/design/blob/main/content/foundations/color/overview.mdx); [MDC Color](https://github.com/material-components/material-components-android/blob/master/docs/theming/Color.md) | evidenced | script | Every token has a `usage` field and belongs to exactly one role family. Brand hexes never appear in `status-*`. |
| C8 | Colour proportion is stated, with neutral dominant and accents rare | USWDS: primary/secondary/accent "60/30/10", base usually predominant; Carbon: neutral grey "dominant", other colours "sparingly"; Mastercard: warm greys "as the base for all compositions" | evidenced (3 systems) | model-visual | The brand sheet's sample layouts show the stated ratio. The model estimates area share on the render. 60/30/10 is USWDS's figure, not universal. |
| C9 | Brand palette is few colours, derived from the mark | Slack: "four primary colors, more manageable than the original's eleven" ([Pentagram, Slack](https://www.pentagram.com/work/slack/story)); Mastercard scales "surrounding the red and yellow of the logo", with orange as "a perfect midpoint" | evidenced (cases) | script + human | Every non-neutral hue is a mark hue, or a declared derivation of one (midpoint, complement, ±Δh) recorded in a provenance log. Proposed default: ≤ 4 brand hues plus neutrals. |
| C10 | Logo colours are calibrated against every approved ground | Mastercard: "hundreds of tests"; the mark had to work "on white backgrounds, black backgrounds, and different values in between" | evidenced (case) | model-visual + script | Render the mark on each ground in the sheet. Where mark-vs-ground contrast is < 3:1 (proposed default), the sheet must specify the mono or reversed variant for that ground. Note that **(computed)** Mastercard's reported yellow is 2.13:1 on white (hex **unverified**), so a hard 3:1 gate on full-colour marks would be wrong. |
| C11 | Each role resolves in light and dark themes | MDC Color (light and dark baselines per role); [Carbon](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/color/overview.mdx) (four themes; roles fixed, values vary); Primer (functional tokens "respect color modes") | evidenced | script | Run C1 and C2 per theme. |
| T1 | Type relates to the mark: either *derived* (shares construction) or *neutral support* | Derived: Mastercard, [Google](https://design.google/library/evolving-google-identity) **(extract)**, Mozilla **(extract)**, [New School](https://www.pentagram.com/work/the-new-school/story). Neutral: [MIT Media Lab](https://www.pentagram.com/work/mit-media-lab/story), [Verizon](https://www.pentagram.com/work/verizon/story) | evidenced (cases) | human (choose) + model-visual | The route's rationale names which relation it uses. If derived, the model lists the shared features (e.g. circular bowls, slab terminals, stroke contrast) visible in a side-by-side render. |
| T2 | Few families: one superfamily, or two contrasting families with clear jobs | IBM Plex: Sans, Serif, Mono and Condensed as one corporate family ([IBM/plex](https://github.com/IBM/plex)); H&Co "keep one thing consistent, vary one" ([typography.com newsletter](https://www.typography.com/email/2010_03/index.htm)) **(extract)** | practice-consensus | script | ≤ 2 families (proposed default). Each type style has a role. |
| T3 | Type roles form a scale (display, headline, title, body, label) | [MDC Typography](https://github.com/material-components/material-components-android/blob/master/docs/theming/Typography.md) (15 styles, Display Large 57 sp … Label Small 11 sp) | evidenced (one system) | script | The Design System contract caps groups and styles ([claude-design-capabilities.md](claude-design-capabilities.md)). Start with 5–7 styles. |
| T4 | The font licence permits logo use, and webfont bundling or subsetting is handled | OFL FAQ 1.1: logos allowed, "No additional license or permission is required"; FAQ 2.6: subsetting is modification, so Reserved Font Names may not be used ([OFL FAQ](https://github.com/silnrsi/font-charis/blob/master/OFL-FAQ.txt)); OFL conditions ([OFL.txt](https://github.com/google/fonts/blob/main/ofl/inter/OFL.txt)) | evidenced | script | Read `license:` from the family's Google Fonts `METADATA.pb` ([example](https://github.com/google/fonts/blob/main/ofl/inter/METADATA.pb)). Allow OFL or Apache only (proposed default). Ship `OFL.txt` with any font file. |
| G1 | Supporting graphics are extracted from the mark (shape, grid, parameter, device or principle) and their provenance is recorded | Slack, MIT, Mastercard, [Windows](https://www.pentagram.com/work/windows/story), New School (all Pentagram, read in full); GOV.UK dot **(extract)** | evidenced (cases) | script + model-visual | Script: every graphic element is built from the mark's primitives (same radius set, stroke and grid; see mark-craft rules 12–13), and the provenance log names its source. Model: "does this read as the same family as the mark?" |
| G2 | Generated variation stays recognisable as one family and does not compete with the mark | MIT 2011 (40,000 variants) replaced in 2014 ([The Next Web](https://thenextweb.com/news/mit-media-labs-new-logo-has-40000-variations) **(extract, design press)**; reasons **unverified**); Mastercard "infinite arrangements… all part of the same visual system" | practice-consensus | model-visual + human | Sample about 12 generated outputs. The model groups them blind with the mark. Proposed default: ≥ 10/12 judged "same system" and none mistaken for the logo. |
| B1 | The brand sheet carries mark variants, clear space, minimum size, palette with roles, type with roles, graphic device, don'ts and an application | §6 sources (CNCF, Kubernetes, GOV.UK, NHS, Mastercard/Pentagram) | evidenced | script | Checklist of sections present, plus files present per the matrix in §6. |

\* A role map is the list of foreground/background pairs the system intends to appear adjacent. WCAG asks for exactly that: "color pairs specified in the content that an author would expect to appear adjacent" ([contrast ratio](https://github.com/w3c/wcag/blob/main/guidelines/terms/20/contrast-ratio.html)).

---

## 2. One idea, several extractions: documented systems

All of the following are Pentagram's own case texts, **read in full** unless marked otherwise.

| System | The idea | Colour from it | Type from it | Graphic language from it |
|---|---|---|---|---|
| **Mastercard (2016)** ([story](https://www.pentagram.com/work/mastercard/story)) | Two interlocking circles: "connection", "inclusiveness" | The overlap uses an **additive** mix, "lighter than the red and darker than the yellow", to suggest translucency and "transparency". The palette is "scales surrounding the red and yellow"; warm greys are the base; orange, "a perfect midpoint", is the new primary | The wordmark plays "on the perfectly circular forms of the mark, with rounded letterforms that each contain a portion of the circle" | "Pure graphic shapes with parameters" generating "an infinite series of varied yet connected graphic patterns"; built "parametically around mathematical principles found in the mark". Custom icons, illustration and photo style complete it |
| **Slack (2019)** ([story](https://www.pentagram.com/work/slack/story)) | Keep the octothorpe's equity; communication | 11 colours reduced to 4 primaries "optimized to look better on screen". The original palette "suffered against any background color other than white". Aubergine kept as accent | (not stated) | The octothorpe, "built on a grid", is made of "two basic geometric shapes—a speech bubble and lozenge—that can be extracted and used as graphic elements". Icons and illustrations use "rounded corners that echo the shapes of the logo" |
| **MIT Media Lab (2014)** ([story](https://www.pentagram.com/work/mit-media-lab/story)) | A 7×7 grid taken from the previous (2011) logo | (not stated) | Helvetica "reinstated to support the overall system": neutral support | The same grid generates an ML monogram plus glyphs for "each of the 23 research groups": "an interrelated system of glyphs" |
| **Windows 8 (2012)** ([story](https://www.pentagram.com/work/windows/story)) | "Your name is Windows. Why are you a flag?": a window in perspective | Bold, flat colours per Metro (no gradients) | Metro / Swiss style (not specified further) | "A complete system based on the idea of perspective". The crossbar stays the same size at every height, so it "has to be redrawn for each time it increases in size, like classic typography" |
| **The New School (2015)** ([story](https://www.pentagram.com/work/the-new-school/story)) | Integrated, flexible, evolving curriculum | Black wordmark; school names in red; a commissioned Pantone ("Parsons Red") | The typeface *is* the identity: Neue, by Peter Biľak, has three widths "used together seemingly at random", placed by an algorithm | "A pair of parallel lines that echo the horizontal striations in the architecture" organise names at every scale |
| **Verizon (2015)** ([story](https://www.pentagram.com/work/verizon/story)) | Simplicity, reliability; a ✓ as "sign-off" | Red, "long a salient feature", kept as an **accent** in a brighter, cleaner hue | Custom letterforms dropped for Neue Haas Grotesk, fine-tuned by Christian Schwartz: neutral support | The checkmark |
| **The Public Theater (1994–2008)** ([story](https://www.pentagram.com/work/the-public-theater/story)) | "Street typography… almost graffiti-like" | Varies by season | Wood type, later Akzidenz Grotesk, later redrawn in Knockout | Typographic collision, later "angled printers rules" on a De Stijl-inspired 90° grid. **The graphic language is typographic**, not shape-based |
| **Google (2015)** ([design.google](https://design.google/library/evolving-google-identity)) **(extract)** | Simple, geometric | Four-colour logo palette | Product Sans, "a custom, geometric sans-serif typeface to complement the logo in product lockups" | Four dots in the logo colours (from secondary coverage only; the article's own text on the dots was not seen **(unverified)**) |
| **Mozilla (2017)** **(extract)** | "moz://a": the URL as wordmark | — | Johnson Banks chose a slab for the logo. Typotheque then drew Zilla Slab, with a Highlight variant and an "ill" → "://" ligature ([Mozilla Open Design](https://blog.mozilla.org/opendesign/zilla-slab-common-language-shared-font); [Typotheque](https://typotheque.com/blog/new-wordmark-and-typeface-for-mozilla)) | The text-selection "highlight" became a device. A later 2024 rebrand is reported **(unverified)** |
| **GOV.UK (2025)** **(extract)** | The dot in the wordmark | "4 tiers: primary, tints, shades and accents", with blue as the anchor; combinations failing WCAG 2.2 "are not allowed" ([GOV.UK brand guidelines](https://www.gov.uk/government/publications/govuk-brand-guidelines)) | (not confirmed) | The dot is "used within our wordmark and as a graphic device across all GOV.UK channels" (same source) |

**What generalises.**
1. Colour, type and graphic language are each **argued from the mark or the idea in one sentence**. Examples: Mastercard's additive overlap because of "transparency"; Windows' perspective because "Windows"; Slack's rounded corners because of the speech bubble.
2. The extraction is **literal**: the *same* shapes, grid or parameters are reused. A mood is not reused.
3. **Neutral support is a legitimate choice**: Helvetica at MIT, Neue Haas at Verizon. Not every element must be bespoke.
4. One element usually carries the identity's personality, and the others are deliberately quiet: type at The New School and The Public; shapes at Slack; colour plus geometry at Mastercard. The last point is my synthesis, not a quoted principle.

---

## 3. Palette: how it is built, given roles and checked

### 3.1 Two layers: identity colours and role tokens

- **Identity colours** belong to the mark and are tuned visually. Mastercard's three needed "hundreds of tests" to work on white, black and mid-tones, and to keep "sufficient contrast from the orange in between" ([Pentagram](https://www.pentagram.com/work/mastercard/story)). **(computed)** Third-party hex values for those colours (**unverified** as official) give red/orange 1.51:1 and orange/yellow 1.43:1, and yellow on white 2.13:1. Mark colours are *not* tuned to WCAG text thresholds, which is consistent with the logo exemption.
- **Role tokens** are what UI and documents use. Every system read here separates three things:
  - **raw values**, called "System tokens" (USWDS), "Base" tokens (Primer) or the tonal palette (Material);
  - **roles**: USWDS theme tokens `base / primary / secondary / accent-warm / accent-cool`; Primer "Functional" tokens; Carbon tokens where "Roles cannot be changed between themes"; Material `primary / onPrimary / primaryContainer / onPrimaryContainer / surface…`;
  - **themes** that assign values to roles.

  Sources: [USWDS theme tokens](https://github.com/uswds/uswds-site/blob/main/pages/design-tokens/color/theme-tokens.md); [Primer](https://github.com/primer/design/blob/main/content/foundations/color/overview.mdx) ("Base color tokens… should never be used directly"); [Carbon](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/color/overview.mdx); [MDC Color](https://github.com/material-components/material-components-android/blob/master/docs/theming/Color.md).
- **Functional colours are separate from brand colours.** GOV.UK: use `govuk-functional-colour("brand")` rather than copying `#1d70b8`, and use the palette colour, not `functional-colour("error")`, when you just want red ([GOV.UK colour](https://github.com/alphagov/govuk-design-system/blob/main/src/styles/colour/index.md)). Primer ties semantic colours (accent, success, danger, warning, done, sponsors) to roles, each with `muted` and `emphasis` variants.

### 3.2 Building ramps

- **Graded ramps per hue are the common mechanism.**
  - USWDS: every family has grades 5–90. "a color of grade 50 in one color family should be the same level of lightness as a color of grade 50 in another".
  - Material: tones 0–100, where "Tone is equivalent to L* in the L*a*b* color space" ([MCU contrast.ts](https://github.com/material-foundation/material-color-utilities/blob/main/typescript/contrast/contrast.ts)).
  - GOV.UK: tints at 25/50/80/95 % plus shades.
  - Carbon: Gray 10 … Gray 100.
- **Grades are tied to luminance so contrast follows from arithmetic.** USWDS's "magic number" is a difference in grade. 40+ gives AA large text, 50+ gives AA, 70+ gives AAA, and grade 50 passes against both white and black ([USWDS colour](https://github.com/uswds/uswds-site/blob/main/pages/design-tokens/color/overview.md)). Material maps roles to tones: light `primary40` on white, `primaryContainer90` with `onPrimaryContainer10`; dark `primary80` with `onPrimary20` ([MDC Color](https://github.com/material-components/material-components-android/blob/master/docs/theming/Color.md)).
- **What I checked by running code (computed):**
  - **USWDS claims hold on the real tokens.** All 463 system tokens were parsed from [USWDS source](https://github.com/uswds/uswds/tree/develop/packages/uswds-core/src/styles/tokens/color). Every pair with grade gap ≥ 40, ≥ 50 or ≥ 70 meets 3:1, 4.5:1 and 7:1 respectively: 0 failures in 41,476 / 28,551 / 9,328 pairs. **But the published luminance-range table alone does not guarantee it.** Its bounds allow grade 40 vs grade 90 at 4.23:1. The actual tokens sit tighter than the table, so a generator must check real values, not bounds.
  - **Material tone gaps.** Over all tone pairs, the minimum WCAG ratio is 3.17 for a gap of 40, **4.48** for 50, 6.46 for 60 and 9.15 for 70. A gap of 50 is therefore *just under* 4.5:1 at the worst point. The role pairs Material actually ships are well clear: 40/100 = 6.46, 90/10 = 13.27, 80/20 = 7.72.
  - **OKLCH vs HSL.** CSS Color 4's own example (blue and yellow both at HSL L = 50 %, but at OKLCH L 0.452 and 0.968) was reproduced. Across 12 hues at HSL L = 50 %, contrast with white spans 1.07–8.59. At OKLCH L = 0.55 it spans 4.54–5.27, and at L = 0.60 it spans 3.70–4.28. The OKLCH L that reaches 4.5:1 on white ranges from 0.556 (green) to 0.582 (red) at C = 0.12.
  - **A ramp built evenly in OKLCH** at hue 250 (L 0.97 → 0.25) crosses 4.5:1 on white between the L 0.62 and L 0.54 steps. So the "500/600" boundary is where text-capable steps begin. That is a property of this ramp, not a rule.
- **Keeping a brand colour exact while deriving roles is documented.** Material's Fidelity and Content schemes place "the source color in `Scheme.primaryContainer`… adjusted for color relativity", at about ±5 tone between light and dark ([scheme_fidelity.ts](https://github.com/material-foundation/material-color-utilities/blob/main/typescript/scheme/scheme_fidelity.ts)). Default one-seed schemes regenerate tones and do not keep the hex; [claude-design-capabilities.md](claude-design-capabilities.md) found the same for Flutter's `fromSeed`. USWDS adds that its palette is "not generated by an algorithm… we are trying to find good colors, not just those that fit a function". That is an explicit vote for hand-tuning *after* generation.

### 3.3 Deriving accessible roles from a brand colour (computed demonstration)

For sample brand hues, I darkened at constant OKLCH C and h until the colour reached 4.5:1 on white:

| Brand hex (sample) | Contrast vs white / black | Best "on" colour | Text-on-white role |
|---|---|---|---|
| `#F2A900` (amber) | 2.01 / 10.45 | black | `#9f6d00` (L 0.785 → 0.572) |
| `#E4002B` (red) | 4.85 / 4.33 | white | brand hex usable as is |
| `#00A3AD` (teal) | 3.07 / 6.84 | black | `#00848c`, which came out at **4.49 after hex rounding**, so it needs a margin (rule C1) |
| `#5B2C83` (violet) | 9.85 / 2.13 | white | brand hex usable as is |

Light brand colours (amber, yellow, teal) need a separate, darker text role, and they take *dark* "on" text. That is the concrete form of rule C3.

### 3.4 Contrast standard: WCAG 2.x, not APCA

- **WCAG 2.2 is the current requirement** that GOV.UK cites ([GOV.UK colour](https://github.com/alphagov/govuk-design-system/blob/main/src/styles/colour/index.md)). The thresholds in C1 and C2 come from WCAG's own documents. Its rationale: 3:1 is the ISO-9241-3 / ANSI-HFES minimum, and 4.5:1 compensates for 20/40 acuity ([WCAG 1.4.3 Understanding](https://github.com/w3c/wcag/blob/main/understanding/20/contrast-minimum.html)).
- **APCA** is a "beta" contrast method "developed as an assessment method for W3 Silver/WCAG3". Its constants are "fixed at 0.0.98G-4g", and it is licensed to W3C/AGWG with "specific limitations" ([Myndex/apca-w3 README](https://github.com/Myndex/apca-w3)). Secondary reporting says APCA was pulled from the July 2023 WCAG 3 Working Draft and that the current draft says the contrast algorithm is "yet to be determined" ([Roselli, April 2026](https://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html)) **(unverified: the W3C draft could not be fetched)**. **Use for the skill:** gate on WCAG 2.x. APCA Lc may be *reported* as advisory; the `dataviz` validator already exports `apca()`.
- **WCAG's own caveat:** thin or unusual fonts render fainter than their CSS colour, and authors "are encouraged to choose a font with stronger/thicker lines, or… exceed the normative requirements" (same source). This argues for a stricter margin on light-weight display faces. Model-visual on the render.

### 3.5 Proportion and restraint

- USWDS: primary/secondary/accent at "about 60%… 30%… 10%" of non-base colour, with the neutral base often predominant ([theme tokens](https://github.com/uswds/uswds-site/blob/main/pages/design-tokens/color/theme-tokens.md)).
- Carbon: neutral grey "dominant", blue the "primary action color", others "sparingly and purposefully".
- NHS: NHS Blue and white "dominant", with four supporting groups whose tints "decrease in emphasis" ([NHS colours](https://england.nhs.uk/nhsidentity/identity-guidelines/colours)) **(extract)**.
- USWDS: "Start in black and white" and "put the practical before the emotional". This is the palette-level echo of Geismar's black-and-white-first test in [mark-craft.md rule 17](mark-craft.md).

---

## 4. Typography: pairing with the mark, and sourcing

### 4.1 How type relates to the mark

- **Derived type.** It shares the mark's geometry or idea.
  - Mastercard: the circle inside each letter.
  - Google: "a custom, geometric sans-serif… to complement the logo" ([design.google](https://design.google/library/evolving-google-identity)) **(extract)**.
  - Mozilla: Zilla Slab continues the logo's slab **(extract)**.
  - The New School: the variable-width face *is* the system.
  - Bespoke type is expensive. The documented cases are all large clients, and an agent can only *select* type, not draw a family (inference).
- **Neutral support.** It lets the mark carry the character: MIT's Helvetica, Verizon's Neue Haas Grotesk, IBM Plex as the family for all text. Plex's README says it "has been designed to work well in user interface (UI) environments" ([IBM/plex](https://github.com/IBM/plex)).
- **The wordmark is not the text face.** Mastercard drew a custom wordmark, and Verizon fine-tuned its wordmark (Christian Schwartz) while setting text in the retail face. So the kit needs **two type decisions**: wordmark lettering (outlined, spaced per mark-craft rule 20) and a text system.
- **Pairing technique.** The only foundry source seen is H&Co's 2010 newsletter: keep one element consistent and let one vary, with the display face used "only occasionally, and always in large sizes" ([typography.com](https://www.typography.com/email/2010_03/index.htm)) **(extract)**. "Superfamily" pairing (Sans/Serif/Mono of one family) appears in Typekit's blog ([Typekit, Type Study](https://blog.typekit.com/2012/05/23/type-study-pairing-typefaces/)) **(secondary)** and is embodied in Plex. No primary source gives measurable pairing criteria. Candidate measurable proxies (x-height ratio, stroke contrast, aperture) are **my proposal, not documented**.

### 4.2 Sourcing and licences

- **The OFL permits logos.** FAQ 1.1: you may use OFL fonts "to create logos or other graphics… No additional license or permission is required". FAQ 1.1.1: "You remain the author and copyright holder of that newly derived graphic". FAQ 1.13: the OFL does not apply to documents or artwork made with the font ([OFL FAQ, SIL, 1.1-update7](https://github.com/silnrsi/font-charis/blob/master/OFL-FAQ.txt); canonical at openfontlicense.org, not reached).
- **Bundling fonts** with the kit is allowed if each copy carries the copyright notice and the licence. Fonts may not be "sold by itself" ([OFL.txt](https://github.com/google/fonts/blob/main/ofl/inter/OFL.txt)).
- **Subsetting a webfont "is considered modification"** (FAQ 2.6). Under condition 3 a modified font may not use a Reserved Font Name. A subset fonts/ file for the UI system must therefore be renamed if the family declares an RFN, or be shipped unsubset.
- **Machine-readable licence.** Every Google Fonts family directory carries `METADATA.pb` with a `license:` field ("OFL" for Inter) and the licence file, organised under `ofl/`, `apache/` and `ufl/` ([google/fonts, Inter](https://github.com/google/fonts/blob/main/ofl/inter/METADATA.pb)). This is the scriptable sourcing route. [claude-design-capabilities.md](claude-design-capabilities.md) found a ~1,700-family Google Fonts list and an RFN list already shipped with the Design type.
- **Commercial fonts** (Frutiger at the NHS, Akzidenz, Knockout, Neue Haas) need a purchased licence. The NHS documents Arial as the fallback where Frutiger is unavailable ([NHS fonts](https://england.nhs.uk/nhsidentity/identity-guidelines/fonts)) **(extract)**. An agent cannot verify a commercial licence, so this is human.
- **Gap.** A wordmark set in a free font is not exclusive: anyone can set the same word in the same font. No primary source on trademark strength was read. This is an inference to flag to the user, not a finding.

---

## 5. Graphic language: extraction methods, hand vs algorithm

**Five documented extraction moves** (§2 for sources):

| Move | Example | What the agent extracts | Primitive needed |
|---|---|---|---|
| **Shapes** | Slack: speech bubble + lozenge; rounded corners in icons | The mark's constituent closed shapes and its corner radius | Boolean decomposition of the mark into parts; reuse of its radius set |
| **Grid** | MIT: 7×7 grid → monogram + 23 group glyphs | The construction grid (mark-craft rule 12) | A grid object shared by mark and glyph generator |
| **Parameters** | Mastercard: circles, overlap rule (additive), parametric patterns | Shape type + ratios + colour-mix rule | Parametric pattern generator, seeded and bounded by the mark's ratios |
| **Device** | GOV.UK dot **(extract)**; New School parallel bars; Verizon ✓ | One small, repeatable element | Single-element symbol with usage rules (placement, scale relative to type) |
| **Principle** | Windows: perspective; The Public: typographic collision | A rule of composition, not a shape | Layout rules (angle set, grid), with a model-visual check |

**Hand-composed or algorithmic?** Both are documented.

- **Algorithmic, constrained.** Mastercard: "Coupled with the power of computing, the parametric design generates infinite arrangements, each different from the next, though all part of the same visual system." New School: "An algorithm has been created to facilitate the use of the three widths".
- **Algorithmic, unconstrained, then replaced.** The 2011 MIT Media Lab identity by TheGreenEyl and E Roon Kang let each person generate a logo from three spotlights in "40,000 shapes and 12 color combinations" ([The Next Web](https://thenextweb.com/news/mit-media-labs-new-logo-has-40000-variations)) **(extract, design press)**. Pentagram's 2014 replacement kept the *grid* and dropped the free variation. Press accounts that it failed to introduce the 23 groups, and that "they all looked pretty much the same", are **unverified** (Gizmodo extract).
- **Generative kit.** Sagmeister's Casa da Música shipped a digital kit and an auxiliary colour-picker application ([Sagmeister](https://sagmeister.com/work/casa-da-musica/); [Cooper Hewitt](https://collection.cooperhewitt.org/objects/18794271/)) **(extract; mechanism unverified)**.
- **Hand-drawn per size.** The Windows crossbar is "redrawn for each time it increases in size, like classic typography".

**Reading.** Algorithms appear where the system must make *many* outputs (patterns, names, group glyphs). The constraint that keeps them on-brand is the mark's own parameters. That matches the hybrid-drawing decision: scripts expose the mark's parameters as a generator, and the agent composes and selects (inference).

---

## 6. What a minimal brand sheet and kit contain

**Asset matrix (documented).** CNCF ships every project logo in "2 formats (PNG & SVG), 3 layouts -- horizontal…, stacked…, and icon…, and at least 3 versions (color/black/white). So, that's at least 18 versions" ([cncf/artwork](https://github.com/cncf/artwork)). Kubernetes uses the same layouts with 5 colourways: colour, black, white, all-blue and white-text ([Kubernetes usage guidelines](https://github.com/kubernetes/kubernetes/blob/master/logo/usage_guidelines.md)). Together with mark-craft's small-size and mono rules, this is the file contract for the logo half.

**Sheet sections across published guides:**

| Section | Sources that include it |
|---|---|
| Concept / one-line idea | Pentagram case texts all lead with it; Wolff Olins "creative north star" ([brief-to-concept.md](brief-to-concept.md)) |
| Mark + lockups + colour versions | CNCF; Kubernetes; NHS logo page ([NHS logo](https://www.england.nhs.uk/nhsidentity/identity-guidelines/nhs-logo/)) **(extract)** |
| Clear space, minimum size | [mark-craft.md rules 18–19](mark-craft.md); NHS exclusion zone "the full height of the NHS logo" **(extract)** |
| Approved grounds / reversing rules | NHS: the logo "cannot be reversed out of any colour other than NHS Blue" **(extract)**; Mastercard calibration across grounds |
| Colour: values, roles, approved pairs, proportion | GOV.UK (tiers; WCAG-failing combinations "not allowed") **(extract)**; USWDS; NHS |
| Typography: families, roles, fallback | NHS (Frutiger, Arial fallback) **(extract)**; Material type roles |
| Graphic device / language with rules | GOV.UK dot **(extract)**; NHS "visual styles, graphic devices" page ([NHS](https://www.england.nhs.uk/nhsidentity/identity-guidelines/visual-styles-graphic-devices-and-straplines/)) **(extract)**; Mastercard "graphic tools" |
| Iconography, illustration, photography style | Mastercard: "custom icon sets, illustrations and photographic styles" |
| Misuse ("don'ts") | Kubernetes cites the Linux Foundation's "correct and incorrect usage examples" |
| Applications | Wheeler "trial applications" and Haviv's in-context presentation ([brief-to-concept.md §4](brief-to-concept.md)) |

**Minimal one-page sheet (proposed, derived from the table):**
1. idea line;
2. primary mark + horizontal/stacked/icon in colour, black and white;
3. clear-space diagram + minimum sizes;
4. 3–4 brand swatches with hex/RGB plus OKLCH, and their roles, followed by the neutral ramp, approved text pairs with measured ratios, and a proportion bar;
5. type specimen showing the wordmark lettering vs text family, with 5–7 styles;
6. graphic-device strip showing extraction provenance (mark → part → pattern);
7. two applications;
8. three don'ts.

CMYK/Pantone values appear in print-era guides (the New School's commissioned Pantone). An agent cannot produce reliable print conversions without a target profile, so this is human, or flagged as screen-only (inference).

---

## 7. Implications for the skill (inference: my reasoning, not sourced)

- **Colour pipeline (script):**
  1. Take the mark's colours (identity layer; exempt).
  2. Convert to OKLCH.
  3. Build one ramp per brand hue plus a neutral ramp (optionally tinted toward the primary hue, as Mastercard's warm greys are), with an 11-step L ladder.
  4. Gamut-map by chroma reduction (CSS Color 4).
  5. Snap to hex.
  6. Measure WCAG on the snapped hex.
  7. Assign roles by measured contrast, not by step name: text, surface, action, on-action, container, border, focus, and status from separate hues.
  8. Emit the light and dark themes.
  9. Write a provenance log (each token → source hue + derivation).

  Every step is deterministic. The only taste call is *which* brand hues and the chroma level, which the route proposes and the human approves.
- **Palette rubric (model-visual):**
  - Does the palette feel like the mark, and does the neutral carry the right temperature?
  - Is the accent rare enough?
  - Do the mark colours hold on each approved ground (C10)?
- **Type pipeline:**
  - The route declares *derived* or *neutral*.
  - Candidate families come from the Google Fonts list, filtered by `METADATA.pb` licence (script).
  - The model compares the specimen against the mark render and names the shared features.
  - The human approves.
  - Wordmark lettering is always outlined and spaced per mark-craft rule 20. The OFL allows this.
- **Graphic-language generator (hybrid):**
  - Expose the mark's construction (radius set, grid, parts, colour-mix rule) as a parameter object.
  - Generators for each of the five moves read only from it.
  - The agent samples, rejects anything mistaken for the logo, and keeps 3–5 exemplars plus the rules.
  - Record provenance so the rationale is truthful (mark-craft §2).
- **Kit contract:**
  - Logo matrix: 3 layouts × 3+ colourways × SVG/PNG, plus small-size variant and favicon set.
  - `palette.json`: identity + ramps + roles + themes + measured pairs.
  - Type: families, licence files, styles.
  - Graphic-language SVGs + generator parameters.
  - Brand sheet: one page (§6).
  - These map onto the Design System contract in [claude-design-capabilities.md §3.1](claude-design-capabilities.md).
- **Human only:** final hue choice; commercial-font licensing; print colour (CMYK/Pantone); whether a free-font wordmark is distinctive enough for the client's trademark needs.

---

## 8. Open disagreements and gaps

**Disagreements**
1. **Generated vs tuned palettes.** Material generates roles algorithmically from one seed (MCU README: schemes "from a single color"). USWDS says its palette is deliberately "not generated by an algorithm". A middle path is documented: Material's Fidelity scheme keeps the source colour.
2. **The USWDS table vs the USWDS tokens.** The published luminance bounds allow a 4.23:1 pair at "magic number 50". The shipped tokens never fail **(computed)**. Trust the tokens, and check values, not bounds.
3. **Material tone gap 50 ≈ 4.5:1** holds only approximately (worst case 4.48 **(computed)**). Claims that "tone difference 50 guarantees 4.5:1" were not found in a primary source here, and they would be slightly wrong at the margin.
4. **Free variation vs fixed identity.** MIT 2011 (40,000 variants) vs MIT 2014 (one grid, fixed glyphs). Mastercard shows the constrained middle.
5. **WCAG 2 vs APCA.** WCAG 2.x is the normative requirement. APCA claims better perceptual accuracy but is beta and not in the current WCAG 3 draft **(unverified)**.
6. **Logo colours vs contrast.** WCAG exempts logos. A rubric that hard-gates full-colour marks at 3:1 on white would reject Mastercard's yellow **(computed, hex unverified)**. Gate the mono variant instead.

**Gaps**
- **Not reached:**
  - the W3C-hosted WCAG 3 draft;
  - m3.material.io colour-role pages (read via MDC and MCU source instead);
  - Mastercard Brand Center palette and proportions;
  - Google's own text on the four dots;
  - GOV.UK, NHS and NASA guideline PDFs (extracts only);
  - Wolff Olins, Koto, CGH, Collins and Johnson Banks case studies (Mozilla type via Mozilla/Typotheque extracts only);
  - H&Co's full pairing article;
  - the OFL FAQ at its canonical URL (read via the SIL copy in a SIL font repo).
- **No primary source** for:
  - measurable type-pairing criteria;
  - a minimum number of palette colours;
  - colour-to-meaning mappings (colour psychology);
  - CMYK/Pantone derivation for agents;
  - the trademark strength of free-font wordmarks.
- **All thresholds marked "proposed default"** need calibration. Examples: ΔEOK step ≥ 0.04, ≤ 4 brand hues, ≥ 10/12 "same system", the 4.55 solver margin, status ΔL ≥ 0.10. Calibrate them by running the checks on documented systems (USWDS, Material baseline, GOV.UK) before using them as gates.
