# OTEKH Apps — Raspberry Pi Component

Raspberry Pi OS is a target for **local, single-machine OTEKH applications**: sensor stations, kiosks, field devices, and lab instruments that run on a Pi 4/5 with a local display. These apps are Linux apps first — everything in `LINUX.md` applies — but they are allowed to be Pi-only when they depend on GPIO/I2C hardware. For the full process, see `OTEKH_App_Startup_Instructions_v1.2.txt`; for design rules, see `Otekh_App_Shell/docs/`.

## Stack: Tkinter/CustomTkinter

The reference stack for Pi local apps is **Python + CustomTkinter** — lightweight enough for a Pi, native desktop windows, no browser runtime. The Shell ships a complete Tkinter toolkit:

- `Otekh_App_Shell/tokens/otekh_tokens.py` — all design tokens as Python constants
- `Otekh_App_Shell/tkinter/otekh_shell.py` — app bar, nav rail, panels, data wells, status bar, dialogs, button factories, font bootstrap
- `Otekh_App_Shell/starter/starter-shell-tkinter.py` — runnable five-region reference layout
- `Otekh_App_Shell/install_fonts/*/ttf/` — TTF builds of the bundled fonts (Tkinter cannot load WOFF2)
- `Otekh_App_Shell/docs/TKINTER.md` — token→widget mapping and behaviour rules

Copy `otekh_tokens.py` + `otekh_shell.py` into the project (or import in place) and build on the starter. The OTEKH Weather app (`~/05_Projects/OTEKH-Weather-App`) is the reference implementation.

## Package management: use nala, not apt

Same rule as `LINUX.md`: **always use `nala` instead of `apt`** on Raspberry Pi OS (Debian-based). Install once with `sudo apt update && sudo apt install nala`, then `sudo nala install <package>` everywhere — including inside install scripts (with an `apt-get` fallback for systems without nala).

## Base development environment

```bash
sudo nala update
sudo nala install git curl build-essential swig python3-dev fontconfig
curl -LsSf https://astral.sh/uv/install.sh | sh   # uv — manages Python + deps
```

- **uv-managed Python** ships with Tk built in — no `python3-tk` needed, and you get a modern Python regardless of the distro version.
- `swig`, `build-essential`, `python3-dev` are needed only if a wheel (e.g. `rpi-lgpio`) must build from source — install them lazily on failure rather than upfront.
- Enable hardware interfaces once: `sudo raspi-config` → Interface Options → **I2C** (and GPIO). Check `/dev/i2c-1` exists before assuming sensors work.

## Fonts on Tkinter

Tkinter loads fonts through fontconfig at process start and **cannot read WOFF2**. Use the TTFs in `install_fonts/*/ttf/`:

1. Bundle them in the app (e.g. `resources/fonts/`) with their `LICENSE.txt` files.
2. Install per-user before the Tk root is created — `otekh_shell.ensure_fonts()` does this (`~/.local/share/fonts/otekh/` + `fc-cache`); install scripts should do the same.
3. Each weight is a separate family name: `Bai Jamjuree SemiBold`, `Inter`, `Inter Medium`, `Inter SemiBold`. Request the family, not a weight flag.

## Hardware conventions

- **GPIO on Pi 5: `rpi-lgpio` only** — never `RPi.GPIO`. `adafruit-lgpio` provides prebuilt lgpio wheels.
- **I2C sensors**: `adafruit-circuitpython-*` libraries (`busio`, `adafruit_bme280`, `adafruit_ahtx0`, `adafruit_ads1x15`, …).
- Keep **all hardware I/O in one module**; catch exceptions and surface failures as `None` so the UI shows `--` instead of crashing.
- Run `GPIO.cleanup()` on exit; run sensor reads off the UI thread (or keep them fast inside `after()` polls).

## Desktop integration

- `.desktop` entry in `~/.local/share/applications/`, icon in `~/.local/share/icons/hicolor/<size>/apps/`, launcher script in `~/.local/bin/` that exports `DISPLAY=:0` and runs `uv run --directory <repo> <app>`.
- XDG paths per `LINUX.md`: app data in `~/.local/share/<app>/`, fonts in `~/.local/share/fonts/<app>/`.
- Icon sizes per `docs/ICON_AND_LOGO_RULES.md`; the app window icon is set with `iconphoto()`.

## Install / update / uninstall pattern

Ship three scripts (see the Weather app for a working set):

- `scripts/install.sh` — installs `uv` if missing, `uv sync` (venv + deps), copies icon/wordmark/fonts, writes launcher + `.desktop`, warns if `/dev/i2c-1` is absent. Uses nala→apt fallback for system packages.
- `scripts/update.sh` — `git pull --ff-only` then re-runs the installer; skips gracefully when offline or not a git checkout.
- `scripts/uninstall.sh` — removes launcher, icon, fonts, `.desktop`, app share dir; leaves `.venv/` (inside the repo) and `uv` itself.

**In-app updates** (optional, recommended for distributed devices): `git fetch` + commits-behind count on a worker thread, `GIT_TERMINAL_PROMPT=0` so auth failures never hang, deferred-update flag in `~/.local/share/<app>/`, run `update.sh` and restart via `os.execv(sys.executable, [sys.executable, "-m", "<pkg>"])`. External users get the same flow for free as long as their clone can read the remote — public repo needs nothing extra.

## Performance on Pi

- Keep widget counts modest; prefer `pack`/`grid` over deep nesting.
- Poll sensors with `after()` (1 s is typical); never block the mainloop on I2C, network, or `git` — use worker threads + `after(0, ...)`.
- No animation beyond what confirms state; the design system forbids decorative motion anyway.

## Pi test checklist

- Clean Raspberry Pi OS install: `./scripts/install.sh` works end-to-end (uv, deps incl. any source builds, fonts, menu entry).
- Launch from the app menu and from `uv run <app>`; window icon and wordmark render.
- Bundled fonts render (Bai Jamjuree headings, Inter UI) — check `fc-list | grep -i "bai\|inter"` if they fall back.
- Sensors absent → `--` values and a degraded status-bar state, no crash.
- I2C disabled → clear failure state, not a hang.
- Update flow: check → update → restart; deferred update shows the reminder dot and re-asks on launch.
- Offline start works; update check fails cleanly without hanging.

See `Otekh_App_Shell/docs/QA_CHECKLIST.md` for the full release checklist.
