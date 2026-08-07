---
name: context-map
description: Create and maintain a repo's CONTEXT.md — the mental model an agent reads before touching the code — and its ADRs, the record of why each load-bearing decision was made. Use when onboarding to an unfamiliar repo, when a decision worth remembering has just been made, or when CONTEXT.md has drifted from the code.
---

# Context Map

Two artifacts, one job: make the **why** of a codebase reachable without reading all of it.

- **`CONTEXT.md`** — the mental model. What the modules are, how they relate, where things live. Read at the start of a session.
- **ADRs** — decision records. Why one option was chosen over another, and what it costs. Read when you're about to change the thing they cover.

Templates for both are in [FORMATS.md](FORMATS.md).

`CONTEXT.md` describes structure; `/codebase-design` supplies the vocabulary for it (module, interface, seam, depth) and `/domain-modeling` supplies the domain section. Use their words, don't invent parallel ones.

## Branch: map the codebase

Producing or refreshing `CONTEXT.md`.

1. **Read the entry points first** — the binaries, routes, jobs, or commands the system is actually invoked through. A map built from entry points is navigable; one built from the file tree is an inventory.
   _Done when_: you can name every way the system gets started.

2. **Name the modules and their seams.** For each: what it's responsible for, what its interface is, and what it depends on. Use `/codebase-design`'s vocabulary.
   _Done when_: every directory in the source tree is either accounted for by a named module or explicitly noted as not worth mapping.

3. **Record what's load-bearing and what's incidental.** This is the part that can't be derived from the code and is the whole reason the file exists: which choices are deliberate and would break things if changed, versus which are accidents of history that a reader should feel free to fix.
   _Done when_: a reader can tell, for each surprising thing in the codebase, whether it's surprising on purpose.

4. **Link, don't restate.** Point at ADRs, specs, and issues rather than summarising them. A summary is a second copy that goes stale independently.

_Done when_: an agent that reads only `CONTEXT.md` can find the right file for a given change without searching blindly.

## Branch: record a decision

Producing an ADR, after a decision has actually been made.

Write one when the decision is **load-bearing and non-obvious** — when a competent person would plausibly have chosen otherwise, and reversing it later would be expensive. Routine choices don't need a record; an ADR for every decision is noise that buries the ones that matter.

Capture the **alternatives that were seriously considered and why they lost**. A record of what was chosen, without what it beat, doesn't survive contact with the next person who thinks the rejected option is obviously better.

Record consequences honestly, including the bad ones. An ADR that lists only benefits is marketing, and the next reader will discover the costs the hard way.

ADRs are **immutable**. A decision that's been superseded gets a new ADR that supersedes it, with both linked — never an edit to the original. The value is the trail, and editing history destroys it.

## Keeping it true

A stale `CONTEXT.md` is worse than none: it costs the same to read and it actively misleads. The failure is silent, because nothing breaks when the map goes wrong.

Two defences:

- **Update it in the change that invalidates it.** When a change moves a seam, splits a module, or reverses something the map asserts, the map is part of that change — not a follow-up.
- **Check it when you use it.** Reading `CONTEXT.md` at the start of a session is also an opportunity to notice it's wrong. When you find a claim that no longer holds, fix it then, or say plainly that it's stale.

Prefer claims that stay true. "Auth lives behind one seam in `auth/`" survives refactoring; "`auth/session.ts` exports `validateSession`" is stale the moment someone renames a function, and the code already says it.
