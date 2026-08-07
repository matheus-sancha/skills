# Wayfinder — map and ticket formats

## The map body

The whole map at low resolution, loaded once per session. Open tickets are
**not** listed — they are open sub-issues, found by the frontier query in
[GITHUB.md](GITHUB.md).

```markdown
## Destination

<what reaching the end of this map looks like — the spec, decision, or change
this effort is finding its way to. One or two lines; every session orients to
it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this
effort. Say so here if this effort overrides "plan, don't do" and carries
execution into the map.>

## Decisions so far

<!-- the index — one line per closed ticket: enough to judge relevance, then
     zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link) — <one-line gist of the answer>

## Not yet specified

<!-- in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- work ruled beyond the destination; closed, never graduates -->

- [<closed ticket title>](link) — <gist> — out of scope because <why>
```

## The ticket body

Sized to one 100K token agent session. The body is the question and nothing
else — the answer arrives later as a resolution comment.

```markdown
## Question

<the decision or investigation this ticket resolves>
```

## The resolution comment

Posted when the ticket is resolved, immediately before closing it.

```markdown
## Answer

<the decision, stated so a later session can act on it without re-deriving it>

## Assets

<links to anything created while resolving — research notes, prototypes.
Omit the heading if there are none.>
```

Then append one line to the map's **Decisions so far**, gisting this answer and
linking the ticket by name. The full detail stays here, in the ticket — the map
never restates it.

## Titles

The title is the **name** the human reads everywhere, so make it carry meaning
on its own:

- **Map** — shaped like its destination: "Spec for offline sync", "Pick the
  auth model".
- **Ticket** — shaped like its question: "Which store owns draft state?", not
  "Investigate state" or "Task 3".
