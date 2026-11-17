# Claude's design capabilities: what the identity skill builds on, and what it must add

**Question.** Which of Claude's existing design capabilities should the brand-identity skill build on, and where must it add new ones? The inventory covers Artifacts and the Design / Design System artifact types; the `canvas-design`, `algorithmic-art`, `theme-factory`, `brand-guidelines`, `frontend-design`, `web-artifacts-builder` and `skill-creator` skills; the design plugin; the built-in `artifact-design` and `dataviz` skills; image viewing for self-critique; this repo's `flutter-ui-design`; and the better-known public logo and brand skills.

**Purpose.** Input to the spec for a Claude Agent Skill that designs brand identities and delivers an identity kit: concept rationale, SVG logo system, palette, type pairing, graphic language and brand sheet. It also delivers a UI design system derived from that kit, usable as a Claude Design System. Several decisions are binding:
- build on Claude's own capabilities before inventing anything;
- the spec may add scripts, references or companion skills where those capabilities fall short;
- drawing is **hybrid**: Python geometry primitives, composed by the agent;
- the quality gate is **render-then-rubric**.

This note is meant to settle four open questions: *delivery surface*, *new capabilities to create*, *skill anatomy*, and *the seam to flutter-ui-design*.

> **How these sources were read. Please read this first.**
> **Verified** means I read the file in this container or ran the thing. Every installed skill was read in full from the path cited. The synced copies of `canvas-design`, `algorithmic-art`, `theme-factory` and `brand-guidelines` match [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills) apart from line endings (checked with `diff` against `raw.githubusercontent.com`).
> The Design and Design System artifact types were inspected **read-only**. I used `Artifact` `list scope:"types"`, `read type_url`, `read` of the type's reference files by `path`, and one `quickstart`. Nothing was published, created or deleted.
> I also read the `project/README.md` and index of one existing Design System artifact in this account, as an observed example.
> The public logo skills were fetched from `raw.githubusercontent.com`. The GitHub API refused access to those repos, so their star counts and licences come from aggregator search snippets and are marked **(unverified)**.
> The `artifact-diagramming` skill was **not** loaded.
> Statements under "Implications" are my inference.

---

## 1. Answer

**Build on four things. The skill must add one thing that nothing covers: identity-mark construction and its checks.**

1. **The Design System artifact type is the delivery target for the UI half and the brand book.** It has an exact, documented file contract (§3.1): `README.md` as the brand book, a list-shaped `tokens.json` (colour themes, type, spacing, radius, shadow), components with live previews, an asset store for SVG logos, `fonts/`, and a generated cover. Other agents, including the Design canvas, already know how to read and install it. This account already holds a Design System artifact that carries a small identity: a mark, mono variants, a small-size variant, an app icon and usage rules. That is a precedent for the shape.
2. **Image viewing makes render-then-rubric possible.** In Claude Code a PNG written by a script can be viewed with `Read`. I verified this: a 256 px mark and a 16 px downsample were rendered and viewed, and the 16 px clog was visible (§4). Headless Chrome and PIL render SVG here. `rsvg`/`cairo` system libraries are present but Python bindings are not installed.
3. **The `frontend-design` and `artifact-design` anti-default lists, plus `canvas-design`'s two-step "philosophy → expression".** These are the best existing prompt technique for keeping concepts away from AI tropes. They should be borrowed and specialised, not duplicated.
4. **The design plugin's `design-critique`, `accessibility-review` and `design-system` skills, and the `dataviz` palette validator.** These are downstream checkers and documenters the skill should defer to. The Design System type's own craft rules (contrast in every theme, colour-blind-safe status colours) already encode most of the UI-side accessibility floor.

**Nothing existing covers the core of identity work.** None of the following is provided anywhere:
- a geometry library for marks;
- converting type to outlines for wordmarks;
- the mark-craft checks from [mark-craft.md](mark-craft.md);
- multi-size and mono render sheets;
- a palette builder that goes from an identity palette to a themed token set;
- a brand-sheet layout;
- an identity-to-Flutter token export.

