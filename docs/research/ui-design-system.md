# From brand identity to UI design system: tokens, character, components and formats

**Question.** How do practitioners get from a logo, palette and type pairing to a UI design system? This covers design tokens (colour roles, type scale, spacing, radius, elevation, motion), how brand character reaches components beyond colour (shape, density, motion, illustration), what a minimal credible component set is, and which token formats and structures are in common use. It also covers what Claude's Design System artifact type expects as input, so the output can be delivered as one.

**Purpose.** Input to the spec for a Claude Agent Skill that first designs a brand identity (SVG logo system, palette, type pairing, graphic language, brand sheet) and then derives a UI design system from it. The identity comes first; the UI system derives from it. Two decisions bind this note. First, a **render-then-rubric gate**: output is rendered, scored and redone if weak. Second, **never invent standards or APIs**. Every rule is therefore stated as a check: one a script can run (*script*), one the model judges by viewing a render (*model-visual*), or one only a person can judge (*human*). The note aims to clear four fog items: *component set and fidelity*, *quality gate for the UI system*, *colour method (roles)*, and *the seam to flutter-ui-design*.

> **How these sources were read. Please read this first.**
> The network policy blocked every design-system website: `designtokens.org`, `w3.org`, `m3.material.io`, `styledictionary.com`, `radix-ui.com`, `carbondesignsystem.com`, `polaris-react.shopify.com`, `open-props.style` and `tailwindcss.com` all failed DNS or returned no connection. **GitHub and the npm registry were reachable, so nearly every claim below was read in full from the system's own source repository or published package.** That counts as a primary source: the token files are the systems' actual values, and most of these systems' documentation sites are built from the same repositories. Repositories were shallow-cloned on 2026-11-17, and links point to the default branch. Commits: carbon `84127bd`, carbon-website `5e9cd1d`, design-tokens/community-group `882ebd6`, material-web `cde7082`, material-color-utilities `f242efc`, material-components-android `66b0eeb`, primer/primitives `4773648`, Shopify/polaris `3f7954a`, adobe/spectrum-design-data `92e77eb`, radix-ui/website `402e749`, tailwindcss `ae63833`, open-props `f39ab7c`, style-dictionary `795233d`, w3c/wcag `2766fae`, w3c/wcag3 `c110b49`, alphagov/govuk-frontend `f0d6e2f`, salesforce-ux/theo `9f6832d`. Atlassian's tokens were read from the npm tarball `@atlaskit/tokens@20.12.0`.
> **Web search was used only for the DTCG publication date and the APCA history.** Those claims are marked where they rest on search extracts.
> **Claude's Design System type** was read **read-only** with the Artifact tool: `list scope:"types"`, `read type_url`, and `read` of `format.md`, `craft.md`, `cover.md` and `demo.json` by path (release `1794863772-48f6`). Nothing was published, created or deleted.
> **Code checks** were run in a scratch directory, not in the repo (§10): role-palette contrast, type-scale arithmetic, DTCG schema validation, and DTCG → Claude Design System conversion.
> **Numbers labelled "proposed default — not a documented standard" are mine.**

---

## 1. Answer

