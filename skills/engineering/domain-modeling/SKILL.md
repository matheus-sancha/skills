---
name: domain-modeling
description: Pin down the domain — name the entities, their relationships, and the invariants that must always hold, then lock one ubiquitous language for them. Use when the nouns of a feature are still vague, when the same concept goes by several names, or before designing the modules that will hold it.
---

# Domain Modeling

Grilling surfaces **decisions**; this surfaces **nouns**. The output is a model: the things that exist, how they relate, what must always be true of them, and exactly one name for each.

Work it like an interview — **one question at a time**, waiting for the answer before the next. Where a question can be answered by reading the code, read the code instead of asking.

This skill stops at the model. Turning it into modules, interfaces, and seams is `/codebase-design`.

## Vocabulary

**Entity** — a thing with identity that persists through change. Two entities with identical fields are still different things. An order stays the same order after its status changes.

**Value object** — a thing defined entirely by its values, with no identity. Two are interchangeable if their fields match. Money, a date range, an address.

**Invariant** — something that must be true at every observable moment, not just usually. "An order's total equals the sum of its lines." Invariants are the model's real content: they say what the system refuses to allow.

**Aggregate** — a cluster of entities and value objects that must stay consistent together, with one entity as its root. The aggregate is the unit an invariant can be enforced over, because it's the unit you can lock, load, and save as a whole.

**Ubiquitous language** — one name per concept, used identically in conversation, code, tests, docs, and the UI. Its value is entirely in being *ubiquitous*: a synonym anywhere costs more than a slightly worse name everywhere.

**Bounded context** — the region within which one ubiquitous language holds. The same word means different things in different contexts, and that's fine — as long as the contexts are named and the translation between them is explicit. (`codebase-design` deliberately avoids "boundary" for this reason; say **bounded context** for the domain, **seam** for the code.)

## Steps

1. **Harvest the nouns.** Collect every candidate from the user's own words, the tickets, and the existing code. Don't filter yet — synonyms and near-misses are the raw material.
   _Done when_: the list includes every noun the user has used for this feature, including the ones you suspect are duplicates.

2. **Collapse the synonyms.** Find the nouns that name the same concept, and the single nouns that are secretly two concepts. This is where most of the value is: a codebase with `user`, `account`, `member`, and `profile` for one thing has a modelling problem, not a naming problem.
   _Done when_: each surviving noun names exactly one concept, and each concept has exactly one noun.

3. **Classify each as entity or value object.** The test: if two of these had identical fields, would they be the same thing? Same → value object. Different → entity.
   _Done when_: every noun is classified, and any you couldn't classify is flagged as genuinely ambiguous rather than skipped.

4. **Map the relationships.** For each pair that relates: what's the cardinality, which side owns the reference, and can either side exist without the other? Lifecycle dependence is what reveals aggregates.
   _Done when_: every relationship has a cardinality and an owner.

5. **Pin the invariants.** For each concept and each relationship, ask what must *always* be true. Then ask the sharper question: **what would it mean if this were violated?** An invariant nobody can describe the violation of isn't one.
   _Done when_: every invariant is stated as a checkable condition, and each is assigned to the aggregate that can enforce it.

6. **Record it.** Write the model where the repo keeps such notes — if `CONTEXT.md` exists, its domain section belongs there (`/context-map` owns that file). State each concept, its classification, its relationships, and its invariants.
   _Done when_: a reader who has never seen the conversation can use the model without asking what a word means.

## What good looks like

The model is done when the **invariants** are sharp, not when the noun list is long. A list of entities with no invariants is a glossary, and a glossary decides nothing.

Two signals you're finished early:

- **You can't state an invariant for a concept.** Either it's a value object with nothing to enforce, or you haven't found what it's for.
- **Every relationship is "has many".** Real domains have lifecycle rules — things that can't exist alone, things that must be created together. If nothing depends on anything, you've drawn a schema, not a model.