Every public logo skill read (§5) generates SVG by hand-writing path data and does at most a structural check. None renders and looks.

### Capability table

| Capability | What it does (verified) | Good for identity work | Weak for identity work | How the skill invokes / composes | Borrow |
|---|---|---|---|---|---|
| **Design System artifact type** ([type](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd), release 1794863772-48f6) | Hosted, browsable design system. Files under `project/`: index, `tokens.json`, `README.md`, components, assets, fonts, cover | Final home for the tokens, logo assets and brand book. Other agents read it; a Design canvas installs it | No logo-construction view and no logo page. SVG is shown via `<img>` only, so no `currentColor` ([format.md](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd)). No motion family. Needs claude.ai artifact access | `Artifact publish type_url` → `url`, then publish files under `project/` with `root`. The index is written last (§3.1) | Cover recipe: blocks + one pattern + name, derived from tokens. "Usage note on every token". Contrast rules per theme |
| **Design artifact type** ([type](https://claude.ai/artifact/QKN21svewxgyPb6SYRqWnd), release 1794872754-7b8b) | Canvas of `.dc.html` artboards; installs a Design System | Brand-sheet and application mockups (cards, signage, app screens) as live artboards | Its SKILL.md says "**NEVER VERIFY UNLESS THE USER ASKED** … do not … render, screenshot". That conflicts with render-then-rubric *inside* the canvas | `type_url` create; `project/canvas.json` + one artboard per file; `designSystems` record | Application mockups as artboards. It ships a list of ~1,700 Google Fonts families (`google-fonts-families.json`) usable as the type-pairing whitelist |
| **Plain Artifact page** (`artifact-design` skill) | Single HTML page; CSP allows Google Fonts plus five script CDNs; light/dark tokens required | A portable brand sheet / presentation page | Not editable as a system; no token UI | `Artifact publish file_path` | Light/dark token block; "ground it in the subject"; AI-trope list |
| **canvas-design** ([GitHub](https://github.com/anthropics/skills/tree/main/skills/canvas-design); Apache-2.0; 81 files in `canvas-fonts/`, 27 OFL licences, ~29 families) | Writes a "design philosophy" .md, then a single-page PNG/PDF | Posters and brand-sheet compositions; the bundled OFL fonts are a ready type library | Art-first ("90% visual, 10% text"), no system thinking, no SVG, no checks. Prompt-only, no scripts | Defer to it for one-off brand posters; take fonts from its folder | Two steps: name a movement, then express it. The "refine, don't add" final pass |
| **algorithmic-art** ([GitHub](https://github.com/anthropics/skills/tree/main/skills/algorithmic-art); Apache-2.0) | p5.js seeded generative art; `templates/viewer.html` + `generator_template.js` | Generative graphic language (patterns, textures) | The template is locked to Anthropic branding (Poppins/Lora, `viewer.html` l.6, 26–46). Raster/canvas output, no SVG | Not composed directly; borrow its method | Seeded params; a "parameters emerge from the philosophy" table |
| **theme-factory** ([GitHub](https://github.com/anthropics/skills/tree/main/skills/theme-factory); Apache-2.0) | 10 preset themes, each 4 hex + header/body font; can generate a new theme | Applying a finished palette to decks and docs | Fonts are system fonts (DejaVu, FreeSans/FreeSerif in all 10). 4 colours, no roles, no contrast check | Downstream: hand it the identity's palette and fonts as a custom theme | Theme file shape (name, palette, fonts, "best used for") as a minimal export |
| **brand-guidelines** ([GitHub](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines); Apache-2.0) | Hard-codes **Anthropic's** colours and Poppins/Lora; python-pptx application | A worked example of a "brand applier" skill | Not a generator; Anthropic-only | None. Pattern only | Shape of a companion "apply-<brand>" skill the identity skill could *emit* |
| **frontend-design** (`/mnt/skills/public/frontend-design`; [GitHub](https://github.com/anthropics/skills/tree/main/skills/frontend-design); Apache-2.0) | Studio-lead stance; plan tokens → review against the brief → build → critique by screenshot | The strongest anti-template guidance; names five AI-default clusters, incl. cream + clay `#D97757` | UI pages, not marks | Defer for UI pages built *from* the identity | The AI-default calibration list; "spend boldness in one place"; plan review before build |
| **web-artifacts-builder** ([GitHub](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder); Apache-2.0; `init-artifact.sh`, `bundle-artifact.sh`, shadcn tarball) | React + Tailwind + shadcn bundled into one HTML file | Interactive brand explorer, if ever needed | Heavy; shadcn look | Optional | — |
| **skill-creator** (Anthropic, Apache-2.0; `scripts/run_eval.py`, `run_loop.py`, `package_skill.py`, `quick_validate.py`; plus this repo's own `skills/productivity/skill-creator`) | Authoring, evals, description tuning | Building and evaluating the new skill itself | — | Used at build time, not runtime | Eval loop for the rubric |
| **Design plugin** (Anthropic, v1.2.0; `…/plugins/synced/…/design`; upstream `anthropics/knowledge-work-plugins`, licence **(unverified)**) | Prompt-only skills: `design-system` (audit/document/extend), `design-critique`, `design-handoff`, `accessibility-review` (WCAG 2.1 AA), `ux-copy`; Figma MCP optional | Critique and audit *after* the identity exists; component documentation template | No scripts and no measurement: contrast is a checklist line, not a computation. Figma connector failed to connect here | Defer to it: `/design-critique` on the brand sheet render, `/accessibility-review` on the UI system, `/design-system document` for component READMEs | Component doc table (variants, states, a11y, do/don't) |
| **dataviz** (built-in; `scripts/validate_palette.js` + `.py`) | Runnable OKLab palette validator for **chart categorical** palettes: lightness band, chroma floor, CVD ΔE, contrast | Checking the *data-viz* extension of a brand palette; it exports `contrast()`/`apca()` | Scoped to chart palettes. Run on a neutral identity palette it FAILs "chroma floor" by design (§4) | Call for the chart palette the UI system ships; reuse its contrast functions | "The colour part is computable, so compute it" |
| **Image viewing** (`Read` on PNG) | The model sees rendered pixels | The render-then-rubric gate | Unverified in claude.ai chat/Cowork (§4) | Script renders sheet → `Read` → rubric | Sheet layout: large + 16 px upscaled side by side |
| **flutter-ui-design** ([SKILL.md](../../skills/engineering/flutter-ui-design/SKILL.md), this repo) | Tokens → `ThemeData`; Material 3 anti-defaults; audit checklist | Consumer of the identity's tokens on Flutter | Colour comes from **one seed** through `ColorScheme.fromSeed` ([THEME.md §2](../../skills/engineering/flutter-ui-design/references/THEME.md)), which regenerates tones and won't keep exact brand hexes. Max 2 weights | Seam: identity skill emits tokens; flutter-ui-design consumes them (§6) | Its scales (spacing 4–64, radius 4–16, motion 100/200/300 ms) as defaults the UI system may map to |

---

## 2. The installed skills, one by one

### 2.1 canvas-design, algorithmic-art: philosophy-then-expression

Both skills share one method ([canvas-design SKILL.md](https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md); [algorithmic-art SKILL.md](https://github.com/anthropics/skills/blob/main/skills/algorithmic-art/SKILL.md)):
- name a 1–2-word "movement";
- write 4–6 paragraphs of philosophy;
- deduce a "subtle reference" from the request;
- express it in code;
- then do a refinement pass that forbids adding elements ("If the instinct is to call a new function or draw a new shape, STOP").

`canvas-design` outputs only `.md`, `.pdf` and `.png`. It has no scripts, just a `canvas-fonts/` folder of 81 files with OFL licence texts (verified by listing). `algorithmic-art` ships a p5.js viewer template that is explicitly fixed to "Anthropic branding (colors, fonts, layout)" (`templates/viewer.html` line 6).

*For identity work:* the method maps well onto the brief-to-concept "big idea" step ([brief-to-concept.md §1](brief-to-concept.md)), but it is tuned for art, not for marks that must survive 16 px and one colour. Neither skill has a check of any kind.

### 2.2 theme-factory and brand-guidelines: appliers, not generators

`theme-factory` holds 10 theme files of 4 hexes plus header and body fonts. All of them use DejaVu or FreeSans/FreeSerif (counted with `grep`). "Create your own theme" is one paragraph with no contrast check ([SKILL.md](https://github.com/anthropics/skills/blob/main/skills/theme-factory/SKILL.md)).

`brand-guidelines` is Anthropic's own palette (`#141413`, `#faf9f5`, `#d97757` …) with Poppins/Lora, applied through python-pptx ([SKILL.md](https://github.com/anthropics/skills/blob/main/skills/brand-guidelines/SKILL.md)).

*Use:* downstream appliers of a finished identity. `brand-guidelines` is the template for an optional emitted "apply-this-brand" skill.

### 2.3 frontend-design and artifact-design: anti-default discipline

[`frontend-design`](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) (verified at `/mnt/skills/public/frontend-design/SKILL.md`) lists five clusters that AI design converges on. It specifically names "a warm cream background (near #F4F1EA) … terracotta or warm-clay accent (often near #D97757 — Anthropic's own …)". It requires a token plan (4–6 named hex, type roles, layout, principles) that is reviewed against the brief *before* building, then critiqued by screenshot.

`artifact-design` (built-in; loaded via the Skill tool, no file on disk found) repeats the trope list and adds the Artifact page contract:
- the CSP: Google Fonts is the only stylesheet host, plus five script CDNs;
- light and dark tokens, with a guarded `prefers-color-scheme` block;
- a 16 px gutter.

*Use:* the identity skill's concept-review step should run the same "would a generic brief land here?" test on each route. It should also include these clusters in its rubric as "default, not choice".

### 2.4 Design plugin: critique and documentation, no measurement

All six skills under `…/plugins/synced/…/design/skills/` are prompt-only Markdown, with no scripts. The `.mcp.json` lists Figma, Slack, Linear, Notion and others.
- `design-critique` covers first impression, usability, hierarchy, consistency and accessibility.
- `accessibility-review` is a WCAG 2.1 AA quick reference (1.4.3 at 4.5:1, 1.4.11 at 3:1, 2.5.5 at 44 px).
- `design-system` has audit, document and extend templates.

The plugin README says it is "primarily designed for Cowork" and installs from `anthropics/knowledge-work-plugins`.

*Use:* defer critique wording and component documentation to it; do not re-author them. Its contrast check is a checklist line, so numeric contrast must come from a script (ours, or dataviz's `contrast()`).

### 2.5 dataviz validator

`node scripts/validate_palette.js "<hex,…>" --mode light` ran here. On a neutral five-grey identity palette (`#0F1113,#3A4A5A,#9AA3AD`) it reported:
- FAIL on lightness band and chroma floor ("reads gray");
- PASS on CVD separation (ΔE 22.5) and normal-vision separation;
- WARN on contrast (2.49:1 for `#9AA3AD`).

The script states its own scope: "categorical palettes only. For a lone status/text color check text contrast with this script's apca() or contrast()". So it is the right tool for the UI system's **chart palette** and a usable contrast function. It is the wrong gate for the identity palette itself.

### 2.6 flutter-ui-design (this repo)

[SKILL.md](../../skills/engineering/flutter-ui-design/SKILL.md) makes tokens the source of truth: spacing `4·8·12·16·24·32·48·64`, radius `4·8·12·16·full`, ~1.2 type ratio, max 2 weights, motion `100·200·300 ms`, and "one seed (not default purple)". It says "if the project already has a brand, adopt its tokens but keep the systematic discipline".

[THEME.md](../../skills/engineering/flutter-ui-design/references/THEME.md) builds colour with `ColorScheme.fromSeed(seedColor: _seed)`. [AUDIT.md](../../skills/engineering/flutter-ui-design/references/AUDIT.md) holds the hard floor: 4.5:1, 48 dp targets, a dark theme from the same tokens.

---

## 3. Artifact types

`Artifact list scope:"types"` returned 7 core types: Data, Design, Design System, Docs, Sheets, Slides and Whiteboard. `quickstart intent:"design"` returned the Design type plus this account's two Design System artifacts. Neither is marked default, so a design run must ask which system to use, or build without one.

### 3.1 Design System type: the exact input contract

Source: the type's `SKILL.md` and `artifact-type/reference/format.md`, `craft.md` and `cover.md`, read from [the type](https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd). Contract version `"0.2.47"`. Capabilities inherited: artifact, assets, comments, db, downloads, room, user.

**Creation.** One `publish` with `type_url` and a required `title`, and no files. Every later write goes to the returned `url`, and only under `project/`. Everything else belongs to the type and is refused.

**Files under `project/`:**

| Path | Content | Rules / caps |
|---|---|---|
| `design-system.json` | The index: `{"v":3,"layout":"files","createdOnFiles":{"v":1,"at":<ISO now>},"title","namespace","libraries":[],"sections":{},"groups":[…],"assetGroups":{<Group>:{"name","tile":"l".."xs","order":[…],"files":{<name>:{"name","blob","size","type"}}}},"blobs":{},"docs":{"sections":[]},"lastChange":{"by","at","via","note"}}` | Written **last**, once per change; re-read right before writing. `title` is the system's name |
| `tokens.json` | Tokens, always written whole | ≤512 KB; shape below |
| `README.md` (+ up to 24 further `*.md` sections) | The brand book: usage rules naming tokens, voice, visual foundations, iconography | ≤200 KB; no title, no provenance; required in every system |
| `components/<Comp>/README.md`, `components/<Comp>/preview.html` | Guidelines; live preview whose line 1 is `<!-- @dsCard group="…" height=N -->` | Preview ≤256 KB; preloaded tokens.css, fonts, bundle.css, bundle.js; no iframes; CDN URLs pinned |
| `components/bundle.js`, `bundle.css`, `index.d.ts`, `lib/*.js` | One classic script setting `window.<namespace>`; React 18 from jsDelivr unless shipped in `lib/` | bundle ≤6 MB; no `import`, no network, no literal `</script` |
| `components/Cover/preview.html` | The cover, written last: colour blocks cut from the scales, one pattern, the name ≤120 px bottom-left, at 960 × 240–360 | Folder kept bare (a README there makes it a component). A derivation comment is required |
| `assets/<Group>/<file>` | Logos, icons and images, **uploaded** to the asset store (`publish asset:true` → `/_blob/<id>`) and recorded in the index's `assetGroups`. A group's `README.md` is a plain file | Upload ≤20 MB, SVG ≤2 MB. Shown via `<img>` only, so no `currentColor`; name a single-ink mark's ink in the group README |
| `fonts/<file>` | woff2/woff/ttf/otf, listed in `tokens.json` `type.fonts[].file` | A Google-hosted face has no file and is named only in `type.families` |
| `tokens.css`, `manifest.json`, `api/…` | **Generated by the page**; never written (except a first `tokens.css` in a clean-up) | — |

**`tokens.json` grammar.**
- `{"name","version","color":{"themes":[{"id","name"}…],"tokens":[{"name","value":{"<themeId>":…}|"…","usage"}]},"type":{"fonts":[{"family","file","weight","style"}],"families":{"<key>":"<css stack>"},"groups":[{"name","family","styles":[{"name","fontSize","lineHeight","fontWeight","letterSpacing"?,"sample"?,"usage"?}]}]},"spacing":{"tokens":[…]},"radius":{"tokens":[…]}}`.
- Optional: `shadow`, plus up to 12 other `{tokens:[…]}` families. There is **no motion family**.
- Every family except `type` is a **list**. DTCG name-to-value maps are valid JSON that the page shows as empty.
- Names match `[A-Za-z0-9][A-Za-z0-9_.-]{0,63}` and must be unique across families.
- Colour values: hex, `rgb()`, `hsl()`, `oklch()`, `lab()` and similar with numeric arguments, or an alias `"{token}"`. No `var()`, `color-mix()` or named colours.
- A theme missing a value inherits the first theme's value.
- Caps: ≤8 themes, ≤600 colours, ≤12 type groups / ≤80 styles, ≤60 tokens per other family.

**Craft rules the type enforces in prose.** From `craft.md` and the SKILL checklist:
- a usage note on every token, and a README per asset group;
- text contrast ≥4.5:1 (3:1 at 24 px+, borders, focus rings, icons) **in every theme**;
- status colours differ in lightness, not hue alone;
- "Assets are copied, never approximated". This targets reproducing *existing* brands and does not block designing a new one;
- with no source, make a SMALL first system (6–10 colours, 5–7 text styles, 4 spacing steps, 3 radii) and say so;
- no AI tropes.

**Observed example.** This account's existing Design System artifact contains:
- an index whose `assetGroups.Logos` lists seven SVG uploads (primary mark, on-dark, two mono, two small-size variants, app icon);
- a README with sections *The mark*, *Logo files* (a table of file → use), *Using the logo* (lockups, clear space, minimum size, grounds, don'ts), *Colour*, *Type*, *Shape and spacing*.

An identity kit fits the type without strain. The logo-system rules from [mark-craft.md](mark-craft.md) (clear space in mark units, minimum size, small-size master) go into README prose.

### 3.2 Design type

From [the type's SKILL.md](https://claude.ai/artifact/QKN21svewxgyPb6SYRqWnd):
- Canvases hold `project/canvas.json` (boards with x/y/w/h, order, pages, notes, `designSystems`) and one self-contained `.dc.html` per artboard. Each artboard has the `support.js` head line, `<x-dc>` markup, and a `DCLogic` script with `data-props` tweaks.
- A design system is "installed" by copying its `tokens.json` to `project/ds/<folder>/tokens.json` and adding a `designSystems` record.
- Its craft defaults are: "No design system? … Inter, Space Grotesk headings"; touch targets ≥44 px; text 4.5:1.
- It explicitly forbids self-verification: "**NEVER VERIFY UNLESS THE USER ASKED** … Do NOT … render, screenshot or open it".
- Its references include `brand-colors.md`, `brand-typography.md`, `google-fonts-families.json` (a list of Google Fonts family names) and `google-fonts-reserved.json`. The reserved file is sourced from `github.com/google/fonts at 5174b33`; I infer it lists families with OFL Reserved Font Names, which matters when subsetting or outlining **(unverified)**.

---

## 4. Image viewing: the render-then-rubric gate

**Verified here (Claude Code, Linux container):**
- A 64-unit SVG mark was rendered to PNG with headless Chrome (`google-chrome --headless=new --screenshot`).
- It was downsampled to 16 px with PIL and pasted beside the large render. `Read` on the sheet PNG showed both images.
- The view was good enough to see that the vertical bar merges into the ring at 16 px. That is the kind of failure the mark-craft rubric asks the model to catch (rules 14–15).

**What renders:**
- PIL 12.3, NumPy and reportlab are installed.
- ImageMagick `convert` has **no SVG delegate**: it failed.
- `librsvg-2` and `libcairo` are present as system libraries, but `cairosvg`, `skia`, `fontTools`, `shapely` and `svgpathtools` are not installed. All are downloadable from PyPI here (`pip download cairosvg` succeeded; `pip index` lists `skia-python 144.1` and `fonttools 4.68.0`).

**claude.ai / Cowork (unverified).** Anthropic's [code execution tool docs](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/code-execution-tool) describe a sandboxed container that accepts image inputs and returns file outputs. I found no Anthropic page that states whether the model can *view* a PNG it wrote itself in claude.ai or Cowork, or what renderers those containers ship. Treat the gate as verified for Claude Code only. Two consequences:
- the skill should declare its render dependency and fall back gracefully;
- the Design type's NEVER-VERIFY rule means the gate must run **before** content is pushed to a canvas, on local renders, not on the artifact.

---

## 5. Public logo and brand skills

| Skill | What it does | Read? | Technique worth borrowing | Weakness |
|---|---|---|---|---|
| [rampstackco/claude-skills `brand-identity`](https://github.com/rampstackco/claude-skills/blob/main/skills/brand-identity/SKILL.md) (MIT, ~500★ per [tessl/skills.sh](https://skills.sh/rampstackco/claude-skills/brand-identity) **(unverified)**) | A 5-element framework: logo system (primary, wordmark, symbol, lockups, monogram), colour, type, imagery, motion | SKILL.md read | Explicit "logo system, not a logo" component list. "Common failure: designing only the primary mark". Per-colour documentation (hex/RGB/HSL/CMYK, contrast, allowed pairings). Routes to sibling skills (`brand-ideation`, `brand-style-guide`, `brand-voice`) | Prose only; no drawing, rendering or checks |
| [luongnv89/skills `logo-designer`](https://github.com/luongnv89/skills/blob/main/skills/logo-designer/SKILL.md) (`license: MIT` in frontmatter) | 7 SVG variants + `brand-showcase.html`, through brand-researcher → svg-generator → svg-reviewer subagents | SKILL.md read | **The canonical mark first, then every variant derived from its literal `d=""` strings, read back and compared**. Previews on light and dark. A favicon "simplified 2-layer mark" | Hard-coded default style ("dark base + neon-green"), which is exactly an AI-default cluster. The reviewer checks structure (viewBox, no raster), not appearance |
| [rknall/claude-skills `svg-logo-designer`](https://github.com/rknall/claude-skills/blob/main/svg-logo-designer/SKILL.md) | Requirements → 3–5 concepts → 5 layouts (horizontal, vertical, square, icon, text) → SVG → usage guidelines | SKILL.md read | Layout matrix per concept. `<title>/<desc>` accessibility in SVG. Colour classes in `<defs><style>` | Wordmarks as `<text>` with font-family (not outlined). PNG export via `inkscape`/`convert`, which is absent or broken here. No render review |
| seb1n/awesome-ai-agent-skills `logo-design`; b1rdmania/claude-brand-skills; Im5tu `brand-design`; travisjneuman `brand-identity` | Listed by aggregators ([skillselion](https://skillselion.com/skills/seb1n/awesome-ai-agent-skills/logo-design), [typingmind](https://www.typingmind.com/skills/b1rdmania-brand), [agent-skills.md](https://agent-skills.md/skills/Im5tu/claude/brand-design)) | **Not read**: raw paths 404'd and the API was refused | — | — |

**Finding.** No public skill found builds marks from geometry primitives, renders at multiple sizes, or looks at the result. The Anthropic Design System demo's own `ember-wordmark.svg` is also a live `<text>` element, not outlines (`artifact-type/demo.json`).

---

## 6. Implications for the skill (inference: my reasoning, not sourced)

**Delivery surface: deliver on three tiers, with plain files as the source of truth.**
1. **Plain files** (always), the canonical kit:
   - `identity/` holding the SVG masters (outlined) and every variant;
   - render sheets (PNG);
   - `tokens.json` in the Design System list grammar;
   - `README.md` brand book;
   - `rationale.md`;
   - the brand-sheet HTML.

   This works in every surface and is what the rubric gates.
2. **Claude Design System artifact** (when the Artifact tool is present): the same `tokens.json` and README, logos uploaded to `assets/Logos/`, Google or OFL fonts in `fonts/`, and a cover generated per `cover.md`. The UI design system lives here.
3. **Optional Design canvas** for application mockups, which installs the system. Run no rubric inside it, because of its NEVER-VERIFY rule.

A plain published page is a fallback brand sheet only.

**New capabilities to create (scripts and references):**
- `geometry` primitives (per [mark-craft.md §10](mark-craft.md)), emitting SVG with a construction log.
- `outline_text`: wordmark to paths via fontTools, with kerning and optical spacing hooks. It also resolves the `<text>` problem.
- `render_sheet`: SVG to PNG at 16/32/48/256 px, mono, reversed, on light and dark. Chrome-headless or cairosvg/resvg backend with a declared fallback.
- `check_mark`: the script half of the mark-craft rules.
- `palette`: identity palette to themed colour tokens in OKLCH, with `on-*` pairs, contrast per theme, and status colours separated by lightness. Reuse dataviz `contrast()`/`apca()` or port it.
- `emit_tokens`: write the Design System `tokens.json` lists, with usage notes. Optionally also emit DTCG and a Flutter `tokens.dart`.
- `brand_sheet`: layout template, plus a cover generator following `cover.md`.
- References: the rubric, the logo-system inventory (the rampstack list plus mark-craft size and clear-space rules), and the concept method from [brief-to-concept.md](brief-to-concept.md).

**Defer instead of duplicating:**

| Task | Defer to |
|---|---|
| Critique wording | `design:design-critique` |
| WCAG audit of UI screens | `design:accessibility-review` |
| Component READMEs and variant tables | `design:design-system document` |
| UI pages built from the identity | `frontend-design` / `artifact-design` |
| Deck or doc theming | `theme-factory` (pass a custom theme) |
| Posters | `canvas-design` |
| Generative patterns | `algorithmic-art`'s method (not its template) |
| Chart palettes | `dataviz` |
| Flutter theming | `flutter-ui-design` |

**Skill anatomy (suggested).**
- One skill with phases: brief → routes → draw → render/rubric → system → deliver. It has `scripts/` for the pieces listed above and `references/` (rubric, logo-system inventory, Design System contract, cover recipe).
- Use subagents only where `logo-designer` shows they pay off: SVG generation is the big context cost.
- The derive-variants-from-canonical-paths rule belongs in the drawing step.

**Seam to flutter-ui-design.**
- The identity skill emits tokens, including a Dart token file or a mapping onto flutter-ui-design's `Space`/`Radii`/`Motion` names.
- flutter-ui-design consumes them under its "adopt its tokens" clause.
- **Conflict:** `ColorScheme.fromSeed` will not reproduce exact brand hexes. Either the seam supplies a full explicit `ColorScheme` (or `fromSeed(...).copyWith(...)` for brand roles), or flutter-ui-design gains a "brand-supplied scheme" branch.
- The "max 2 weights" rule may also clash with a wordmark's weight contrast. That clash affects UI text only and should be stated at the seam.

---

## 7. Open disagreements and gaps

**Disagreements**
1. **Verify or not.**
   - `frontend-design` says critique your own work "taking screenshots".
   - `artifact-design` allows one look before publishing.
   - `dataviz` says "Render it and look at it".
   - The Design type says NEVER verify unless asked.

   The binding render-then-rubric decision sides with the first three. The spec must confine rendering to local files.
2. **`currentColor` in logos.** The Design System `format.md` says pictures show "only via `<img>` (no scripts; no `currentColor`)". The type's own demo logo uses `fill="currentColor"`. Ship explicit-ink variants (dark, light, mono), as the observed example does.
3. **Seed vs exact palette** (flutter-ui-design `fromSeed` vs identity hexes): see §6.

**Gaps**
- Image viewing and the renderers available in claude.ai and Cowork containers are **unverified**.
- The design plugin's licence and upstream path are unverified: no LICENSE file in the synced copy.
- `artifact-diagramming` was not read.
- seb1n, b1rdmania and other aggregator-listed skills were not read.
- The meaning of `google-fonts-reserved.json` is inferred.
- Whether a Design System cover or README may embed the logo (the cover rules say "no images") is a constraint, not a gap. The logo lives in `assets/Logos` and the brand book, not the cover.
