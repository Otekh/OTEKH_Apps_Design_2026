# OTEKH Apps — Linux Component

Linux is a first-class target for every OTEKH application, alongside macOS. Windows is excluded unless the user explicitly requests it. This file covers the Linux-side setup, conventions, and packaging expectations. For the full process, see `OTEKH_App_Startup_Instructions_v1.2.txt`; for design rules, see `Otekh_App_Shell/docs/`.

## Package management: use nala, not apt

On Ubuntu/Debian-based systems, **always use `nala` instead of `apt`**. Nala is a modern frontend for apt with clearer coloured output, parallel downloads, and more intuitive commands — it is fully compatible with apt repositories.

Install nala once:

```bash
sudo apt update && sudo apt install nala
```

Then use nala everywhere:

```bash
sudo nala update
sudo nala install <package>
```

## Base development environment

```bash
sudo nala update
sudo nala install build-essential git curl python3 python3-venv python3-pip nodejs npm
```

Project defaults (from `../agent.md`): Python is preferred, managed with `uv`; JavaScript uses `npm`. Apps should run with a single command where possible.

## Fonts on Linux

The shell bundles Bai Jamjuree and Inter in `Otekh_App_Shell/install_fonts/` (WOFF2, with licences). For desktop apps, **bundle the font files with the application** — do not rely on system fonts or runtime downloads, since offline operation is a requirement.

To preview the shell locally with correct fonts, install them per-user:

```bash
mkdir -p ~/.local/share/fonts/otekh
cp Otekh_App_Shell/install_fonts/*/*.woff2 ~/.local/share/fonts/otekh/
fc-cache -f
fc-list | grep -i -E "bai jamjuree|inter"
```

Keep `LICENSE.txt` files alongside any distributed fonts.

## Linux platform conventions

- **Shortcuts**: Control-based (`Ctrl+S`, `Ctrl+O`, …). macOS uses Command — map both in cross-platform code.
- **Paths**: follow the XDG base directory spec — config in `~/.config/<app>/`, data in `~/.local/share/<app>/`, cache in `~/.cache/<app>/`. Never hardcode macOS paths.
- **File pickers**: use native dialogs via the desktop portal (`xdg-desktop-portal`) or the framework's native picker (Electron, Tauri, Qt, and GTK all handle this).
- **Window behaviour**: respect the desktop environment's window controls, scaling (HiDPI), and dark/light preference where applicable.

## Desktop integration

- Ship a `.desktop` entry and install icons into the hicolor theme (`/usr/share/icons/hicolor/<size>/apps/` or `~/.local/share/icons/hicolor/`).
- Icon export sizes per `docs/ICON_AND_LOGO_RULES.md`: 16, 32, 64, 128, 256, 512 px PNGs.
- AppStream metadata (`*.metainfo.xml`) if distributing through software centres or Flatpak.

## Packaging targets

Pick per project, but plan for at least one of:

- **AppImage** — simplest single-file distribution.
- **.deb** — native for Ubuntu/Debian (build with `dpkg-deb`, `electron-builder`, or `cargo-bundle`/`tauri` depending on stack).
- **Flatpak** — best sandboxing and store distribution; requires a manifest.

## Linux test checklist

- Launch and core workflow on a clean Ubuntu/Debian install.
- Fonts render correctly (bundled, not substituted).
- Keyboard access and Ctrl shortcuts; Orca screen reader where applicable.
- File open/save through native pickers; drag-and-drop.
- Window resizing, compact width (<720 px), and HiDPI scaling.
- Offline start and reconnect behaviour.
- XDG paths used correctly; no macOS-only assumptions.

See `Otekh_App_Shell/docs/QA_CHECKLIST.md` for the full release checklist.