**Conclusions first.**
- **Every well-documented system uses the same three tiers.** Tier 1 is a *reference palette* of raw values: tonal ramps, a size base. Tier 2 is a *system/semantic* layer of roles that alias tier 1. Tier 3 is an optional *component* layer that aliases tier 2. Material names the tiers `md-ref` → `md-sys` → `md-comp` ([material-web tokens](https://github.com/material-components/material-web/tree/main/tokens)). Carbon calls them value → token → role → theme ([Carbon themes overview](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/themes/overview.mdx)). Primer uses `base` → `functional` → `component` ([primer/primitives src/tokens](https://github.com/primer/primitives/tree/main/src/tokens)). GOV.UK uses palette → `govuk-functional-colour(...)` ([CHANGELOG v6.0.0](https://github.com/alphagov/govuk-frontend/blob/main/CHANGELOG.md)). **For this skill, the identity's palette is tier 1 and the UI system is tiers 2–3.**
- **Brand colour becomes roles by generating a tonal ramp per brand hue, then assigning roles by tone so that contrast is guaranteed by construction.** Material does this in HCT, with fixed tones per role (primary = T40 light / T80 dark) ([MCU scheme generation](https://github.com/material-foundation/material-color-utilities/blob/main/concepts/scheme_generation.md)). Radix does it with 12 steps, each with a stated use ([understanding-the-scale](https://github.com/radix-ui/website/blob/main/data/colors/docs/palette-composition/understanding-the-scale.mdx)). Atlassian does it in code: it takes one brand hex, finds its closest step on a generated 10-step ramp, branches on its contrast with white, and mirrors the ramp for dark mode ([`generate-token-map.js`](https://www.npmjs.com/package/@atlaskit/tokens)). **The exact brand hex usually lands on a *container/bold* role, not on the role used for text.** Running Material's own library on four brand colours shows this (§3.3).
- **Type, spacing and radius scales in real systems are *engineered*, not pure modular scales.** Carbon grows its type scale by a formula with step increments of 2 px ([scale.ts](https://github.com/carbon-design-system/carbon/blob/main/packages/type/src/scale.ts)). Material's 15 type roles have step ratios from 1.09 to 1.38. Spacing everywhere is a 4/8-px base with hand-picked steps (§4–5).
- **Brand character beyond colour is carried by a few global knobs: corner shape, density, motion personality and a second "expressive" type set.** Systems expose these as theme-level settings. Radix has a `radius` factor and a `scaling` of 90–110 % ([radius.mdx](https://github.com/radix-ui/website/blob/main/data/themes/docs/theme/radius.mdx), [spacing.mdx](https://github.com/radix-ui/website/blob/main/data/themes/docs/theme/spacing.mdx)). Carbon has *productive vs expressive* motion curves and type sets ([motion overview](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/motion/overview.mdx)). Spectrum has desktop/mobile component heights ([layout.json](https://github.com/adobe/spectrum-design-data/blob/main/packages/tokens/src/layout.json)). Material says it "encourages brand expression through shapes" ([MDC Shape.md](https://github.com/material-components/material-components-android/blob/master/docs/theming/Shape.md)).
- **The minimal credible component set is the six components all five sampled systems ship:** button, text input, checkbox, radio, select, tabs. Seven more appear in four of five systems (§7). **But Claude's Design System type says a brand built from scratch with no components should get a *small* first system with no components**, and a standard set only on request ([type SKILL.md / craft.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd)). So components are a second tier.
- **The interchange format is the W3C DTCG Format Module 2025.10, published as stable on 2025-10-28.** Carbon's token files already declare its schema ([layout.tokens.json](https://github.com/carbon-design-system/carbon/blob/main/packages/layout/tokens/layout.tokens.json)). **But Claude's Design System type cannot read DTCG.** It needs its own list-shaped `tokens.json` and has no motion family. The skill must therefore *emit two formats from one source*: DTCG for interchange (and as the Flutter source), and the Claude list shape for delivery (§8–9).

### Derivation table: identity input → UI token family

| Identity input | UI token family | Documented method | Key source | Check |
|---|---|---|---|---|
| Brand palette (1–3 hues + neutrals) | Tonal ramps (tier 1) | One perceptual-lightness ramp per hue: HCT tones 0–100, Radix 12 steps, GOV.UK tints and shades | [MCU](https://github.com/material-foundation/material-color-utilities/blob/main/concepts/color_spaces.md); [Radix](https://github.com/radix-ui/website/blob/main/data/colors/docs/palette-composition/understanding-the-scale.mdx); [GOV.UK v6](https://github.com/alphagov/govuk-frontend/blob/main/CHANGELOG.md) | script: monotone lightness; the brand hex is present in its ramp (or its nearest step is recorded) |
| Ramps | Colour roles (tier 2), light + dark | Role = fixed tone or step per theme; pairs (`on-X` / `X`) chosen so the tone gap guarantees contrast | [material-web `_md-sys-color.scss`](https://github.com/material-components/material-web/blob/main/tokens/versions/v0_192/_md-sys-color.scss) | script: the pair list in §10 |
| Type pairing | Families + type roles | Brand face for display/headline, text face for body/label. Role names display/headline/title/body/label (M3), or productive/expressive sets (Carbon) | [material-web typescale](https://github.com/material-components/material-web/blob/main/tokens/versions/v0_192/_md-sys-typescale.scss); [Carbon typography](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/typography/overview.mdx) | script: monotone sizes, line height on a 4 px grid; model-visual: hierarchy reads |
| Logo geometry (corner treatment, stroke module) | Radius scale, border width, icon stroke | Shape is a theme-level brand knob, scaled contextually per component | [MDC Shape](https://github.com/material-components/material-components-android/blob/master/docs/theming/Shape.md); [Radix radius](https://github.com/radix-ui/website/blob/main/data/themes/docs/theme/radius.mdx) | model-visual + human: UI corners rhyme with the mark |
| Brand personality (strategy words) | Density, motion personality, elevation style | Productive vs expressive motion; desktop/mobile scale; layers vs shadows | [Carbon motion](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/motion/overview.mdx); [Spectrum layout](https://github.com/adobe/spectrum-design-data/blob/main/packages/tokens/src/layout.json) | human: which end of each knob; model-visual: consistency |
| Graphic language (pattern, illustration) | Illustration/pictogram rules, cover pattern | Pictograms with productive/expressive usage; the cover pattern is chosen from the system's own personality | [Carbon pictograms](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/pictograms/usage.mdx); [type cover.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd) | model-visual |

---

## 2. Token architecture: three tiers and role names

- **Origin.** The DTCG repository states that "Design tokens were created by the Salesforce design system team" ([DTCG README](https://github.com/design-tokens/community-group/blob/main/README.md)). Polaris quotes Salesforce's definition: tokens are "named entities that store visual design attributes … in place of hard-coded values" ([polaris-tokens README](https://github.com/Shopify/polaris/blob/main/polaris-tokens/README.md)). Salesforce's own Theo tool shows the early form: YAML `props` aliasing `aliases` (`"{!primary_color}"`) ([Theo README](https://github.com/salesforce-ux/theo/blob/master/README.md)).
- **Carbon's vocabulary is the clearest definition of the role layer.** A *token* is "a role-based identifier that assigns a value to a theme. Tokens are universal and never change across themes." A *role* is "the systematic usage(s) of a token. Roles cannot be changed between themes." A *theme* is "a collection of visual attributes assigned to the tokens" ([themes overview](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/themes/overview.mdx)). It also states the brand link: "Carbon's default themes are derived from the IBM Design Language color palette" ([color overview](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/color/overview.mdx)).
- **Role naming varies, but the roles are the same.**
  - Material: `primary / on-primary / primary-container / on-primary-container`, ×3 accents, `surface`, `surface-container-lowest…highest`, `outline`, `outline-variant`, `error`, `inverse-*`, `scrim`, `shadow` ([`_md-sys-color.scss`](https://github.com/material-components/material-web/blob/main/tokens/versions/v0_192/_md-sys-color.scss)).
  - Carbon: `background`, `layer-01..03`, `field-01..03`, `border-subtle/strong`, `interactive`, `background-brand` ([theme.tokens.json](https://github.com/carbon-design-system/carbon/blob/main/packages/themes/tokens/themes/g10/theme.tokens.json)).
  - Primer: `fgColor.default/muted`, `bgColor.*`, `borderColor.*` ([fgColor.json5](https://github.com/primer/primitives/blob/main/src/tokens/functional/color/fgColor.json5)).
  - GOV.UK: `brand, text, secondary-text, focus, focus-text, error, success, border, input-border, hover, link(-visited/-hover/-active)` ([`_colours-functional.scss`](https://github.com/alphagov/govuk-frontend/blob/main/packages/govuk-frontend/src/govuk/settings/_colours-functional.scss)).
- **The common minimum across them** is: page background, 2–3 raised surfaces, default and muted text, a brand/accent fill and the text on it, a subtle and a strong border, focus, link, and the status colours error, success and warning. Interaction states (hover, pressed, selected) are separate tokens. This list is my synthesis.
- **Themes are values per role, not new roles.** Spectrum stores each colour token as `sets: {light, dark, wireframe}` with an alias per set ([color-aliases.json](https://github.com/adobe/spectrum-design-data/blob/main/packages/tokens/src/color-aliases.json)). Primer keeps the light value in `$value` and dark/high-contrast/colour-blind values in `$extensions['org.primer.overrides']` ([fgColor.json5](https://github.com/primer/primitives/blob/main/src/tokens/functional/color/fgColor.json5)). Claude's Design System type uses the Spectrum shape: `value: {light, dark}` (§9).
- **Usage notes as machine-readable rules.** Primer attaches `$description` plus an `org.primer.llm` extension holding `usage` tags and `rules`, for example "RECOMMENDED default for all text" ([fgColor.json5](https://github.com/primer/primitives/blob/main/src/tokens/functional/color/fgColor.json5)). Claude's type requires "a usage note on every token" ([craft.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd)). Both point the same way: every derived token carries a one-line usage rule.

---

## 3. Colour: from brand palette to roles

### 3.1 Ramps

- **Material (HCT).** HCT is "hue, chroma, tone … based on CAM16 × L*". MCU does "most of calculation in HCT then converts the colors to sRGB" ([color_spaces.md](https://github.com/material-foundation/material-color-utilities/blob/main/concepts/color_spaces.md)). Tone is L*, so contrast follows from the tone gap alone: "a difference of 40 in tone guarantees a WCAG contrast ratio ≥ 3.0; a difference of 50 … ≥ 4.5" ([contrast_for_accessibility.md](https://github.com/material-foundation/material-color-utilities/blob/main/concepts/contrast_for_accessibility.md)).
- **Radix (12 steps).**
  - Steps 1–2: app backgrounds.
  - Steps 3–5: component backgrounds (normal, hover, pressed or selected).
  - Steps 6–8: borders (subtle non-interactive, subtle interactive, strong and focus rings).
  - Steps 9–10: solid fills. Step 9 is "the purest step"; step 10 is its hover.
  - Steps 11–12: low- and high-contrast text.
  - Steps 11 and 12 "are guaranteed to Lc 60 and Lc 90 APCA contrast ratio on top of a step 2 background" ([understanding-the-scale.mdx](https://github.com/radix-ui/website/blob/main/data/colors/docs/palette-composition/understanding-the-scale.mdx)).
  - A custom-palette tool generates all 12 steps "based just on a couple reference colors" ([custom-palettes.mdx](https://github.com/radix-ui/website/blob/main/data/colors/docs/overview/custom-palettes.mdx)).
- **GOV.UK (a real brand → UI case).** GOV.UK Frontend v6.0.0 adopted "the GOV.UK web palette from v1.0 of the GOV.UK brand guidelines". That palette "reduces the number of named colours but introduces tints and shades for each colour". The team added "25% and 50% shades for all colours except brown" and darkened green "to improve colour contrast and legibility". Old named colours were replaced by functional colours (`$govuk-brand-colour` → `govuk-functional-colour(brand)`) ([CHANGELOG v6.0.0](https://github.com/alphagov/govuk-frontend/blob/main/CHANGELOG.md)). **This is the documented path in miniature: brand palette → ramps → functional roles, with contrast forcing the ramp to grow.**
- **Tailwind v4 and Open Props** ship generic ramps (Tailwind: 11 steps per hue in `oklch()`) as CSS custom properties ([theme.css](https://github.com/tailwindlabs/tailwindcss/blob/main/packages/tailwindcss/theme.css); [open-props src](https://github.com/argyleink/open-props/tree/main/src)). They are tier 1 only, with no roles.

### 3.2 Roles by tone (Material baseline, read from tokens)

| Role | Light tone | Dark tone |
|---|---|---|
| primary / on-primary | 40 / 100 | 80 / 20 |
| primary-container / on-primary-container | 90 / 10 | 30 / 90 |
| surface / on-surface | 98 / 10 | 6 / 90 |
| on-surface-variant | NV30 | NV80 |
| outline / outline-variant | NV50 / NV80 | NV60 / NV30 |
| error / on-error | 40 / 100 | 80 / 20 |

The source is [`_md-sys-color.scss` v0_192](https://github.com/material-components/material-web/blob/main/tokens/versions/v0_192/_md-sys-color.scss) (NV = neutral-variant palette). MCU then adjusts tones per "contrast level" (−1, 0, 0.5, 1). Default contrast guarantees "4.5:1 for all text and icons" and "3:1 for required non-text elements" ([contrast_for_accessibility.md](https://github.com/material-foundation/material-color-utilities/blob/main/concepts/contrast_for_accessibility.md); [creating_color_scheme.md](https://github.com/material-foundation/material-color-utilities/blob/main/dev_guide/creating_color_scheme.md)).

### 3.3 Where the brand hex lands: an observed run

I ran `@material/material-color-utilities@0.3.0` (npm) on four brand colours. A WCAG 2 contrast function was written separately from the SC definition, so the check does not rely on MCU's own maths. Script: `roles.mjs` in the scratch directory.

| Brand hex (HCT chroma) | `tonalSpot` light primary (chroma) | `fidelity` light primaryContainer | Text/surface pairs ≥ 4.5? | outline/surface | outline-variant/surface |
|---|---|---|---|---|---|
| `#E8590C` orange (75.5) | `#8e4d31` (35.7) | `#cb4a00` (shifted) | yes, all | 4.25 | **1.62** |
| `#0F7A52` green (44.0) | `#246a4b` (35.9) | `#0f7a52` (**exact**) | yes, all | 4.27 | **1.63** |
| `#7B2FBE` purple (70.1) | `#6f528a` (36.1) | `#7b2fbe` (**exact**) | yes, all | 4.28 | **1.62** |
| `#F5C400` yellow (60.9) | `#735c0c` (36.1) | `#f5c400` (**exact**) | yes, all | 4.26 | **1.62** |

Findings:
1. **`tonalSpot`, the default, caps primary chroma at about 36**, so a vivid brand orange becomes a brown. Flutter documents the same thing: tonalSpot "builds pastel palettes with a low chroma", while `fidelity` palettes "match seed color, even if the seed color is very bright" ([Flutter `color_scheme.dart`](https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/material/color_scheme.dart)).
2. **`SchemeFidelity`/`SchemeContent` put the source colour in `primaryContainer`, "adjusted for color relativity"** (≈ ±5 tone) ([scheme_fidelity.ts](https://github.com/material-foundation/material-color-utilities/blob/main/typescript/scheme/scheme_fidelity.ts)). In 3 of 4 runs the exact hex came back. `primary`, the text/link role, is a darker tone of the same hue. **So the brand hex is a fill, and the text-safe sibling is derived.** Atlassian's code applies the same contrast-first logic in a different way ([`dist/esm/utils/generate-token-map.js` in @atlaskit/tokens 20.12.0](https://www.npmjs.com/package/@atlaskit/tokens)):
   - It generates a 10-step ramp and finds the step closest to the brand hex.
   - If the hex has ≥ 4.5:1 against white, that step drives `color.background.brand.bold`, `color.text.brand` and `color.link`, with hover and pressed one or two steps darker.
   - Otherwise every brand role falls back to fixed step 6 of the ramp. In dark mode the hex returns as the bold fill only if it reaches 4.5:1 with inverse text.
   - Dark mode mirrors light (`9 − index`).
3. **`outline-variant` fails 3:1 by design.** Material uses it decoratively. Primer's ADR says decorative borders have "no contrast requirements", but the border of an *empty* control needs 3:1 ([ADR-010](https://github.com/primer/primitives/blob/main/contributor-docs/adrs/adr-010-color-contrast.md)). **The check must therefore be role-aware.** Only roles whose usage says "control boundary" are held to 3:1.
4. MCU's repo is at 0.4.0, with newer `color_spec_2025/2026` files ([dynamiccolor/](https://github.com/material-foundation/material-color-utilities/tree/main/typescript/dynamiccolor)). Tones may differ slightly under the newer spec. **(not re-run on 0.4.0)**

### 3.4 Contrast standard (and APCA status)

- **WCAG 2.2 AA is the normative floor.** Text needs 4.5:1, or 3:1 for large text ([SC 1.4.3](https://github.com/w3c/wcag/blob/main/guidelines/sc/20/contrast-minimum.html)). UI components and graphical objects need 3:1 against adjacent colours ([SC 1.4.11](https://github.com/w3c/wcag/blob/main/guidelines/sc/21/non-text-contrast.html)). Targets need ≥ 24×24 CSS px or spacing ([SC 2.5.8](https://github.com/w3c/wcag/blob/main/guidelines/sc/22/target-size-minimum.html)). The focus indicator should be ≥ a 2 px perimeter at 3:1 (AAA) ([SC 2.4.13](https://github.com/w3c/wcag/blob/main/guidelines/sc/22/focus-appearance.html)).
- **The logotype exemption.** "Text that is part of a logo or brand name has no contrast requirement" ([SC 1.4.3](https://github.com/w3c/wcag/blob/main/guidelines/sc/20/contrast-minimum.html)). The *mark* is exempt; the UI derived from it is not.
- **APCA is not a standard.** The WCAG 3 editor's draft says text contrast "meets @@[contrast measure to be determined]", with the ednote "The contrast algorithm used in WCAG 3 is yet to be determined" ([text-contrast-sufficient-minimum.md](https://github.com/w3c/wcag3/blob/main/guidelines/groups/text-and-wording/text-appearance/text-contrast-sufficient-minimum.md)). Search extracts say APCA was dropped from the July 2023 WCAG 3 draft ([Roselli, April 2026](https://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html)) **(secondary)**. Radix states its guarantees in APCA Lc (above). **Use WCAG 2 ratios as the gate; APCA Lc may be reported for information only.**
- **High contrast and colour vision.** Primer sets 7:1 text and 4.5:1 borders for its high-contrast themes ([colorContrast.config.ts](https://github.com/primer/primitives/blob/main/scripts/colorContrast.config.ts)). It ships tritanopia and colour-blind themes ([README](https://github.com/primer/primitives/blob/main/README.md)). Claude's type defines a "high-contrast theme" as an *added* theme at 7:1. Its colour-blind-safe status rule is: differ in lightness ≥ 3:1, or move success off the red–green axis ([craft.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd)).

---

## 4. Type: pairing → families → a role scale

- **Role sets in use.**
  - Material: 15 roles, display/headline/title/body/label × L/M/S, each with font, size, line height, weight and tracking. Body-large is 16/24 px, display-large 57/64 px, label-small 11/16 px ([`_md-sys-typescale.scss`](https://github.com/material-components/material-web/blob/main/tokens/versions/v0_192/_md-sys-typescale.scss)).
  - Carbon: *productive* (product) and *expressive* (marketing) type sets, with "productive in expressive" crossovers ([typography overview](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/typography/overview.mdx)).
  - Spectrum: `component-s/m/l-regular/medium/bold` plus CJK-specific line heights ([typography.json](https://github.com/adobe/spectrum-design-data/blob/main/packages/tokens/src/typography.json)).
- **The scales are not pure modular scales.** I computed step ratios with `scale.py`:

| System | Sizes (px) | Step ratio min–max | Geometric mean |
|---|---|---|---|
| Material 3 | 11 12 14 16 22 24 28 32 36 45 57 | 1.09–1.38 | 1.18 |
| Carbon `scale01–17` | 12 14 16 18 20 24 28 32 36 42 48 54 60 68 76 84 92 | 1.10–1.20 | 1.14 |
| Tailwind v4 `--text-*` | 12 14 16 18 20 24 30 36 48 60 72 96 128 | 1.11–1.33 | 1.22 |

- **Carbon's sizes come from a recurrence:** `Yn = Yn-1 + (⌊(n−2)/4⌋+1)·2` ([scale.ts](https://github.com/carbon-design-system/carbon/blob/main/packages/type/src/scale.ts)). My script confirms it reproduces all 17 steps.
- **Every Material line height is a multiple of 4.**
- **A pure modular scale collides when snapped to a 4-px grid.** 16·1.2ᵏ snapped to 4 px gives 12, 12, 16 … (one collision). Ratio 1.125 gives three collisions. **Implication:** generate from a ratio, round to whole px, keep the steps distinct, and put line heights on the 4-px grid. Do not insist on exact ratio purity.
- **Pairing to roles (inference, supported by the Carbon and Material role split).** The identity's display face fills display/headline (Carbon's "expressive"). The text face fills title/body/label ("productive"). If the identity has only one family, it carries both, and the hierarchy comes from size and weight. flutter-ui-design caps UI text at 2 weights ([SKILL.md](../../skills/engineering/flutter-ui-design/SKILL.md)). Claude's type expects real font files or a hosted (Google) face named in `type.families` ([format.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd)).

## 5. Spacing, radius, elevation, motion

| Family | Material 3 | Carbon | Polaris | Primer / Spectrum / Tailwind | flutter-ui-design default |
|---|---|---|---|---|---|
| Spacing | (no sys spacing tokens in material-web) | 2 4 8 12 16 24 32 40 48 64 80 96 160 px ([layout.tokens.json](https://github.com/carbon-design-system/carbon/blob/main/packages/layout/tokens/layout.tokens.json)) | `space-100` = 4 px; names = 4-px multiples × 100 ([size.ts](https://github.com/Shopify/polaris/blob/main/polaris-tokens/src/size.ts)) | Primer 2 4 8 12 16 24 … with usage rules ([space.json5](https://github.com/primer/primitives/blob/main/src/tokens/functional/spacing/space.json5)); Tailwind one `--spacing: 0.25rem` multiplier ([theme.css](https://github.com/tailwindlabs/tailwindcss/blob/main/packages/tailwindcss/theme.css)) | 4 8 12 16 24 32 48 64 |
| Radius | 0 4 8 12 16 28 full ([`_md-sys-shape`](https://github.com/material-components/material-web/blob/main/tokens/versions/v0_192/_md-sys-shape.scss)) | — | 0 2 4 6 8 12 16 20 30 full ([border.ts](https://github.com/Shopify/polaris/blob/main/polaris-tokens/src/themes/base/border.ts)) | Spectrum `corner-radius-100` = 4 px; Tailwind 2 4 6 8 12 16 24 32 | 4 8 12 16 full |
| Elevation | levels 0 1 3 6 8 12 dp ([`_md-sys-elevation`](https://github.com/material-components/material-web/blob/main/tokens/versions/v0_192/_md-sys-elevation.scss)) | *Layering model*: depth by stepped surface colour (`layer-01..03`) ([color overview](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/color/overview.mdx)) | `shadow` tokens ([shadow.ts](https://github.com/Shopify/polaris/blob/main/polaris-tokens/src/themes/base/shadow.ts)) | — | outline borders; shadow only for floating layers |
| Motion | durations 50–1000 ms in 16 steps; emphasized/standard easings ([`_md-sys-motion`](https://github.com/material-components/material-web/blob/main/tokens/versions/v0_192/_md-sys-motion.scss)); springs fast/default/slow × spatial/effects ([MDC Motion.md](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md)) | 70 110 150 240 400 700 ms; productive vs expressive curves ([motion.tokens.json](https://github.com/carbon-design-system/carbon/blob/main/packages/motion/tokens/motion.tokens.json)) | `motion.ts` | — | 100 200 300 ms |

**Reading across the table.** Spacing is uniformly a 4-px base with a geometric-ish tail. Radius is 4–7 steps plus `full`. Elevation splits into two schools: *shadows* (Material, Polaris) and *layers/borders* (Carbon, and flutter-ui-design's "elevation 0 + outline"). That split is itself a brand-character choice (§6).

---

## 6. Brand character beyond colour

| Knob | What systems expose | Evidence | How the identity sets it (inference) |
|---|---|---|---|
| **Corner shape** | One theme-level factor, applied *contextually*. With Radix `full`, a Button becomes a pill but a Checkbox "will never become fully rounded to prevent any confusion between it and a Radio" | [Radix radius.mdx](https://github.com/radix-ui/website/blob/main/data/themes/docs/theme/radius.mdx); Material "encourages brand expression through shapes", with cut corners and edge treatments ([MDC Shape.md](https://github.com/material-components/material-components-android/blob/master/docs/theming/Shape.md)); Open Props even ships hand-drawn `--radius-drawn-1..6` ([props.borders.js](https://github.com/argyleink/open-props/blob/main/src/props.borders.js)) | Take the mark's dominant corner treatment (sharp, small round, large round, cut) and stroke module. Map it to a radius factor, never to a per-component whim |
| **Density** | A global scale on spacing, font size and line height (Radix `scaling` 90–110 %); per-platform sizes (Spectrum `component-height-100` 32 px desktop / 40 px mobile) | [Radix spacing.mdx](https://github.com/radix-ui/website/blob/main/data/themes/docs/theme/spacing.mdx); [Spectrum layout.json](https://github.com/adobe/spectrum-design-data/blob/main/packages/tokens/src/layout.json) | Personality words ("precise, technical" → compact; "calm, generous" → comfortable) choose the factor. Accessibility targets bound it (§10) |
| **Motion personality** | Two named curve families. *Productive* "efficiency and responsiveness … subtle"; *expressive* "enthusiastic, vibrant … for significant moments" | [Carbon motion overview](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/motion/overview.mdx); Material springs: "Effects springs … should not be overshot" ([MDC Motion.md](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md)) | Choose the default family from the brand voice. Expressive motion only for page-level moments |
| **Typographic voice** | Separate productive/expressive type sets | [Carbon typography](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/typography/overview.mdx) | Brand display face = expressive set; text face = productive |
| **Depth style** | Shadows vs tonal layers vs borders | §5 table | Flat or editorial identities → borders/layers; tactile or playful → shadows |
| **Illustration / pictograms** | A pictogram library with productive vs expressive usage, sizing, clearance and colour rules | [Carbon pictograms usage](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/pictograms/usage.mdx) | The identity's graphic language (pattern, motif) becomes empty-state and marketing art, with icon stroke = mark stroke module |
| **Cover / brand face of the system** | Claude's type picks *one* pattern from the system's own personality ("soft, friendly, large radii → discs, pills"; "precise, technical, mono, a 4px grid → a dot or plus grid"; "editorial, serif, 'borders not shadows' → a FEW hairline rules") | [cover.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd) | Derive the pattern from the identity's graphic language, using token geometry only |

**No primary source gives a numeric mapping from personality words to these knobs.** The right-hand column is a proposed design method, not a documented standard. The documented part is that the knobs exist as global, named settings.

---

## 7. A minimal credible component set

I listed the component folders of five systems: Carbon React, Polaris React, GOV.UK Frontend, Radix Themes and Material Web. The table below counts them, normalised by hand for naming (e.g. `radios`/`RadioButton`). Material Web's text field covers textarea; its tables and badges are absent from that repo.

| In 5 of 5 | In 4 of 5 | In 3 of 5 |
|---|---|---|
| button, text input, checkbox, radio, select, tabs | tag/badge, table, alert/banner/notification, dialog/modal, menu, progress/spinner, slider | tooltip, textarea, switch, skeleton, pagination, link, icon button, divider, card, breadcrumb, accordion |

Sources: [carbon packages/react/src/components](https://github.com/carbon-design-system/carbon/tree/main/packages/react/src/components); [polaris-react/src/components](https://github.com/Shopify/polaris/tree/main/polaris-react/src/components); [govuk-frontend components](https://github.com/alphagov/govuk-frontend/tree/main/packages/govuk-frontend/src/govuk/components); [Radix Themes component docs](https://github.com/radix-ui/website/tree/main/data/themes/docs/components); [material-web](https://github.com/material-components/material-web).

**What Claude's type says.**
- From scratch with nothing to build from, make "a SMALL first system (6–10 colors in one theme, 5–7 text styles, 4 spacing steps, 3 radii, a one-paragraph README, no components) and say so".
- "Only a from-scratch or guidelines-only brand gets a standard set" of components.
- Each component needs a live `preview.html` and a `README.md`; components ship as one `bundle.js` that sets `window.<namespace>`, with React 18.

([type SKILL.md, craft.md, format.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd)). The type's own demo, *Ember*, ships exactly two components: Button and Badge ([demo.json](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd)).

**Proposed tiers (proposed default — not a documented standard).**
- **Tier 0 (always):** tokens + README brand book + logo assets + cover. This matches the type's small first system, but with the identity's full palette in two themes.
- **Tier 1 "credible core" (default on):** Button (primary/secondary/quiet + focus), Text input (with label, hint, error), Checkbox, Radio, Select, Tabs. These are the 5-of-5 set; each is cheap to preview and exercises every colour role, the radius knob and the focus ring.
- **Tier 2 (on request):** Badge/Tag, Alert/Banner, Dialog, Card, Table, Menu, Progress. Card is included because it is where shape and elevation character shows most, even though it is only 3-of-5.

---

## 8. Token formats in use

- **The W3C DTCG Format Module, 2025.10.**
  - **Status.** The community group announced "first stable version" 2025.10 on 2025-10-28 ([W3C DTCG post](https://w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/), via search extract; the final report is at [CG-FINAL-format-20251028](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/), not opened). It is a Community Group report, not a W3C Recommendation. The repo's `main` branch now carries a "**preview draft** of in progress changes. Do not … implement anything in this document", with `latestVersion: …/TR/2025.10/format/` ([format/index.html](https://github.com/design-tokens/community-group/blob/main/technical-reports/format/index.html)). **Target 2025.10, not `main`.**
  - **Shape.**
    - A token is an object with `$value`; it may also have `$type`, `$description`, `$extensions` and `$deprecated`. `$type` is inherited from groups ([design-token.md](https://github.com/design-tokens/community-group/blob/main/technical-reports/format/design-token.md); [groups.md](https://github.com/design-tokens/community-group/blob/main/technical-reports/format/groups.md)).
    - References use `"{group.token}"` or JSON Pointer `$ref` ([aliases.md](https://github.com/design-tokens/community-group/blob/main/technical-reports/format/aliases.md)).
    - Files are `.tokens` / `.tokens.json`, with media type `application/design-tokens+json` ([file-format.md](https://github.com/design-tokens/community-group/blob/main/technical-reports/format/file-format.md)).
  - **Types.**
    - Simple types: color, dimension, fontFamily, fontWeight, duration, cubicBezier, number.
    - Composite types: strokeStyle, border, transition, shadow, gradient, typography ([types.md](https://github.com/design-tokens/community-group/blob/main/technical-reports/format/types.md); [composite-types.md](https://github.com/design-tokens/community-group/blob/main/technical-reports/format/composite-types.md)).
    - **Colour is an object**, `{colorSpace, components, alpha?, hex?}`, with spaces including `srgb` and `oklch` ([color-type.md](https://github.com/design-tokens/community-group/blob/main/technical-reports/color/color-type.md)).
    - **Dimension is `{value, unit}`, with unit `px` or `rem` only** ([types.md](https://github.com/design-tokens/community-group/blob/main/technical-reports/format/types.md)).
  - **Themes and modes** are a separate *Resolver* module: "Theming, such as light mode, dark mode, and high contrast color modes; Sizing … Accessibility mode" ([resolver/introduction.md](https://github.com/design-tokens/community-group/blob/main/technical-reports/resolver/introduction.md)).
  - **A JSON Schema exists** in the repo ([schemas/src/2025.10](https://github.com/design-tokens/community-group/tree/main/schemas/src/2025.10)).
- **Adoption seen in source.**
  - Carbon's token files declare `"$schema": "https://www.designtokens.org/schemas/2025.10/format.json"` and use `{value, unit}` dimensions and `$ref` colour components ([layout.tokens.json](https://github.com/carbon-design-system/carbon/blob/main/packages/layout/tokens/layout.tokens.json); [theme.tokens.json](https://github.com/carbon-design-system/carbon/blob/main/packages/themes/tokens/themes/g10/theme.tokens.json)).
  - Primer uses DTCG `$value`/`$type`/`$extensions` keys in JSON5 ([fgColor.json5](https://github.com/primer/primitives/blob/main/src/tokens/functional/color/fgColor.json5)).
  - Style Dictionary 5.8 has DTCG support "as of version 4". However, "the latest format 2025.10 does not have full support yet", and that work is in progress in v5 ([DTCG.mdx](https://github.com/style-dictionary/style-dictionary/blob/main/docs/src/content/docs/info/DTCG.mdx)).
  - Spectrum uses its own JSON schema, with `sets` per theme and a uuid per token, and calls its legacy package "generated legacy output" ([tokens README](https://github.com/adobe/spectrum-design-data/blob/main/packages/tokens/README.md)).
  - Tailwind v4 and Open Props use **CSS custom properties as the format**: `--color-blue-500: oklch(…)`, `--spacing`, `--radius-*`, `--text-*` ([theme.css](https://github.com/tailwindlabs/tailwindcss/blob/main/packages/tailwindcss/theme.css)).
- **Observed (`dtcg.mjs`, ajv against the repo's 2025.10 schema).**
  - My sample brand file with object colours and `{value,unit}` dimensions validates.
  - Carbon's `layout.tokens.json` and `motion.tokens.json` validate.
  - **The legacy forms `"$value": "#a23a00"` and `"$value": "8px"` are INVALID under 2025.10** ("must be object"). Older DTCG drafts, and Style Dictionary v3/v4 examples, use those strings. **Generators must emit the 2025.10 object forms.**

---

## 9. Claude's Design System type: the input contract, as a derivation target

The full file contract (index, paths, caps, upload flow, write order) is already recorded in [claude-design-capabilities.md §3.1](claude-design-capabilities.md). I re-read it at the same release (`1794863772-48f6`). The points that bind *derivation* are:

- **`tokens.json` is list-shaped and not DTCG.** "Every family but `type` … is `{"tokens":[{"name","value","usage"}, …]}`." A DTCG map "is valid JSON the page CANNOT read: the family shows empty".
  - Colour: `color.themes[]` plus a flat `color.tokens[]` whose `value` is `{"light": …, "dark": …}`. A missing theme inherits the first theme's value.
  - Values: hex, `rgb()`/`hsl()`/`oklch()` with plain numbers, or an alias `"{other-token}"` to an *existing* colour token.
  - Names match `^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$` and are unique across families.
  - Caps: ≤ 8 themes, ≤ 600 colours, ≤ 60 tokens per other family.
  - `type` is `{fonts[], families{}, groups[{name, family, styles[{name, fontSize, lineHeight, fontWeight…}]}]}`. ≤ 12 groups / 80 styles ([format.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd)).
- **Optional families.** `shadow` takes per-theme values. Up to 12 other `{tokens:[…]}` keys (e.g. `opacity`, `zIndex`) take "plain CSS values … single values, not composites". **The docs say "No motion family."** Whether a family under another name (e.g. `duration`) would display is **untested**. Put motion in README prose and `bundle.css` custom properties.
- **Components.**
  - `components/<Comp>/preview.html`: line 1 is `<!-- @dsCard group="…" height=N -->`, it renders "ONE component (a few states)", and runs with `tokens.css`, the fonts, `bundle.css` and `bundle.js` preloaded.
  - `components/<Comp>/README.md`: its first sentence is the summary, and it should say "what the consumer provides".
  - `components/bundle.js`: one classic script that assigns `window.<namespace>`; React 18.
  - `components/index.d.ts`: types as documentation ([format.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd)).
- **Craft rules that act as gates** ([craft.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd)):
  - text ≥ 4.5:1 on the grounds its usage note names, in *every* theme (3:1 for 24 px+ text, borders, focus rings and icons);
  - fills that change across themes get an `on-…` token instead of literal white;
  - a solid focus ring at ≥ 3:1 on every surface;
  - status colours told apart by lightness;
  - no AI tropes ("bluish-purple gradients, emoji as decoration, rounded cards with a coloured left-border accent", overused fonts such as Inter and Roboto).
- **Conversion, observed.** `to_claude_ds.mjs` flattens DTCG paths to names (`palette.orange.40` → `palette-orange-40`), rewrites aliases, maps `dimension` groups to `spacing`/`radius`, and runs the type's drop rules as checks: name regex, duplicates, alias target exists, readable colour value, usage note present.
  - On my sample it **dropped `duration` and `cubicBezier` tokens**, because there is nowhere to put them.
  - It **flagged 8 tokens with no usage note.** The DTCG source must therefore carry `$description` on every token, or the Claude output fails the type's own checklist.
  - Composite DTCG `typography` tokens must be split into `type.groups[].styles[]`.

---

## 10. Quality gate for the UI system: rules as checks

| # | Rule | Evidence | Check type | How to check → threshold |
|---|---|---|---|---|
| U1 | Every text-role / ground pair named in a usage note meets 4.5:1 (3:1 for ≥ 24 px or bold ≥ 18.66 px) in every theme | [SC 1.4.3](https://github.com/w3c/wcag/blob/main/guidelines/sc/20/contrast-minimum.html); [type craft.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd); Primer's pair list ([colorContrast.config.ts](https://github.com/primer/primitives/blob/main/scripts/colorContrast.config.ts)) | script | Build the pair list from usage notes (Primer pattern) and compute the WCAG 2 ratio per theme. Fail below threshold |
| U2 | Control boundaries, focus ring and meaningful icons ≥ 3:1 against adjacent colours; decorative borders exempt | [SC 1.4.11](https://github.com/w3c/wcag/blob/main/guidelines/sc/21/non-text-contrast.html); [Primer ADR-010](https://github.com/primer/primitives/blob/main/contributor-docs/adrs/adr-010-color-contrast.md) | script | Role-aware: only roles tagged boundary/focus/icon are checked. `outline-variant`-type roles are tagged decorative (§3.3 shows they sit at ~1.6:1) |
| U3 | The brand hex is reproduced exactly in at least one fill role, and text/link roles use a contrast-safe sibling | [scheme_fidelity.ts](https://github.com/material-foundation/material-color-utilities/blob/main/typescript/scheme/scheme_fidelity.ts); [Atlassian generate-token-map.js](https://www.npmjs.com/package/@atlaskit/tokens) | script | The exact hex appears in tier 2 (light theme); if its contrast with the text on it is < 4.5:1, an `on-` token exists that passes. Proposed rule — neither source *requires* the exact hex (Atlassian falls back to a ramp step) |
| U4 | Light and dark themes have the same role set; a dark fill that lightens gets dark `on-` text | [Carbon themes](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/elements/themes/overview.mdx) ("roles cannot be changed between themes"); [craft.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd) | script | Set equality of role names per theme; U1 per theme |
| U5 | Status colours are distinguishable without hue, and each carries a word or icon | [craft.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd) | script + model-visual | Success vs error lightness contrast ≥ 3:1, or success hue outside the red–green axis. Model checks the previews show text or an icon |
| U6 | Ramps are monotone in lightness, with no duplicate steps | Radix and HCT ramps ([understanding-the-scale](https://github.com/radix-ui/website/blob/main/data/colors/docs/palette-composition/understanding-the-scale.mdx); [color_spaces.md](https://github.com/material-foundation/material-color-utilities/blob/main/concepts/color_spaces.md)) | script | L* strictly monotone. Proposed default — not a documented standard: adjacent ΔL* ≥ 2 |
| U7 | Type sizes strictly increase; line heights sit on a 4-px grid; ratio between adjacent steps 1.06–1.42 | Range observed in M3/Carbon/Tailwind (§4) | script | Proposed default — not a documented standard (the bounds bracket the observed 1.09–1.38) |
| U8 | Spacing values all come from one base (4 px); ≤ 12 steps; nothing off-scale in previews | Carbon, Polaris, Primer, Tailwind (§5); flutter-ui-design | script | Every spacing token % 4 == 0 except the 2-px hairline step. Grep previews and `bundle.css` for literal px not in the scale |
| U9 | Radius: ≤ 7 steps plus `full`; one factor; checkbox never fully round | [Radix radius](https://github.com/radix-ui/website/blob/main/data/themes/docs/theme/radius.mdx); M3 shape | script + model-visual | Count steps; model checks the checkbox/radio distinction at the chosen factor |
| U10 | Interactive targets ≥ 24×24 CSS px (WCAG AA); ≥ 44–48 for touch-first | [SC 2.5.8](https://github.com/w3c/wcag/blob/main/guidelines/sc/22/target-size-minimum.html); flutter-ui-design AUDIT (48 dp) | script | Measure the rendered preview boxes. The density knob (§6) may not push below this |
| U11 | Focus ring visible: solid, ≥ 2 px, ≥ 3:1 on every surface it can land on | [SC 2.4.13](https://github.com/w3c/wcag/blob/main/guidelines/sc/22/focus-appearance.html); [craft.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd) | script + model-visual | Render a focused state per component |
| U12 | Every token has a usage note; names valid; no duplicates; aliases resolve; `tokens.json` passes the type's drop rules | [format.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd) | script | `to_claude_ds.mjs`-style validator: zero problems |
| U13 | The DTCG export validates against the 2025.10 schema | [DTCG schemas](https://github.com/design-tokens/community-group/tree/main/schemas/src/2025.10) | script | ajv validation. Zero errors |
| U14 | Brand fit: UI corners, density, motion and depth match the identity (mark's corner treatment, personality words) | §6 (knobs documented; the mapping is not) | model-visual + human | Model views a specimen screen next to the brand sheet and answers "same family?" with reasons. A human approves the knob settings |
| U15 | No AI tropes | [craft.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd) | model-visual | Checklist on the rendered previews and cover |

---

## 11. Seam to flutter-ui-design

What flutter-ui-design already owns is listed in its [SKILL.md](../../skills/engineering/flutter-ui-design/SKILL.md), [THEME.md](../../skills/engineering/flutter-ui-design/references/THEME.md) and [AUDIT.md](../../skills/engineering/flutter-ui-design/references/AUDIT.md):
- tokens in Dart (`Space`, `Radii`, `Motion`);
- `ThemeData` assembly and the Material 3 anti-defaults (purple seed, tonal mud, elevation soup, over-rounding);
- adaptive navigation;
- the screen audit.

**The new skill should not duplicate any of it.** The seam:

1. **The new skill emits a DTCG 2025.10 file as the platform-neutral source.** flutter-ui-design consumes it under its "if the project already has a brand, adopt its tokens" clause. Spacing, radius and motion map onto `Space`/`Radii`/`Motion` by value. The default scales of the two skills are already compatible (§5).
2. **Colour: replace bare `fromSeed` with a brand-faithful scheme.** THEME.md's `ColorScheme.fromSeed(seedColor: _seed)` uses the default `DynamicSchemeVariant.tonalSpot`, which caps chroma (§3.3) and turns a vivid brand into pastels. Flutter's `fromSeed` accepts `dynamicSchemeVariant` (e.g. `DynamicSchemeVariant.fidelity`), `contrastLevel`, and per-role overrides (`primary:`, `onPrimary:` …) ([color_scheme.dart](https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/material/color_scheme.dart)). **Proposed handoff:** emit `fromSeed(seedColor: brand, dynamicSchemeVariant: DynamicSchemeVariant.fidelity)`, plus explicit overrides for any role whose hex the identity fixes. This is a small edit to THEME.md §2, not a new skill branch.
   - **(Inference)** Flutter uses the Dart port of the same MCU algorithms, so the §3.3 results should carry over. I ran the TypeScript port, not Flutter.
3. **Type.** The identity's display face maps to `display*`/`headline*`, and the text face to `title*`/`body*`/`label*`. flutter-ui-design's "≤ 2 weights" applies to UI text. The wordmark is an asset and is exempt (logotype exemption, §3.4).
4. **Audit.** flutter-ui-design's AUDIT floor (4.5:1, 48 dp targets, a dark theme from the same tokens) is a subset of U1–U11. The identity skill runs its gate on its own HTML previews. flutter-ui-design runs AUDIT on the Flutter screens. Neither re-implements the other.

---

## 12. Implications for the skill (inference: my reasoning, not sourced)

- **One source, three emitters.** Keep one internal token model (tier 1 ramps, tier 2 roles with per-theme values and a usage note each, and scales). Emit:
  1. Claude Design System `tokens.json` (list shape) + README + components;
  2. DTCG 2025.10 `.tokens.json`;
  3. optionally a Dart snippet for flutter-ui-design.
- **Colour method.** Use HCT (via MCU, which is already a published library on npm and pub) to build ramps from each identity hue. Assign roles by Material-style tone tables. Use the `fidelity` placement for the main brand hue so the brand hex survives as a fill role. Generate dark from the same roles. Then run U1–U6. Do not hand-pick tones.
- **Scales.** Base 4 px; spacing like flutter-ui-design's 4…64; radius from the mark's corner treatment through one factor; type from a ratio near 1.2, rounded, with line heights on 4 px. Then run U7–U9.
- **Character.** Ask for, or derive, four knob settings: radius factor, density, motion family, depth style. Show them on a specimen screen beside the brand sheet for U14.
- **Components.** Tier 1 by default, as React components in one `bundle.js` with one `preview.html` each. Each preview shows rest, hover, focus, disabled, and error where relevant, in both themes. This makes the previews the render surface for the model-visual checks.
- **Scripts the skill likely needs (suggestions; the interface is a later decision):** `ramp(hue_hex)`; `roles(ramps, variant, contrast_level)`; `contrast_pairs(tokens, theme)`; `scale_check(tokens)`; `to_claude_ds(model)`; `to_dtcg(model)` + schema validation; `to_flutter(model)`; and a headless render of previews for the visual rubric.

---

## 13. Open disagreements and gaps

**Disagreements**
1. **Shadows vs layers.** Material and Polaris express depth with shadow/elevation tokens. Carbon uses a layering model. flutter-ui-design says "elevation 0 + outline". This is a brand-character choice, not a correctness issue.
2. **WCAG 2 vs APCA.** Radix guarantees APCA Lc values. WCAG 3 has not chosen an algorithm. WCAG 2.2 remains the only normative ratio, so the gate uses it.
3. **Exact brand hex vs generated tones.** Material's default (tonalSpot) regenerates brand colour. GOV.UK and the Claude type ("A real source's pair that misses stays exact … say so") keep brand values exact and flag misses. The skill designs the brand itself, so it can choose hexes that pass. The tension remains if a user supplies a fixed palette.
4. **Pure modular scales vs engineered scales.** Design writing often recommends a single ratio. All three systems measured deviate from one (§4).

**Gaps**
- **Not read directly:** the 2025.10 published spec pages (`designtokens.org`, `w3.org` blocked). Its stable status and date rest on search extracts. The `main`-branch text read from GitHub is a later draft.
- **Not read:** m3.material.io pages (blocked). Material facts come from the material-web token files and MDC-Android docs instead. Material 3 Expressive's shape library and spring tokens were seen only in MDC-Android's Motion doc.
- **Atlassian:** read only as compiled npm code (no design docs). It is clearly a brand-colour → roles algorithm, but the rationale is undocumented.
- **No primary source** gives a numeric mapping from brand personality to radius, density or motion. §6's right-hand column is a proposed method.
- **Only one documented brand-team case** of identity → product UI was found in primary form (GOV.UK v6 adopting brand guidelines v1.0). Carbon states its themes derive from the IBM Design Language palette but documents no method. The 2017 Atlassian and other rebrand stories were not reachable.
- **Claude type:** whether a non-`motion` family name holding durations would display is untested. The type was read, not exercised (no publish).
- **MCU version:** the run used npm 0.3.0. The repo is at 0.4.0, with 2025/2026 colour specs that may shift tones slightly.
