# OTEKH Apps — Windows Component

**Windows is not a default OTEKH target.** Per `OTEKH_App_Startup_Instructions_v1.3.txt`, all OTEKH apps target macOS + Linux only. Use this file **only when the user explicitly requests Windows support** for a specific project — otherwise do not provide Windows instructions, installers, paths, or compatibility work.

## Package management: use winget

On Windows 10/11, use **winget** (built into current Windows) for system packages:

```powershell
winget install <package>
```

Alternatives: `choco install <package>` (Chocolatey) or `scoop install <package>` for dev tools.

## Base development environment

```powershell
winget install Git.Git Python.Python.3.12 OpenJS.NodeJS
```

Project defaults (from `../agent.md`): Python is preferred, managed with `uv`; JavaScript uses `npm`. Apps should run with a single command where possible.

C++ build tools may be required for native dependencies:

```powershell
winget install Microsoft.VisualStudio.2022.BuildTools
```

## Fonts on Windows

The shell bundles Bai Jamjuree and Inter in `Otekh_App_Shell/install_fonts/` (WOFF2, with licences). For desktop apps, **bundle the font files with the application** — do not rely on system fonts or runtime downloads, since offline operation is a requirement.

To preview the shell locally, install fonts per-user by copying to `%LOCALAPPDATA%\Microsoft\Windows\Fonts`, or right-click → Install. Keep `LICENSE.txt` files alongside any distributed fonts.

## Windows platform conventions

- **Shortcuts**: Control-based (`Ctrl+S`, `Ctrl+O`, …) — same as Linux.
- **Paths**: use `%APPDATA%\<app>\` for roaming config/data, `%LOCALAPPDATA%\<app>\` for local data/cache. Use `path.join`/`pathlib` — never hardcode `/` or `~` paths.
- **File pickers**: use native dialogs via the framework (Electron, Tauri, Qt all handle this).
- **Window behaviour**: respect Windows window controls, DPI scaling (per-monitor aware), and dark/light mode.

## App integration

- App icon as `.ico` (multi-size: 16–256 px) generated from the PNG export set per `docs/ICON_AND_LOGO_RULES.md`.
- Set app metadata: file description, product name (`OTEKH <Product>`), version.

## Packaging targets

- **MSI or NSIS installer** — standard installable distribution (`electron-builder`, `tauri`, or WiX depending on stack).
- **Portable .zip** — acceptable for internal/test builds.
- **Code signing** — required to avoid SmartScreen warnings; needs an EV or standard code-signing certificate.
- **MSIX / Microsoft Store** — only if the user requests store distribution.

## Windows test checklist

- Launch and core workflow on a clean Windows 10/11 install.
- Fonts render correctly (bundled, not substituted).
- Keyboard access and Ctrl shortcuts; Narrator/NVDA where applicable.
- File open/save through native pickers; drag-and-drop.
- Window resizing, compact width (<720 px), and DPI scaling (100%/150%/200%).
- Offline start and reconnect behaviour.
- Correct `%APPDATA%`/`%LOCALAPPDATA%` paths; no POSIX-only assumptions (paths, line endings, shell commands).

See `Otekh_App_Shell/docs/QA_CHECKLIST.md` for the full release checklist.
