# OTEKH in Tkinter — Applying the Shell to Python Desktop Apps

How to build an OTEKH-looking application with Tkinter/CustomTkinter — the
reference stack for Raspberry Pi local apps and lightweight desktop tools.
For macOS/Linux desktop apps where aesthetics is the priority, use
PySide6/Qt instead — see `NATIVE_DESKTOP.md` for the non-webapp design
approach, frontend dispatch, and desktop conventions.
The design system itself is unchanged: same tokens, same fonts, same
layout regions. This file only covers the translation.

## What ships for Tkinter

| Piece | Location | Purpose |
|---|---|---|
| Python tokens | `tokens/otekh_tokens.py` | Every colour/font/geometry value as constants — import, never copy hex values |
| TTF fonts | `install_fonts/*/ttf/` | Tkinter-compatible builds of Bai Jamjuree + Inter (Tk cannot load WOFF2) |
| Shell toolkit | `tkinter/otekh_shell.py` | AppBar, NavRail, Panel, DataWell, StatusBar, Dialog, button factories, font bootstrap |
| Reference app | `starter/starter-shell-tkinter.py` | Runnable five-region layout — the twin of `starter-shell.html` |

## Stack

- **CustomTkinter** (`customtkinter`) on top of Tkinter — themed frames,
  buttons, labels, images. Pillow for image loading.
- **Python via uv** — uv-managed CPython ships with Tk built in, so no
  system `python3-tk` is needed. On Raspberry Pi OS this avoids the
  distro's older Python entirely.
- All widget styling is explicit (`fg_color`, `border_color`,
  `corner_radius`, `font`) — do not rely on CTk appearance themes.

## Fonts: the one rule that bites

Tkinter resolves fonts through **fontconfig at process start**. Therefore:

1. Ship the TTFs from `install_fonts/*/ttf/` inside the app (e.g.
   `resources/fonts/`). Keep `LICENSE.txt` beside them.
2. Call `otekh_shell.ensure_fonts(font_dirs)` **before** creating the CTk
   root — it copies TTFs to `~/.local/share/fonts/otekh/` and runs
   `fc-cache`. Skips cleanly when fonts are already installed.
3. Resolve families after the root exists with `Fonts()` — it picks the
   installed family or falls back to `TkDefaultFont`.

**Each weight is a separate family name.** Request the family, never a
weight flag:

| Role | Family to request |
|---|---|
| Display (product name, titles) | `Bai Jamjuree SemiBold` |
| UI regular | `Inter` |
| UI medium (nav, card titles) | `Inter Medium` |
| UI semibold (controls, values) | `Inter SemiBold` |

## Token → widget mapping

| Shell concept | Tkinter implementation |
|---|---|
| `surface.chrome` app bar (64 px) | `AppBar` — `CTkFrame(fg_color=CHROME, height=64)` + 3 px gold rule frame |
| `surface.canvas` workspace | root `fg_color=CANVAS` + canvas `CTkFrame` |
| `surface.panel` cards | `Panel` — `fg_color=PANEL, border_width=1, border_color=BORDER, corner_radius=4` |
| Dark data surfaces | `DataWell` — `fg_color=CHROME, corner_radius=2`, text in `TEXT_INVERSE`/status colours |
| `surface.recessed` nav | `NavRail` — recessed bg, 3 px gold accent on selected item |
| Status bar (44 px) | `StatusBar` — `fg_color=CHROME, height=44`, left/right slots |
| `action.primary` | `primary_button` — gold fill, charcoal text, `ACTION_PRESSED` hover |
| Secondary control | `secondary_button` (light) / `chrome_button` (on dark chrome) |
| Focus ring | Tk has no `:focus-visible` outline — keep `border_color=BORDER_STRONG` on focused entries if needed |
| Radius | `RADIUS_CONTROL=2` controls, `RADIUS_CONTAINER=4` panels/dialogs — no larger |
| Spacing | `SPACE_*` constants for padx/pady — 4 px base unit |

## Layout recipe (five regions)

```python
shell.ensure_fonts([...])          # before CTk()
app = ctk.CTk()
fonts = shell.Fonts()              # after root exists

bar = shell.AppBar(app, fonts, title="APP NAME", context="Context")
bar.pack(fill="x")                 # gold rule is built in

status = shell.StatusBar(app, fonts)
status.pack(fill="x", side="bottom")   # BEFORE the expanding canvas

nav = shell.NavRail(app, fonts, items=[...])      # optional
nav.pack(fill="y", side="left")

inspector = shell.Panel(app, width=T.INSPECTOR)   # optional
inspector.pack(fill="y", side="right")

canvas = ctk.CTkFrame(app, fg_color=T.SURFACE_CANVAS)
canvas.pack(expand=True, fill="both")             # last — fills the rest
```

Order matters: pack the bottom bar before the expanding canvas, and side
regions before the centre.

## Behaviour rules that carry over

- **Status colours always pair with text or an icon** — never colour alone.
- **Live data**: poll with `root.after(ms, fn)`; run blocking I/O (network,
  `git`, sensors) on worker threads and marshal UI changes back through
  `self.after(0, ...)`.
- **Local and durable**: show where data lives and whether it is flowing
  (e.g. `● ON-DEVICE`, `● ALL SYSTEMS OPERATIONAL` in the status bar).
- **No gradients, shadows, gloss, or decorative animation.** Tkinter makes
  most of these hard anyway — keep it that way.
- **Dialogs**: `shell.Dialog` gives a modal panel-surface window with a
  Bai Jamjuree title and a button row; primary action is gold, on the right.

## Raspberry Pi specifics

See `../../RASPBERRY_PI.md` — GPIO/I2C libraries, `raspi-config`, desktop
integration, install/update script patterns, and the Pi test checklist.
