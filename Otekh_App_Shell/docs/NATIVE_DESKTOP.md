# OTEKH Native Desktop — Non-Webapp Design Approach

How to build an OTEKH-looking **desktop application** (no browser) for
macOS and Linux — first proven in *OTEKH Backup Sync* (V0.92, 2026-10).
The design system is unchanged: same tokens, same fonts, same layout
grammar. This file covers the translation and, critically, the
*aesthetics floor* — native does not mean ugly.

## Why native, not web

Choose a desktop app when the job is local-first: filesystem-heavy
work, system tray / menu-bar presence, autostart behaviour, offline by
definition, or long-running background jobs that must survive window
close. A web app still wins when multiple users share state or reach
the app over the network. Same Shell either way.

## Frontend selection — aesthetics decides

| Platform | Frontend | Why |
|---|---|---|
| macOS + desktop Linux | **PySide6 (Qt)** | Aesthetics is first-class. Qt delivers what Tk cannot: real hover states, rounded controls, true native dialogs, tray icon + menu-bar extra, full stylesheet control. |
| Raspberry Pi / embedded | **Tkinter + CustomTkinter** | Footprint over polish. See `TKINTER.md` — same tokens, same layout, reduced chrome. |

The rule: **if the user will look at it daily, it must look modern.**
Tk's flat controls and limited theming are acceptable on a Pi sensor
kiosk; they are not acceptable on a design-led desktop build. Qt costs
a heavier dependency (via `uv`, painless) and buys the look the lab
expects from a web app.

## Aesthetics floor — non-negotiable on desktop

- **Tokens are the single source.** Every colour, font, and geometry
  value comes from `tokens/otekh_tokens.py`, rendered into a Qt
  stylesheet. Never hand-pick hex values in widget code.
- **Layout grammar carries over.** Dark AppBar + 3 px gold rule,
  horizontal tabs, full-width page stack, 44 px StatusBar with the
  `Powered by OTEKH Labs | Vx.y` footer — the desktop layout mirrors the
  web shell's five regions, so a user moving between a web tool and a
  desktop tool feels continuity.
- **Modern micro-interactions.** Hover states, pressed states, soft
  gold selection, hairline separators, thin trackless scrollbars — the
  polish that makes it feel 2026 rather than 2006. This is the whole
  point of choosing Qt.
- **Gold is for selection and primary action only.** Same rule as the
  web shell; do not spread it around.
- **Native dialogs.** Error / confirm / file-pick flows use the OS
  dialogs where possible (QMessageBox, native folder pickers) — the
  app should feel like it belongs on the machine, not ported onto it.

## Architecture pattern — proven shape

```
app entry (CLI flags, single-instance flock, frontend dispatch)
   ├── Qt frontend (macOS/Linux) ┐
   └── Tk frontend (Pi)         ├──► shared engine.py — UI-agnostic
                                 │    core: all logic, callbacks for
                                 │    progress/log/error/confirm
                                 ▼
                            store.py (json persistence)
```

- **Frontend-agnostic engine.** `engine` owns the logic; frontends own
  pixels. Callbacks (`progress`, `log`, `on_error`, `confirm`) keep the
  engine UI-free so Qt and Tk can share it verbatim.
- **Worker thread → GUI thread.** Backup runs on a plain thread; every
  UI update crosses over via Qt `Signal`s (queued onto the GUI thread)
  or Tk `after(0)`. Never touch a widget from a worker — the Tk build's
  crashes came from exactly this.
- **Synchronous prompts from workers.** A worker that needs a yes/no
  (e.g. "fix these filenames?") emits a signal carrying the message and
  parks on a `threading.Event` until a GUI-thread slot writes the reply.
  Qt and Tk both implement this bridge.
- **Never die silently.** Every worker path wraps in a catch-all that
  logs `=== failed: {exc} ===` and sets error status. An uncaught
  worker exception otherwise leaves the app looking idle-but-dead —
  the hardest bug to diagnose from user reports.

## Desktop-specific conventions

- **System tray / menu-bar extra.** `QSystemTrayIcon` with a context
  menu: live status line (disabled item), open/settings action, Quit
  routed through the same close-confirm path as the window. Same code
  gives a macOS menu-bar extra — no platform branch needed.
- **Autostart.** `.desktop` file in `~/.config/autostart` on Linux;
  LaunchAgent on macOS. App must accept `--hidden` and start without
  showing its window while schedules keep running.
- **Close ≠ quit.** Window close offers *Keep running in background /
  Cancel / Shutdown*; background jobs must be stoppable safely (cancel
  event, bounded join, then exit).
- **Inhibit sleep during runs.** `caffeinate -is` on macOS,
  `systemd-inhibit` on Linux — the OS must not nap mid-backup.
- **Single instance.** `flock` (or equivalent) so double-launches
  forward to the running instance instead of stacking two daemons.

## Desktop error ergonomics

Background apps fail quietly by default — don't let them. Post-run,
group errors into categories (vanished files, no space, read-only
dest, permission denied, filename rejection, over-size for the dest
filesystem) and present each group once with a plain-language fix. When
a repair is possible (e.g. rename invalid FAT filenames), offer it as a
yes/no dialog *after* the run, then retry only the affected paths —
never block the main run on preflight.

## Checklist for a new desktop app

1. `pick_frontend` dispatch (Qt default, Tk fallback/Pi, `--force-tk`
   escape hatch)
2. Qt stylesheet generated from `otekh_tokens.py` — not hand-written
   hex
3. Five-region layout grammar mirrored; StatusBar footer with version
4. Worker→GUI marshalling via signals; no widget access off-thread
5. Catch-all in every worker path
6. Tray menu (status / open / quit-through-close-guard)
7. `--hidden` + autostart entry
8. Sleep-inhibit during long runs
9. Single-instance lock
10. Same data/JSON conventions as the web apps
