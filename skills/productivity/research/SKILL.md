---
name: research
description: Investigate a question against primary sources and capture the findings as a cited Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated.
---

# Research

Findings are only worth what their sources are worth. This skill trades speed for **provenance**: every claim traceable to the source that owns it.

## Primary sources

A **primary source** is the artifact that *owns* the fact — official docs, the source code itself, a spec, a first-party API, a changelog from the people who shipped it. A blog post explaining an API is not the API. A Stack Overflow answer is not the spec. Secondary sources are useful for *finding* the primary one; they are never where a claim comes to rest.

Follow every claim back to its owner. When you can't reach one, the claim is **unverified** — say so in the findings rather than laundering a secondary source into a fact.

Sources disagree, and often the disagreement *is* the finding: docs contradicting a changelog usually means something shipped, moved, or was rolled back. Record both, say which you trust and why. Don't silently pick one.

Where the question can be settled by running something — an API call, a flag, a query — run it. An observed result outranks any document describing it, including the official one.

## Output

Write findings to a single Markdown file:

- Put it where the repo already keeps such notes. Match the existing convention; if there is none, choose somewhere sensible and **say where you put it** in your reply.
- Cite each claim inline with a link to its primary source, not a bibliography at the end — a reader checking one claim shouldn't have to guess which of twelve links covers it.
- Lead with the answer. The question was asked because someone needs to act; the reasoning goes below the conclusion, not above it.
- Mark unverified claims and open disagreements explicitly.

_Done when_: every claim in the file either carries a link to its owning source or is explicitly marked unverified.

## Backgrounding

If the user asked for a background agent, or the reading is long enough that they'd otherwise sit idle, delegate it to one and keep working. Otherwise just do the research — a background agent for two doc pages costs more than it saves.
