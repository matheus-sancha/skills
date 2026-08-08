# AUDIT — pass/fail checklist for a Flutter screen

Run this against a screen when building one ("is it done?") or when asked why one looks off. Report each item as **PASS / FAIL / N/A** with the offending file:line. The **Floor** section is hard: any FAIL there means the UI is not shippable, regardless of how it looks.

## Floor — accessibility & theming (hard, audit-failing)

- [ ] **Contrast meets WCAG AA.** Body/label text ≥ **4.5:1** against its background; large text (≥ 18.66 px bold / 24 px) and UI/graphical boundaries ≥ **3:1**. Check the actual `onX`-vs-`X` pairs in both themes.
- [ ] **Interactive targets are reachable.** Touch targets ≥ **48×48 dp** (wrap small icons in `IconButton`/`InkWell` with adequate constraints); pointer/keyboard controls have a visible **focus-visible** state, not ripple-only.
- [ ] **Icon-only controls are labelled.** Every icon button / gesture-only control has a `Semantics` label or `tooltip`. A screen reader must name every action.
- [ ] **Dark theme exists and derives from the same tokens.** Both `theme` and `darkTheme` are set, `themeMode: system`, and no hardcoded colours break in dark. Toggle and look.

## Tokens & consistency

- [ ] **No off-scale spacing.** Every gap/padding traces to `Space.*`. Grep for raw `SizedBox(height:`/`width:` and `EdgeInsets.*(` with literals not on the scale.
- [ ] **No ad-hoc radii.** All `BorderRadius`/`shape` values come from `Radii.*`; count the distinct radii on screen — more than the scale means drift.
- [ ] **No literal colours in widgets.** No `Color(0xFF...)` outside the token/theme files; widgets read `Theme.of(context).colorScheme` / semantic tokens.
- [ ] **No hardcoded `fontSize`.** Text uses `textTheme` roles; hierarchy from role + weight + colour.
- [ ] **≤ 2 font weights, ≤ 2 families.**

## Material 3 anti-defaults (see THEME.md §4)

- [ ] **Seed is not the default purple.**
- [ ] **Surfaces aren't tinted mud** — `scaffoldBackgroundColor` set; surface roles chosen deliberately.
- [ ] **No elevation soup** — separation via `outlineVariant` borders / flat surfaces; real shadow only for floating layers.
- [ ] **No over-rounding** — radii pulled to the scale, not the bubbly M3 defaults.

## Proportion & hierarchy

- [ ] **Generous, grouped whitespace** — related items close, groups separated; content doesn't touch edges.
- [ ] **Line length constrained** (~60–75ch for body).
- [ ] **Exactly one primary action** per screen; secondary actions are visually subordinate.
- [ ] **Layout reflows, not rescales,** across breakpoints.

## Navigation

- [ ] **Adaptive chrome** — `NavigationBar` < 600, `NavigationRail` 600–1240, extended rail/drawer > 1240 — with **stable destinations**.
- [ ] **Selected destination driven by the router** (`go_router` location), single source of truth.
- [ ] **Back/up behave correctly**; every screen is deep-linkable via a real route.

## App flow

- [ ] **All four async states present** — loading (shaped skeleton), empty (zero-state + action), error (plain language + retry), loaded.
- [ ] **Transitions consistent** — one duration/curve from `Motion.*`; motion signals relationship.
- [ ] **No dead-ends** — every action leads somewhere; destructive actions confirmed, reversible ones undoable.

---

**Reporting format:** a short table of the FAILs first (file:line + one-line fix), then a one-line "Floor: PASS/FAIL" verdict. Don't list every PASS — surface what to fix.
