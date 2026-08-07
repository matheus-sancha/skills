# Smell baseline

Fowler's code smells (_Refactoring_, ch. 3), as the floor the Standards axis
applies when a repo documents nothing — and in addition to whatever it does
document.

Two rules bind every entry:

- **The repo overrides.** A documented repo standard always wins. Where it
  endorses something below, suppress the smell.
- **Always a judgement call.** Label each as a possibility ("possible Feature
  Envy"), never a hard violation. Skip anything tooling already enforces.

Match these against the diff, not the whole codebase. Each reads
*what it is* → *how to fix*.

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. → Rename it; if no honest name comes, the design is murky.
- **Duplicated Code** — the same logic shape in more than one hunk or file in the change. → Extract the shared shape, call it from both.
- **Feature Envy** — a method reaching into another object's data more than its own. → Move the method onto the data it envies.
- **Data Clumps** — the same few fields or params travelling together, a type wanting to be born. → Bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept. → Give the concept its own small type.
- **Repeated Switches** — the same `switch` or `if`-cascade on the same type recurring across the change. → Replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forcing scattered edits across many files in the diff. → Gather what changes together into one module.
- **Divergent Change** — one file or module edited for several unrelated reasons. → Split so each module changes for one reason.
- **Speculative Generality** — abstraction, parameters, or hooks added for needs the spec doesn't have. → Delete it; inline back until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. → Hide the walk behind one method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward. → Cut it, call the real target directly.
- **Refused Bequest** — a subclass or implementer ignoring or overriding most of what it inherits. → Drop the inheritance, use composition.
