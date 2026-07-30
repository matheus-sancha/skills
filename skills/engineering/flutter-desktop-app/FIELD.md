# Field Hardening

The app runs on PCs you cannot reach, for people who report problems in words. Words do not carry a stack trace. Everything here exists to make a build survivable at a distance.

## The diagnostics log

An append-only text file in the app directory that a user can attach to a message. Three rules:

- **Append immediately, never buffer.** The lines worth having are the ones written just before a crash, and a buffer is exactly what a crash discards. Serialise writes through a chained future so ordering still holds.
- **Never throw.** A logger that can break the app is worse than no logger. Swallow every failure — there is nowhere to report it to.
- **Ids, never text the user typed.** Breadcrumbs carry record ids, not names or notes, so the file is something a colleague can forward without wondering what else is in it.

Trim at a size cap by cutting at **session boundaries**, so a truncated log still begins at a header rather than halfway through someone's stack trace.

### A static facade, not a provider

```dart
abstract final class Diag {
  static DiagnosticsLog? _log;
  static Future<void> install() async { … }
  static void event(String event, [String? detail]) => _log?.event(event, detail);
  static void error(String source, Object e, StackTrace? s) => _log?.error(source, e, s);
}
```

The error hooks must be installed before a `ProviderScope` exists, the database's `beforeOpen` runs outside the widget tree, and repositories would otherwise each need a log threaded through their constructor. A static facade keeps every call site one line — and leaves the log **absent unless installed**, so `flutter test` writes no files and needs no setup.

### Three error channels, and the third is the one that matters

1. `FlutterError.onError` — build, layout, paint. **Chain it, do not replace it**, so the debug console still shows errors during development.
2. `PlatformDispatcher.instance.onError` — uncaught async errors outside the framework. Preferred over `runZonedGuarded`: no zone mismatch with `ensureInitialized`, and it catches what the framework's own zone would miss. Return `true` — reported here rather than killing the isolate.
3. **A Riverpod `ProviderObserver`'s `providerDidFail`.** Screens render a failed async provider as an error widget, so a repository that throws shows the user a wall of `SqliteException` and never touches `FlutterError.onError`. Without this observer you miss the failure class your users are most likely to actually hit.

### Session header

Write one at every launch: build label, machine, OS version, locale. It answers the questions every report otherwise costs a round trip to ask. Log the **schema version separately**, from `beforeOpen` — the database opens lazily on first query, long after the header is written. "Fresh install or upgrade?" resolves a surprising share of reports on its own.

### Route breadcrumbs

Listen to go_router's `routeInformationProvider`, not a `NavigatorObserver`: that yields the actual location string, and go_router does not guarantee a `Route.settings.name`. **Log the initial location explicitly** — `addListener` only fires on change, so the screen the user was looking at when launch went wrong is otherwise the one route missing.

## An in-app feedback channel

A dialog that writes the user's message beside the log and shows them where both files are. The point is not the message; it is that the log gets attached without you explaining a file path over the phone.

## Two safety nets, for two different failures

Neither replaces the other.

- **A manual backup bundle** — a zip of the database plus media, restorable on any machine. Covers losing the PC. The user has to ask for it.
- **A silent snapshot** — the database alone, taken once a day at launch, keeping the last few. Covers your own bugs, and never leaves the machine.

Rules for both:

- **Snapshot with `VACUUM INTO`, never a file copy.** It is transactionally consistent without closing the live database, and folds in un-checkpointed WAL content that a raw copy silently drops.
- **Restore is total, not a merge**, applied by copying tables into the running database in one transaction via `ATTACH` — not by swapping the file under a live connection. No restart, and no window where the open handle and the file on disk disagree.
- **Validate before touching anything**, so a rejected bundle leaves the app exactly as it was.
- **Version the bundle layout separately from the schema.** They move at very different rates. Migrate an older bundle forward on import; refuse a newer one with a message that says so.
- **Copy columns explicitly on restore**, for the same reason migrations do: a rebuilt table's column order differs between a fresh database and an upgraded one.
- The startup snapshot is **fire-and-forget and can never fail a launch** — wrap it, and log whether it ran. Then a data-loss report gets answered with "there is a copy from yesterday" instead of a guess.

## Desktop manners

- **Remember the window.** Windows does not do this for an application, so without it every launch opens at the hardcoded size from `windows/runner/main.cpp` and starts with a manual maximise, several times a day, for months. Store the frame as a small JSON file beside the database rather than in the settings table — window chrome is not domain state, and putting it there means a schema migration every time you add a field to it. Keep the unmaximised bounds even while maximised, so unmaximising lands somewhere sensible, and fall back to a default when the stored position no longer overlaps a display that exists.
- **Set a minimum size** below which the densest screen cannot lay out its columns. Refusing to shrink beats presenting something unusable.
- **Bind the primary repeated action to a key.** The thing a user does hundreds of times per session is the thing that must not require aiming a mouse at a row.
- **Recover work left in progress.** If the app can be closed mid-operation, detect that on the next launch and offer to resume or discard, rather than leaving an inconsistent row behind and no way to mention it.

## Render tools live in `test/`

Scripts that *produce* artefacts — sample exports, manual screenshots, generated asset files — go in `test/` but are **not** named `*_test.dart`, so a plain `flutter test` skips them. They need the Flutter test harness to render widgets; they assert nothing. Run them by path:

```bash
flutter test test/manual_screens.dart
dart run tool/generate_alert_sounds.dart
```

Commit what they produce. The generator exists so those assets stay reproducible and licence-free rather than being mystery binaries — not so it runs on every build.
