# The Drop

A **drop** is one zip handed to one set of users. It has one label, one git tag, and one commit. If any of those three can disagree with the others, a bug report cannot be traced back to code — which is the failure everything here exists to prevent.

## The label is a Dart constant

```dart
/// **This constant is the single source of truth.** The app shows it in
/// Settings and tool/package_windows.ps1 parses it for the zip name, so the
/// name on disk and the string a user reads off the screen cannot disagree.
///
/// Bump before packaging. A second drop the same day gets a letter suffix.
const kBuildLabel = '2026-07-29b';
```

A date label, not a semver, while the version number would be claiming something you are not ready to claim. The packaging script *parses this file* rather than calling `Get-Date`.

_Rejected: `package_info_plus` reading `pubspec.yaml`._ Its version means what your release plan says v1 means, which is usually not yet true. _Rejected: stamping via `--dart-define`._ `flutter run` builds go anonymous, no test can pin the value, and forgetting the flag once produces an unidentifiable zip.

## The packaging script

One PowerShell script in `tool/`, run from the repo root, doing the whole thing reproducibly. In order:

1. **Resolve the label** by parsing the Dart constant. Throw if it is not found — a zip without a label is unidentifiable.
2. **Refuse to package** when the tag for that label already exists (that label is already out in the world) or the working tree is dirty (the tag would not describe what is in the zip). Give each refusal a `-Allow…` escape hatch for throwaway builds, and put the exact remedy in the error message.
3. `flutter build windows --release`, skippable with `-SkipBuild`.
4. **Stage the release output, then add the three Visual C++ runtime DLLs**: `msvcp140.dll`, `vcruntime140.dll`, `vcruntime140_1.dll`. Flutter links these dynamically and they are **not** part of the build output, so a PC that never had Visual Studio installed cannot start the app at all. Copy them from Visual Studio's redist folder — `C:\Program Files*\Microsoft Visual Studio\*\*\VC\Redist\MSVC\*\x64\Microsoft.VC*.CRT` — taking the newest toolset by **parsed** `[version]`, since a string sort puts 14.44 below 14.9. App-local deployment of these is licensed by Microsoft.
5. Add the user readme and the HTML manuals.
6. Zip, then report path, size, **SHA-256** and label.
7. **Print the `git tag` command; do not run it.** A packaging script does not get to create refs in your repo. But an untagged drop is an unidentifiable drop, so it must hand you the exact command to paste.

Clear only the staging folder, never all of `dist/`. The zips already there are the drops already handed out, and they are how you know what any given user is running.

The script does not run `flutter analyze` or `flutter test` — say so in its header, so the omission reads as a decision rather than an oversight.

**Keep the script ASCII-only.** Windows PowerShell 5.1 reads `.ps1` as ANSI, and UTF-8 punctuation — em dashes, section signs — becomes mojibake that can break parsing.

## What goes in the zip

- The app and its DLLs.
- A short plain-text readme **in the users' language**: unzip anywhere, run the `.exe`, and where their data lives.
- **Manuals as self-contained HTML, never markdown.** A `.md` double-clicked on a stock Windows PC opens in Notepad, where every screenshot is link text. Generate HTML with the images embedded as data URIs: one file, opens in any browser, nothing to keep beside it.

No installer, no store, no code signing. Users unzip a new version over the old one — safe precisely because the data lives in `%APPDATA%` and not in the program folder. Say that in the script's header too, next to the reference to the app-directory source file.

## Tagging

`previa/<label>`, or whatever prefix names the channel. The label is what a user says out loud; the tag is what turns it back into code. Tag the commit you packaged, immediately after packaging it.
