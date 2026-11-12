# OTEKH App Manager — shared shutdown/management infrastructure

The **OTEKH App Manager** is the single status-bar entry every OTEKH app plugs into: one menu-bar icon (macOS) / system-tray icon (Linux) that lists every running OTEKH app and can stop it — individually or all at once — plus a per-app "Settings…" hook for apps that register one. It replaced per-app tray icons and the old "Stop OTEKH Apps" launcher (renamed November 2026).

Every OTEKH app **must** ship the shared installer block and write a running marker. No app ships its own tray icon for shutdown — that is the App Manager's job.

## What gets installed

| Artifact | Path | Purpose |
|---|---|---|
| `otekh_apps_stop` | `~/.local/bin/` | CLI stop engine — the tray delegates to it |
| `otekh_apps_menu` | `~/.local/bin/` | terminal fallback dropdown (osascript/zenity/select) |
| `otekh_tray` + `otekh_tray.py` | `~/.local/bin/`, `~/.local/share/otekh/` | the PySide6 status-bar app itself |
| `OTEKH App Manager.app` | `~/Applications/` (macOS) | launches the tray (Dock/Finder entry) |
| `otekh-app-manager.desktop` | `~/.local/share/applications/` (Linux) | same, for app menus |
| `com.otekh.tray.plist` | `~/Library/LaunchAgents/` (macOS) | autostart, logs to `otekh-tray.log`, restart-on-crash only |
| `otekh-tray.desktop` | `~/.config/autostart/` (Linux) | autostart |
| shared venv | `~/.local/share/otekh/venv` | one PySide6 install for all apps |
| registries | `~/.local/share/otekh/apps/`, `…/running/` | static install markers + live markers |

All installs share `~/.local/share/otekh/` — the newest installer version wins (`OTKH_APPS_STOP_VERSION` stamp), so any app updating refreshes the tools for every app.

## Marker protocol

A running app drops `~/.local/share/otekh/running/<app>.env` — a **bash-sourced** file (quote every value containing spaces):

```bash
APP_NAME=backup-sync                # required — menu key + CLI arg
DISPLAY_NAME="OTEKH Backup Sync"    # pretty name (default: title-cased APP_NAME)
PID=1234                            # required — checked with kill -0
PORT=8000                           # optional — orphan-listener fallback
WRAPPER=/path/to/command            # informational

# Optional App Manager hooks:
OPEN_CMD='bash /path/run.sh'        # adds "Settings…" — open/focus the app
STOP_CMD='bash /path/run.sh --quit' # graceful stop — used INSTEAD of killing
STOP_LABEL=Quit                     # menu verb (default "Shutdown")
```

- `OPEN_CMD` or `STOP_CMD` present → the app gets a **submenu** (`Display Name ▸ Settings… / <STOP_LABEL>`); neither → flat `Shutdown <name>`.
- Remove the marker on clean exit (EXIT trap, or `atexit` from inside the app).

## Shutdown contract — the important part

**An app that must shut down safely registers `STOP_CMD`; the manager then never kills it.** `otekh_apps_stop` runs `STOP_CMD`, waits a beat, and checks `kill -0 $PID`:

- process gone → `Stopped`, marker removed (the app should remove its own);
- still alive → reported as "may still be running", **marker kept** so a later stop can retry. A refused or user-cancelled quit must not escalate to a kill — the app asked for graceful handling precisely because a kill is unsafe (e.g. Backup Sync mid-backup).

Apps without `STOP_CMD` get the safe default: kill the process group **only** when the marker PID leads its own group (a blind group kill of a `.desktop`-launched app takes down the desktop session — this was a real incident), otherwise kill just that PID's process tree; port fallback for orphaned listeners.

## Menu behaviour

- **Shutdown all OTEKH Apps** — confirmation → stop everything → popup **"All Requested Apps shutdown safely."** (verifies markers cleared first; otherwise reports the count still running).
- **Per-app** — `STOP_LABEL <name>` → same popup flow for that app.
- **Quit OTEKH App Manager** — the tray itself exits; autostart brings it back at login.
- Single instance (`QLockFile`) — relaunching is a no-op.
- Fallback icon is drawn in code — an empty `QIcon` renders zero-width on macOS (icon invisible while the process runs).
- No PySide6 → installer skips the tray with a warning; `otekh_apps_stop`/`otekh_apps_menu` still work (relevant on headless/Pi installs).

## The shared installer block

Canonical copy lives in `OTEKH_Lab_Workspace/install.sh`, delimited by the banner `# --- Shared OTEKH App Manager + stop tool` through the end of `create_otekh_stop_icon()`. Vendor it verbatim into every app's installer (DCA, Digitization Manager, Backup Sync, PitFire, Weather all carry identical copies) and call:

```bash
BIN_DIR="$HOME/.local/bin" \
OTKH_APP_NAME=my-app \
OTKH_APP_PORT=8000 \
OTKH_APP_WRAPPER="$BIN_DIR/my-app" \
OTKH_ICON_SRC="$REPO_DIR/resources/icon.png" \
OTKH_APP_DISPLAY_NAME="My App" \
install_otekh_stop_tool
# optional: OTKH_APP_OPEN_CMD / OTKH_APP_STOP_CMD / OTKH_APP_STOP_LABEL
```

Keep the copies byte-identical; the version stamp lets the newest one win.

## Wrapper conventions

- Write the marker **before** launching the real process; `PID=$$`.
- Do **not** `exec` the server — keep the shell wrapper as parent: `server & wait`, `trap 'rm -f marker' EXIT`, `trap 'kill $srv; exit 0' INT TERM`. Exiting 0 on intentional TERM matters: a Finder/LaunchServices app that dies by signal gets macOS's "quit unexpectedly" report.
- Graceful-stop apps may instead write the marker from inside the app (Backup Sync does, after its single-instance claim) — PID should be the real app process.

## Reference implementation for STOP_CMD/OPEN_CMD

Backup Sync (`~/05_Projects/OTEKH_Backup_Sync`): `--quit` → QUIT over its single-instance control socket → marshalled onto the GUI thread → `closeEvent`'s guard (can refuse mid-backup). `OPEN_CMD` re-invokes `run.sh`, whose single-instance path signals SHOW and raises the window. GUI apps with no control channel can use a flag-file poll, an HTTP endpoint, or a unix socket — whatever the app already has.

## Troubleshooting

- Manager logs: `~/.local/share/otekh/otekh-tray.log` (stdout/stderr of the LaunchAgent/autostart).
- Icon missing: run `~/.local/bin/otekh_tray` in a terminal — import errors and `no system tray available` print to stderr; check `launchctl print gui/$(id -u)/com.otekh.tray` on macOS.
- App missing from menu: its `running/` marker is absent or the process died — check `ls ~/.local/share/otekh/running/`.
