# Stage 1: Brief

Goal: a typed brief the user signs off, plus a one-line big idea. Visual questions are **not** asked here; colour, shape and style come at Territory as reaction boards.

## Rules

- One question per message. Each question carries a **proposed answer** drawn from what you already know; the user accepts or edits it.
- Never block. If an answer is still thin after one follow-up, write your best assumption into the field, add the field name to `assumed`, and move on. List every assumed field at sign-off.
- If the user has a brief, deck or notes, map them onto the schema first and ask only for empty fields.

## Rounds

**0. Intake.** "Do you have a brief, deck or notes I should start from?"

**1. Strategy**
1. Name, and what the organisation does, in one line.
2. Who it is for: a primary audience and an optional secondary one.
3. Three to five competitors or peers (names, URLs or images). These feed Audit.
4. Why someone picks it over them (positioning).
5. Three values, ranked.

**2. Voice**
1. Five sliders, 1–5 (from the GV Three-Hour Brand Sprint): Friend ↔ Authority, Playful ↔ Serious, Classic ↔ Modern, Mass ↔ Elite, Quiet ↔ Loud. Use a multiple-choice question tool when one exists.
2. Three to five attribute words.
3. One sentence a customer would say about it.

**3. Constraints**
- Where the identity will live: app, web, signage, print, merch, social.
- What must stay: name, a colour, an existing mark.
- Sub-brands.
- Is accessibility a priority? (`true` switches on the AAA high-contrast themes at System.)

## Then draft

- **Big idea:** one line every visual decision can trace back to.
- **Mark-type hints** (Haviv's rule: a symbol needs a reason). A long name, many sub-brands or an audience that needs an icon justifies a symbol; otherwise lean on a wordmark or letterform.

Show the brief and ask for sign-off. This is the Brief checkpoint; the brief stays reopenable if a route later finds a better idea.

## `01-brief.md` format

```markdown
---
name: Linnet
one_liner: A family-run café for cyclists on the coast road.
audiences: {primary: "...", secondary: "..."}
competitors: ["...", "..."]
positioning: "..."
values: ["...", "...", "..."]          # ranked
sliders: {friend_authority: 2, playful_serious: 2, classic_modern: 3, mass_elite: 2, quiet_loud: 4}
attributes: ["warm", "quick", "local"]
customer_line: "..."
applications: [web, signage, merch]
must_keep: []
sub_brands: []
accessibility_priority: false
big_idea: "..."
mark_type_hints: [pictorial, wordmark]
assumed: []
territory: {}                           # filled at Stage 3
---

(The same content as readable prose.)
```

## Bring your own mark

Short brief only: name, one-liner, audiences, values, sliders and constraints. Skip competitors and the big idea unless the user wants them.
