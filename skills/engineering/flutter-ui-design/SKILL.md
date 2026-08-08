---
name: flutter-ui-design
description: Design and audit beautiful, adaptive UI for Flutter apps — design tokens, Material 3 anti-defaults, proportion/type/color scales, adaptive navigation, and app flow. Use when building or theming Flutter screens, setting up ThemeData/ColorScheme, deciding navigation or layout, or reviewing a Flutter UI that looks off ("make this prettier", "fix the theme", "why does this feel cluttered"). For app architecture, data flow, and packaging, use flutter-desktop-app instead.
---

# Flutter UI Design

The presentation-layer companion to `flutter-desktop-app`. That skill owns **where widgets live and how data flows**; this one owns **how they look and feel**. Reach for it while building a screen, while wiring `ThemeData`, while choosing navigation — and to audit a screen that looks off.

The default aesthetic is **calm, minimal, content-first**: generous whitespace, one accent over neutrals, few weights, low chrome, motion that earns its place. This is the house default, not a mandate — if the project already has a brand, adopt its tokens but keep the systematic discipline below. What is *not* negotiable is the accessibility floor (see `references/AUDIT.md`).

Rules are paraphrased from three authorities and credited where a rule derives from one: the **Material 3** spec (component behaviour, state layers, elevation, motion), **Refactoring UI** by Wathan & Schoger (proportion, scales, hierarchy, semantic colour), and **Apple's HIG** (cross-platform navigation and gesture expectation). Concrete numbers below are this skill's own, chosen to embody those ideas.

## The one rule everything else serves

**Systematise the choice, then never choose ad hoc again.** Beauty in a UI is overwhelmingly consistency, not flourish. Every value a widget uses — a gap, a radius, a colour, a duration — comes from a small, named scale defined once. A `SizedBox(height: 13)` or a one-off `Color(0xFF...)` in a widget is the bug this skill exists to prevent. If a value isn't on a scale, either it's wrong or the scale is missing one step; fix the scale, not the widget.

## Design tokens are the source of truth

Define tokens **once**, in plain Dart, and feed them into `ThemeData`. The widget tree reads the theme, never raw numbers. Both light and dark themes derive from the **same** token set — if they can't, the tokens aren't real yet.

The default scales (all overridable; each maps to a Material 3 role):

| Token | Scale | Note |
|---|---|---|
| **Spacing** | `4 · 8 · 12 · 16 · 24 · 32 · 48 · 64` | 8-dp rhythm; 4 for tight pairs. Nothing off-ramp. |
| **Radius** | `4 · 8 · 12 · 16 · full` | One family. Pick per component role, not per whim. |
| **Type** | ~1.2 ratio onto M3 roles (display → label) | Max **2** weights. Hierarchy from size + weight + colour, not from many fonts. |
| **Motion** | `100 · 200 · 300 ms`, emphasized easing | Enter/exit only where it clarifies. No decorative animation. |
| **Colour** | one seed (**not** default purple) + neutral surfaces + semantic success/warning/error | Both themes from this one seed. |

`references/THEME.md` turns these into a working `ThemeData`/`ColorScheme` and lists the Material 3 anti-defaults that separate a beautiful Flutter app from a stock demo.

## Dependencies

Endorsed: **`go_router`** for navigation (matches `flutter-desktop-app`, so the two skills compose on a real project), and optionally **`google_fonts`** for the type ramp. Everything else — the `ColorScheme`, tokens, components — is hand-rolled, on purpose: the skill teaches understanding your own theme, not outsourcing it to `flex_color_scheme`. Examples stay valid on a no-package project.

## When to read what

| Occasion | Read |
|---|---|
| Setting up `ThemeData`/`ColorScheme`, fixing the stock-M3 look, choosing colours/type/motion | [THEME.md](references/THEME.md) |
| Proportions & spacing rhythm, layout grids, **navigation** patterns, **app flow** and screen states | [STRUCTURE.md](references/STRUCTURE.md) |
| Reviewing a screen — the pass/fail checklist, including the hard accessibility floor | [AUDIT.md](references/AUDIT.md) |

When creating or restyling a screen, read `THEME.md` and `STRUCTURE.md` first, build against the tokens, then run yourself against `AUDIT.md` before calling it done.
