# STRUCTURE — proportions, navigation, and app flow

The three things that make an app *feel* designed rather than assembled. Read this when laying out a screen, choosing how the user moves between screens, or designing a flow.

---

## Part 1 — Proportions

Refactoring UI's core lesson: **don't eyeball, choose from a scale.** Every gap and size below comes from the spacing scale in `THEME.md` (`Space.*`).

### Rhythm

- **One spacing scale, everywhere.** Padding, gaps, margins all draw from `Space`. A `13`, a `15`, a `22` is always a mistake.
- **Space is hierarchy.** Group related things with less space, separate groups with more. Whitespace does the work a divider line often shouldn't. Prefer more breathing room than feels necessary — cramped is the common agent failure.
- **Pad from the inside out.** Container padding ≥ the gaps between its children, so content never touches an edge.

### Sizing & the grid

- **Constrain line length.** Body text wraps at ~`60–75ch`; use `ConstrainedBox(maxWidth: ...)` — full-width paragraphs on desktop are unreadable.
- **Columns, not pixels.** Lay screens on a column grid (`Wrap`, `GridView`, or a flex row of `Expanded`s). Gutters come from `Space`.
- **Size by role, not by fitting.** Touch targets ≥ 48 dp (see AUDIT). Icons from a small set (`16 · 20 · 24`). Don't shrink a control to fit a cramped layout — fix the layout.

### Hierarchy

- **Emphasise by de-emphasising.** One primary action per screen (a single `FilledButton`); everything else is `Outlined`/`Text`. Two competing primaries means neither reads as primary.
- **Weight and colour before size.** Secondary text is `onSurfaceVariant`, not merely smaller. Reserve large sizes for genuine headings.

### Density across breakpoints

Reflow, don't rescale. As width grows, add columns and whitespace rather than stretching a phone layout. Desktop may step `VisualDensity` up to `.comfortable`; touch stays `.standard`.

---

## Part 2 — Navigation

Navigation is **adaptive by breakpoint** — same destinations, different chrome. Drive it off `LayoutBuilder`/`MediaQuery` width, and route with `go_router`.

| Width | Pattern | Notes |
|---|---|---|
| **< 600 (compact / phone)** | `NavigationBar` (bottom) | 3–5 top destinations; thumb-reachable. Overflow → a "More" route, not a hamburger if avoidable. |
| **600–1240 (medium / tablet, small desktop)** | `NavigationRail` | Icons + short labels at the side; frees vertical space. |
| **> 1240 (expanded / desktop)** | Extended `NavigationRail` or persistent drawer | Labels always visible; supports denser info. Matches `flutter-desktop-app`'s home surface. |

Rules:

- **Destinations are stable across breakpoints.** Only the chrome changes; a user's mental model of "where things are" must not shift when the window resizes.
- **One source of truth for the current destination.** `go_router`'s location drives the selected index in *every* variant — never track it separately per widget.
- **Respect back/up.** Back reverses navigation history; up goes to the parent in the hierarchy. On desktop and web, the browser/OS back must work — use real routes, not `setState` page-swapping.
- **Deep-link everything.** Every screen has a URL/route. No screen reachable only by tapping through — this is what makes back, refresh, and restore work.
- **Don't nest bottom nav inside bottom nav.** One primary navigator; secondary navigation within a destination uses tabs or in-page routes.

---

## Part 3 — App flow

Flow is the connective tissue between screens. The house rule: **never dead-end the user, and never show a blank while thinking.**

### Every async surface has four states

A screen or widget that loads data must design all four — a missing state is a bug, not an edge case:

1. **Loading** — a skeleton/placeholder shaped like the eventual content, not a bare centred spinner where layout will later jump.
2. **Empty** — an explicit, friendly zero-state with the primary action to fill it ("No entries yet — add your first"). Never an empty list with no explanation.
3. **Error** — plain-language cause + a retry affordance. Never a raw exception or a silent blank.
4. **Loaded** — the content.

### Transitions

- **Motion signals relationship.** Use a shared-axis / fade-through transition (`Motion.base`, `Motion.curve`) so forward/back and sibling/parent moves read correctly. Reserve hero/shared-element motion for a genuine continuation of the same object.
- **Transitions are quick and consistent.** All page transitions use the same duration and curve from `THEME.md`. A slow or bespoke-per-screen transition draws attention to itself.

### Progressive disclosure & journeys

- **Show what's needed now.** Reveal advanced options on demand (expanders, secondary screens) rather than a wall of controls up front.
- **Onboarding earns its keep or is cut.** If present, ≤ 3 screens, each with a skip; get to the app's value fast. Don't gate first use behind a tour.
- **Confirm the destructive, undo the rest.** Irreversible actions get a confirm; everything else prefers an undoable `SnackBar` over a modal.
- **Close every loop.** A submit leads somewhere — a success state, the updated list, a next step. An action that appears to do nothing is the worst flow bug.
