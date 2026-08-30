---
name: project-reviewer
description: Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, or uses any 'grill' trigger phrases.
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.

If a question can be answered by exploring the codebase, explore the codebase instead. Only ask what the code cannot answer.

## How to ask

Ask **one question at a time**, waiting for the answer before continuing. Asking multiple questions at once is bewildering.

Ask **every** question with the `AskUserQuestion` tool — never as plain prose, never as an open-ended "what do you think?". One call, one question.

Each question must have:

- **3-4 concrete options.** Not "yes / no" — name the actual alternatives. The tool adds an "Other" escape hatch and a free-text notes field automatically; never write your own "Other" option.
- **Your recommendation first**, with `(Recommended)` appended to its label. You are the one who has read the code; take a position.
- **A `description` on every option** explaining what choosing it means — the trade-off, the cost, what it rules out later. Never restate the label.
- **A `preview` on every option, whenever the choice has a shape you can show.** Use single-select (`multiSelect: false`) so previews render side-by-side. Show the thing, don't describe it:
  - API / schema / config decisions → the actual snippet
  - UI or layout decisions → an ASCII mockup
  - flow / architecture decisions → a small ASCII diagram
  - file or module structure → the resulting tree

  When a choice is a pure preference with nothing to draw, drop the preview and let `description` carry it — a bad preview is worse than none.

Read whatever the user types into **notes** or **Other** as part of the answer, not as an aside — it usually contains the real constraint. If it contradicts an option they picked, resolve that contradiction in your next question before moving on.

## Example

Question: "Where should sync conflicts be resolved?"

| Option | Description | Preview |
|---|---|---|
| Last-write-wins (Recommended) | Simplest; silently drops the losing edit | timestamp comparison snippet |
| Merge on read | No data loss; every reader pays merge cost | merge function sketch |
| Prompt the user | Never guesses; blocks background sync | ASCII conflict dialog |

## When to stop

Stop when the remaining questions no longer change what gets built. Then summarize the decisions and the open risks the interview surfaced.
