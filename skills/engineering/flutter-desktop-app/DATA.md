# Data

## One directory, resolved in one place

Every piece of on-device state — the database, the media folder, the diagnostics log, the window geometry file — lives under a single directory returned by a single function. Everything that needs it calls that function; nothing else calls `path_provider`. Relative paths stored in the database resolve against it, which is what lets a backup bundle restore onto a different machine.

```dart
Future<Directory> appDataDirectory() {
  if (Platform.isWindows) return getApplicationSupportDirectory();
  return getApplicationDocumentsDirectory();
}
```

**On Windows this must not be the documents directory.** `getApplicationDocumentsDirectory()` returns the *redirected* Documents folder, and OneDrive's Known Folder Move — on by default in most Microsoft 365 setups — places that inside a sync root. A sync client that uploads a live SQLite file and its `-wal` sidecar mid-write can corrupt the database, and can hold a lock while the app has the file open. Application Support (`%APPDATA%\Roaming\<company>\<product>`) is never redirected.

On iOS the documents directory is the right answer for the opposite reason: it is what iCloud backs up, which for an app with no accounts is the only automatic safety net there is.

**Media are files under that directory, referenced by id. Never blobs in the database.** Blobs bloat every backup, every `VACUUM`, and every query plan for something the database cannot search anyway.

## The database

One `AppDatabase`, `keepAlive` in a provider, closed on dispose. Its constructor takes an **optional** `QueryExecutor` and defaults to the on-device file — that optional argument is the whole testing story.

```dart
class AppDatabase extends _$AppDatabase {
  AppDatabase([QueryExecutor? executor]) : super(executor ?? _openOnDevice());

  static QueryExecutor _openOnDevice() => LazyDatabase(() async {
        final dir = await appDataDirectory();
        return NativeDatabase.createInBackground(
          File(p.join(dir.path, 'app.sqlite')),
        );
      });
}
```

## Migrations

Every schema change adds a numbered step and bumps `schemaVersion`. Four rules, each of which exists because the alternative fails silently on a machine you cannot inspect.

- **Copy columns explicitly. Never `SELECT *`.** A table that an earlier migration rebuilt has a different column order than a freshly created one, so positional copying scrambles values on exactly the upgraded databases you never see. Drift's `m.alterTable(TableMigration(...))` does the rename/create/copy/drop dance by name, and holds `legacy_alter_table` during the rename so other tables' foreign keys are not rewritten to point at the temporary table.
- **`m.createTable` builds from the *current* Dart definition.** So a step that rebuilds a table hands every later version a table that already carries their columns, and their `addColumn` fails the whole upgrade. Guard those steps — `if (from >= 3) { await m.addColumn(...); }` — and comment the guard, because the next column added to that table needs the same treatment for the same reason.
- **Additive steps first, rebuilds and backfills last.** A failure part-way then leaves the least behind, and the backfill runs against final tables.
- **Enable foreign keys on every open.** SQLite has them off by default: `beforeOpen: (d) async => customStatement('PRAGMA foreign_keys = ON')`. They are also off *during* migration, which is what makes the rename dance safe in the first place.

Inside a migration, prefer raw SQL. Drift's typed API maps to the *current* Dart definition, which may not be the shape the database has at that step. Use it only where you have just brought the tables involved up to date — and say so in a comment when you do, because it buys you generated ids and Drift's own encodings instead of hand-rolling both.

## Seeding

Reference data seeds in `onCreate`. Content you want *existing* users to receive — a starter catalog, new picklist options — seeds **outside the version guards**, on every upgrade, made idempotent by its own guards. Gating it on a version number reaches only future installs, and the people already running the app are exactly who it is for.

Use two guards, not one. "The table is empty" alone refills it on every upgrade, undoing a deliberate deletion. Pair it with a `seededAt` timestamp in settings — and set that timestamp even in the branch where you seed nothing, or emptying the table later reads as "never offered" and refills it.

Match seeded rows by **name, not id**, when they may already exist: rows created on an earlier install carry generated ids no constant can know.

## Testing the data layer

Repositories are testable because they are the seam. Construct one over an in-memory database and exercise it directly — no widget tree, no provider container:

```dart
setUp(() {
  db = AppDatabase(NativeDatabase.memory());
  projects = ProjectRepository(db);
});
tearDown(() => db.close());
```

**Test every migration against a fixture built in the old shape** — raw `CREATE TABLE` statements matching what that version actually shipped, then open the current `AppDatabase` over it and assert the rows survived. A migration exercised only against the current schema tests nothing: the shape it has to handle is the one you will never have in development. Keep one fixture per version you have released.
