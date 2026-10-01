# OTEKH Apps — macOS Component

macOS is a first-class target for every OTEKH application, alongside Linux. This file covers the macOS-side setup, conventions, and packaging expectations. For the full process, see `OTEKH_App_Startup_Instructions_v1.3.txt`; for design rules, see `Otekh_App_Shell/docs/`.

## Package management: use Homebrew

On macOS, use **Homebrew** for system packages. Install once:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then:

```bash
brew update
brew install <package>
```

## Base development environment

```bash
brew install git curl python3 node
```

Project defaults (from `../agent.md`): Python is preferred, managed with `uv`; JavaScript uses `npm`. Apps should run with a single command where possible.

Xcode Command Line Tools are required for most builds:

```bash
xcode-select --install
```

## Fonts on macOS

The shell bundles Bai Jamjuree and Inter in `Otekh_App_Shell/install_fonts/` (WOFF2, with licences). For desktop apps, **bundle the font files with the application** — do not rely on system fonts or runtime downloads, since offline operation is a requirement.

To preview the shell locally with correct fonts, install them per-user:

```bash
mkdir -p ~/Library/Fonts/otekh
cp Otekh_App_Shell/install_fonts/*/*.woff2 ~/Library/Fonts/otekh/
```

Keep `LICENSE.txt` files alongside any distributed fonts.

## macOS platform conventions

- **Shortcuts**: Command-based (`Cmd+S`, `Cmd+O`, …). Linux uses Control — map both in cross-platform code.
- **Paths**: use `~/Library/Application Support/<app>/` for app data, `~/Library/Preferences/` for settings, `~/Library/Caches/` for cache. Never hardcode Linux paths.
- **File pickers**: use native `NSOpenPanel`/`NSSavePanel` via the framework (Electron, Tauri, Qt all handle this).
- **Window behaviour**: respect macOS window controls (traffic lights), menu bar conventions, and dark/light appearance.

## App integration

- Ship a proper `.app` bundle with `Info.plist` (bundle ID, version, document types).
- App icon as `.icns` — generate from the PNG export set per `docs/ICON_AND_LOGO_RULES.md` (16–1024 px).
- Support standard menu items (About, Preferences `Cmd+,`, Quit `Cmd+Q`).

## Packaging targets

- **.dmg** — standard drag-to-Applications distribution.
- **.zip of .app** — acceptable for internal/test builds.
- **Notarization** — required for distribution outside the App Store on modern macOS (`xcrun notarytool`). Needs an Apple Developer ID.
- Universal binaries (`arm64` + `x86_64`) where the stack supports it.

## macOS test checklist

- Launch and core workflow on a clean macOS install (both Apple Silicon and Intel if supported).
- Fonts render correctly (bundled, not substituted).
- Keyboard access and Cmd shortcuts; VoiceOver where applicable.
- File open/save through native pickers; drag-and-drop.
- Window resizing, compact width (<720 px), and Retina scaling.
- Offline start and reconnect behaviour.
- Correct `~/Library` paths; no Linux-only assumptions.

See `Otekh_App_Shell/docs/QA_CHECKLIST.md` for the full release checklist.
