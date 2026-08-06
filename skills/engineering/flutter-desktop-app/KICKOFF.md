# Kickoff

## Dependencies

The set that carries a local-first desktop app. Add to it reluctantly: every package is something that has to keep working on a PC you cannot reach.

| Need | Package |
|---|---|
| State | `flutter_riverpod`, `riverpod_annotation`, `riverpod_generator` |
| Database | `drift`, `sqlite3_flutter_libs`, `drift_dev`, `sqlite3` (dev, for migration fixtures) |
| Paths | `path_provider`, `path` |
| Routing | `go_router` |
| Ids | `uuid` |
| Formatting and locales | `intl`, `flutter_localizations` |
| Desktop window | `window_manager`, `screen_retriever` |
| File dialogs | `file_selector` |
| Export | `pdf`, `excel`, `archive`, `share_plus` |
| Media | `image_picker`; `image` (dev) for anything generated |
| Sound | `audioplayers` — **not** `SystemSound.play`, which is one fixed tone that cannot distinguish two alerts, is silenced by the Windows "No Sounds" scheme, and is a documented no-op on iOS |

## Pick the platforms once, on purpose

Windows and iOS share this architecture cleanly. Web does not: `dart:io` and native SQLite run through the whole data layer, so web is a port, not a build flag. Decide that at kickoff rather than discovering it later, and write the decision down in `DESIGN.md`.

## `main()` has an order, and it is load-bearing

```dart
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeDateFormatting();                       // 1
  await Diag.install();                                   // 2
  if (Platform.isWindows || Platform.isLinux || Platform.isMacOS) {
    await windowManager.ensureInitialized();              // 3
    final observer = WindowGeometryObserver();
    windowManager.addListener(observer);
    observer.rememberNormalBounds(await WindowGeometry.restore());
  }
  runApp(ProviderScope(
    observers: [DiagnosticsObserver()],
    child: const App(),
  ));
}
```

1. **Every locale's date symbols, up front.** Exports format dates outside the widget tree, so you cannot rely on the symbols `flutter_localizations` lazily loads for the active locale.
2. **Diagnostics first**, so the session header precedes anything worth logging and the error hooks are in place before any code that could trip them.
3. **Geometry before `runApp`**, while the window is still hidden — the runner's first-frame callback then reveals it already in the right place instead of showing a jump. Seed the observer with the restored bounds: a user whose first action is to maximise has no stored frame otherwise, so nothing gets saved at all.

## Generated code is committed

`*.g.dart` and the generated localizations go in git, and are excluded from the analyzer:

```yaml
analyzer:
  exclude:
    - "**/*.g.dart"
    - lib/src/l10n/generated/**
    - prototype/**        # throwaway spikes are not the app
```

CI then needs no code-generation step and a fresh clone builds. Regenerate with:

```bash
dart run build_runner build --delete-conflicting-outputs
flutter gen-l10n
```

**`riverpod_generator` cannot emit a provider whose return type is a Drift-generated class.** Both come out of the same `build_runner` pass and the ordering between builders is not guaranteed. Hand-write those as plain `StreamProvider`s — the generator only inspects `@riverpod`-annotated elements. Leave a comment saying why, or someone will "fix" it back:

```dart
@riverpod
ProjectRepository projectRepository(Ref ref) =>
    ProjectRepository(ref.watch(appDatabaseProvider));

/// Hand-written (not codegen) on purpose: riverpod_generator cannot emit a
/// provider returning a Drift-generated class from the same build pass.
final projectsListProvider = StreamProvider<List<Project>>(
  (ref) => ref.watch(projectRepositoryProvider).watchAll(),
);
```

Long-lived singletons — the database, the router — are `@Riverpod(keepAlive: true)` and dispose themselves via `ref.onDispose`.

## Localize from the first screen

Every language you intend to support gets an `.arb` file on day one. Retrofitting means revisiting every widget you have written; adding a string to three files as you go costs nothing.

No hard-coded user-facing strings anywhere, including in PDFs and spreadsheets. Locale drives number and date formatting too — decimal comma versus point — so a report built for a pt-BR user formats through `intl` with that locale, never `toStringAsFixed`.
