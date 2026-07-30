---
name: flutter-desktop-app
description: Blueprint for a local-first Flutter app shipped to users as a plain Windows zip. Use when scaffolding such a project, adding a feature slice, changing a Drift schema, hardening a build for users nobody is watching, or packaging and tagging a drop.
---

# Flutter Desktop App

A **local-first** Flutter app — no accounts, no server, no sync — that reaches users as a **drop**: a plain zip they unzip anywhere and run. Two consequences of that setup drive every rule below. You cannot push a fix, so a bad drop lives on someone's PC until they ask for another. And nobody is watching the app run, so the only evidence you will ever get is what the build wrote down about itself.

Worked example: `C:\src\Chronus`. Read it when a rule here needs one.

## The shape

```
lib/
  main.dart                    wiring only, in a fixed order (KICKOFF.md)
  src/
    app/         router, theme, shell, build label, window geometry
    common/      widgets and formatters more than one feature uses
    data/        the database, the schema, the one app directory
    features/<feature>/
      data/          repositories — the only code that touches the database
      application/   providers, notifiers, and every calculation
      presentation/  screens and widgets
    l10n/        one .arb per language + generated output
docs/DESIGN.md   why the app behaves the way it does
tool/            the packaging script and any generators
```

## The slice

Each feature is a vertical **slice** of three folders, and imports only ever point `data → application → presentation`.

- **`data/` is the seam.** A repository is the only place queries are written and Drift types are constructed; nothing outside it imports `drift` except for `Value`. That single rule is what makes the app testable without a widget tree.
- **`application/` holds the providers and all of the arithmetic.** Reports, statistics, comparisons — pure functions over rows, in their own files, tested directly. A screen that computes anything beyond formatting is a bug.
- **`presentation/` renders and dispatches.** It watches providers and calls notifiers.

Reads are `Stream`s off the database, not futures. The UI is driven by the table, so a write anywhere refreshes every screen showing that data with no manual invalidation.

## Write down what you rejected

A decision that took thought gets a doc comment naming the alternative and why it lost, on the code that embodies the decision — not in a commit message nobody will find:

```dart
/// _Rejected: `package_info_plus` reading `pubspec.yaml`._ Its `1.0.0+1`
/// deliberately does not yet mean what §8.3 means by v1, so a semver would
/// have to start claiming something untrue.
```

`docs/DESIGN.md` is the single source of truth for intended behaviour, cited from code by section number (`(DESIGN.md §10.5)`). Read it before changing behaviour; update it in the same commit that changes it.

## When to read what

| Occasion | Read |
|---|---|
| Scaffolding a new project, or adding a dependency | [KICKOFF.md](KICKOFF.md) |
| Storage paths, schema changes, migrations, seeding | [DATA.md](DATA.md) |
| Packaging, labelling and handing out a build | [DROP.md](DROP.md) |
| Diagnostics, backups, window behaviour | [FIELD.md](FIELD.md) |
