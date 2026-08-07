---
name: test-strategy
description: Decide what deserves a test and which seam to write it at. Use when planning tests for new work, when a test is disproportionately hard to write, when the suite is slow or brittle, or when there's no good seam to test a bug against.
---

# Test Strategy

A test buys **confidence** and costs **coupling** — to the code's shape, not just its behaviour. The whole discipline is spending the second to buy the first, deliberately.

Two questions, in order. Most bad suites got the second right and the first wrong.

1. **Is this worth testing at all?**
2. **Which seam do I test it at?**

## What deserves a test

In descending order of value:

- **Invariants.** The conditions the domain says must always hold (`/domain-modeling`). These are the highest-value tests in any suite: they encode what the system refuses to allow, they're stated in the domain's own language, and they survive refactoring because they don't mention structure.
- **Decisions.** Branches that encode a judgement — pricing rules, permission checks, retry policy. If a human argued about it, test it.
- **Bugs that actually happened.** A regression test is a claim about reality, not a guess about it. This is the one category where the test is justified by evidence rather than prediction.
- **Contracts across a seam.** What callers on the other side are entitled to rely on.

## What doesn't

- **The framework.** That the router routes, the ORM saves, the validator validates. You're testing someone else's suite.
- **What the type system already guarantees.** A test that a typed field is that type is a no-op with a maintenance cost.
- **Getters, setters, and pass-throughs.** If deleting the code would make no behaviour disappear, deleting its test loses nothing either.
- **Implementation detail.** A test asserting *how* something works, rather than what it guarantees, breaks on every refactor and catches nothing. This is the coupling cost arriving with no confidence in exchange.

Coverage of these inflates the number and lowers the suite's value. A suite that must be rewritten whenever the code moves is a tax, not a safety net.

## Choosing the seam

**The interface is the test surface** (`/codebase-design`). Test a module through the interface its callers use — not past it, into the implementation. Wanting to reach past the interface is a design signal: usually the module is the wrong shape, or the thing you want to test deserves its own seam.

For each candidate seam, ask what confidence it buys that a **cheaper** seam doesn't:

- If a unit test at the module's interface catches it, an integration test adds cost and no confidence.
- If only wiring several real pieces together catches it — serialization, transactions, actual HTTP — then the cheap test genuinely can't, and the expensive one earns its place.
- If it takes a full end-to-end run to catch, ask whether that's essential complexity or a missing seam. Usually it's the missing seam.

Push tests to the **cheapest seam that can still fail for the right reason**. That's the useful reading of the test pyramid: not a quota of unit tests, but a bias toward the cheapest honest signal.

## Correct seams

A **correct seam** exercises the real pattern as it occurs at the call site. A seam that can only replicate a simplified version of the real usage gives false confidence — it goes green while the bug lives.

When `/diagnosing-bugs` reaches Phase 5 and finds no correct seam for a regression test, that's the same problem arriving from the other direction: the architecture is preventing the bug from being locked down. Both cases resolve the same way — the missing seam is the finding. Create it (hand off to `/codebase-design`), or state plainly that the bug can't be regression-tested and why.

Never write the test at a wrong seam to have written one. A green test that cannot fail for the right reason is worse than no test: it removes the pressure to build the seam that would work.

## Doubles

Prefer, in order:

1. **The real thing**, when it's fast and deterministic. A real in-memory store beats a mock of one.
2. **A fake** — a working implementation with a shortcut, shared across tests. Written once, exercises the same interface as production.
3. **A stub** returning canned values, for what you can't run.
4. **A mock asserting on calls** — last resort. It asserts *how* the code works, which is the coupling you're trying not to buy. Reach for it only when the interaction itself is the behaviour under test, as with a retry policy.

A test needing many doubles to stand up is reporting on the design: the module under test has too many dependencies, or its seam is in the wrong place.
