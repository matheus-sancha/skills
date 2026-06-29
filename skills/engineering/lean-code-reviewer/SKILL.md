---
name: lean-code-reviewer
description: Review the codebase and the project's domain model and architecture, and identify waste or redundancies and suggest improvements to make the codebase optimal and reduce token consumption.
version: 1.0.0
argument-hint: "Which area or module to focus on? (default: entire codebase)"
---

# Lean Code Reviewer

A **lean** codebase carries no **waste**: every module earns its lines, every abstraction has at least two concrete use cases, and the surface a reader (or agent) must traverse to understand the system is as small as the problem allows.

If the user passed an argument, scope the review to that area. Otherwise review the entire codebase.

## Steps

1. **Map the structure.** Read entry points, key types, and module boundaries. Build a mental model before hunting waste — you cannot see redundancy without first seeing structure. For module vocabulary (depth, seam, adapter, interface), use `/codebase-design`.
   _Done when_: you can describe each module's interface and how it relates to the others.

2. **Hunt waste.** Apply every category in [Waste Catalogue](#waste-catalogue) to every module in scope. For each instance record: location (file + line range), category, and a concrete improvement.
   _Done when_: every module examined against every category — no files skipped.

3. **Report.** Group findings by category, ordered by impact (most tokens/complexity saved first). For each finding: location, what the waste is, and the specific change that removes it.

## Waste Catalogue

### Shallow modules
A module whose interface is nearly as complex as its implementation — the caller absorbs work the module should hide. Signs: many thin pass-through methods; parameters that repeat at every call site; logic that leaks into callers.

### Duplication
The same meaning in more than one place. Look for: copy-pasted blocks, parallel type hierarchies, functions that do the same thing under different names, constants defined twice.

### Dead code
Exports, functions, types, or variables unreachable from any production path. Go beyond what the type-checker flags — follow call chains.

### Premature abstraction
An interface, base class, or wrapper with exactly one implementation and no concrete variation expected. One adapter means a hypothetical seam; flag it.

### AI slop
Code that was generated quickly without meaningful design — syntactically valid but semantically hollow. It passes review on a first read and silently degrades the codebase. Signs:
- **Pointless wrappers** — a function that does nothing but call one other function with the same arguments
- **Single-use helpers** — extracted functions called exactly once, adding a name but no reuse or clarity
- **Defensive noise** — null checks, try-catch blocks, or fallback defaults for conditions the calling context already guarantees can't occur
- **Generic names** — `handleData`, `processItem`, `result`, `temp`, `util` — names that describe shape but not meaning
- **Copy-paste mutations** — near-identical blocks differing only in one value, where a loop or parameter would do
- **Always-true guards** — conditions that are structurally guaranteed by the type or the call site (e.g. checking `if (arr)` on a parameter typed `T[]`)
- **Comment noise** — per-line comments restating what the code says, or block comments describing the obvious flow
- **Hallucinated patterns** — abstractions (factory, strategy, observer) applied to a one-off problem with no second use case in sight

Slop is distinct from the other categories: it isn't merely redundant or shallow — it actively misleads a reader into thinking deliberate design choices were made. Flag it separately and be explicit that the fix is deletion, not refactoring.

### Token-heavy structure
Patterns that cost the model (and the reader) disproportionate context to navigate:
- Files over ~300 lines without a clear reason (a module that should split)
- Nesting deeper than 3 levels where early returns or extracted functions would flatten it
- Names that restate their module context (`UserRepository.getUserById` → `Users.byId`)
- Comments that describe what the code already says clearly
- Duplicate types: two shapes describing the same thing under different names
