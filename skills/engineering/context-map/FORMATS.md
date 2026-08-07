# Context map — formats

## CONTEXT.md

Lives at the repo root. Read at the start of a session, so it earns its length
in navigation saved. If it stops being readable in a couple of minutes, it has
started competing with the code it was meant to summarise.

```markdown
# Context

<One paragraph: what this system is and who uses it. Not the pitch — the shape.>

## Entry points

<Every way the system gets invoked: binaries, routes, jobs, CLI commands.
Path + one line each.>

## Modules

<Per module: responsibility, interface, dependencies. Use codebase-design's
vocabulary. Point at the directory; don't list its files.>

- **<name>** (`path/`) — <what it's responsible for>. Interface: <what callers
  must know>. Depends on: <modules>.

## Domain

<The model from /domain-modeling: the concepts, their invariants, and the one
name each goes by. Or a link, if it lives in its own file.>

## Load-bearing

<Deliberate choices that will break things if changed, and what breaks. This
section is why the file exists — it cannot be derived from the code.>

## Incidental

<Things that look deliberate but aren't: history, accidents, known warts.
Tells a reader what they may freely fix.>

## Decisions

<Links to ADRs. One line of gist each, no summaries.>
```

## ADRs

One file per decision, numbered and never renumbered. `docs/adr/NNNN-slug.md`,
or wherever the repo already keeps them.

```markdown
# NNNN. <decision, stated as the thing chosen>

- **Status**: accepted | superseded by [NNNN](./NNNN-slug.md)
- **Date**: YYYY-MM-DD

## Context

<The forces in play when the decision was made. What made this a real question
rather than an obvious call. Written so it still reads as a genuine dilemma
years later.>

## Decision

<What was chosen, in the active voice: "We use X.">

## Alternatives considered

<Each option seriously weighed, and why it lost. An ADR without this is a note,
not a record — the next reader's first instinct will be the rejected option.>

## Consequences

<What this buys, and what it costs. Include the costs, especially the ones
that only show up later. Both halves, always.>
```

### Status

`accepted` on writing. When a later ADR reverses it, set this one to
`superseded by`, link the new one, and change nothing else — the record is the
trail, and editing the original destroys it.
