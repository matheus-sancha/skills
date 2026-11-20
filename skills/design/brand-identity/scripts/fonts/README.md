# Bundled fonts

Six OFL 1.1 variable families from the official google/fonts repository (`ofl/<family>/`), fetched 2026-11-20.
Each licence was checked in the family's `METADATA.pb` (`license: "OFL"`) and its `OFL-<Family>.txt` is kept here.

| File | Class | Axes |
|---|---|---|
| `Outfit-Variable.ttf` | geometric sans | wght |
| `SchibstedGrotesk-Variable.ttf` | grotesque | wght |
| `SourceSans3-Variable.ttf` | humanist sans | wght |
| `Fraunces-Variable.ttf` | serif (soft, display-capable) | opsz, wght, SOFT, WONK |
| `Bitter-Variable.ttf` | slab | wght |
| `JetBrainsMono-Variable.ttf` | mono | wght |

Overused faces the Design System type flags (Inter, Roboto) are left out on purpose.
Wordmarks are always outlined. Font files reach the user only in the kit's `type/` folder, with the matching OFL text.
Note: several defaults are the Thin instance; always pass a `wght` when outlining.
