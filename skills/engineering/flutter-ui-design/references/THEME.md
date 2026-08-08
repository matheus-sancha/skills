# THEME — tokens into ThemeData, and the Material 3 anti-defaults

Goal: one token file drives both themes; the stock-M3 tells are all corrected. Read this when setting up or fixing theming.

## 1. Tokens in plain Dart

Keep tokens as `const` with no Flutter imports beyond `dart:ui`/`material` for `Color`. They are data, not widgets.

```dart
/// Spacing — 8-dp rhythm, 4 for tight pairs. The only gaps allowed in the app.
abstract final class Space {
  static const xs = 4.0, sm = 8.0, md = 12.0, lg = 16.0;
  static const xl = 24.0, xxl = 32.0, xxxl = 48.0, huge = 64.0;
}

/// Radius — one family, chosen by component role, never ad hoc.
abstract final class Radii {
  static const sm = 4.0, md = 8.0, lg = 12.0, xl = 16.0;
  static const full = 999.0; // pills, avatars
}

/// Motion — durations + the one easing curve. Refactoring UI: motion earns its place.
abstract final class Motion {
  static const fast = Duration(milliseconds: 100);   // state layers, ripples
  static const base = Duration(milliseconds: 200);   // most transitions
  static const slow = Duration(milliseconds: 300);   // page / shared-axis
  static const curve = Curves.easeOutCubic;          // M3 "emphasized" feel
}
```

## 2. Colour — one seed, both themes

Material 3's `ColorScheme.fromSeed` is the right engine; the defaults are the problem. Pick a real brand seed (**never leave it Flutter purple**) and generate both brightnesses from it, so light and dark are provably the same token set.

```dart
const _seed = Color(0xFF3B6EA5); // replace with the project's brand seed

ColorScheme _scheme(Brightness b) => ColorScheme.fromSeed(
  seedColor: _seed,
  brightness: b,
);
```

Semantic colours (success/warning/error) live beside the scheme as named tokens, not scattered literals. Map `error` to the scheme's `error`; define success/warning yourself once.

```dart
abstract final class Semantic {
  static const success = Color(0xFF2E7D32);
  static const warning = Color(0xFFED6C02);
  // error → use ColorScheme.error
}
```

## 3. ThemeData — assemble, correct, expose

```dart
ThemeData buildTheme(Brightness brightness) {
  final scheme = _scheme(brightness);
  final base = ThemeData(colorScheme: scheme, useMaterial3: true);

  return base.copyWith(
    textTheme: _typeRamp(base.textTheme),
    // ── Anti-defaults (see §4) ──
    scaffoldBackgroundColor: scheme.surface,        // kill the tinted grey mud
    cardTheme: base.cardTheme.copyWith(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(Radii.lg),
        side: BorderSide(color: scheme.outlineVariant),
      ),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(Radii.md),
        ),
      ),
    ),
    visualDensity: VisualDensity.standard, // desktop: consider .comfortable
  );
}
```

Wire both into `MaterialApp` and let the OS choose:

```dart
MaterialApp.router(
  theme: buildTheme(Brightness.light),
  darkTheme: buildTheme(Brightness.dark),
  themeMode: ThemeMode.system, // dark is mandatory, not optional
  routerConfig: router,
);
```

## 4. The Material 3 anti-defaults (what makes stock M3 look like a demo)

Correct every one of these; each is an `AUDIT.md` line:

- **Purple seed.** The `#6750A4` default screams "untouched Flutter." Set a real seed.
- **Tonal surface mud.** M3 tints surfaces toward the seed; at rest it reads as dirty grey. Set `scaffoldBackgroundColor: surface` and prefer flat `surface`/`surfaceContainer*` roles deliberately rather than accepting elevation-tinted defaults.
- **Elevation soup.** Default cards float on shadow. Prefer **elevation 0 + a 1-px `outlineVariant` border** for separation; reserve real shadow for genuinely floating things (menus, dialogs).
- **Over-rounding.** Some M3 components default to 20–28 px radii that look bubbly. Pull to the radius scale (`md`/`lg`) for a crisper feel.
- **Too many weights / fonts.** Cap at two weights. If using `google_fonts`, one family, or one display + one text family at most.
- **Ripple everywhere.** Fine on touch; on desktop, pair every interactive surface with a **hover + focus-visible** state (see AUDIT), not just the ripple.

## 5. The type ramp

Build the ramp from a ~1.2 ratio mapped onto M3 roles, so `Theme.of(context).textTheme.titleLarge` etc. carry the scale. Hierarchy comes from **size + weight + colour** (`onSurface` vs `onSurfaceVariant`), not from inventing sizes at call sites. Never hardcode `fontSize:` in a widget — if a role is missing, add it to the ramp.
