# Changelog

## 1.2.0 — 2026-10-01

Aligned the Shell with the shipped apps (OTEKH Lab Workspace, OTEKH Data
Cleaning) and added the no-cookie ethics protocol.

- Added shared app chrome to `components/otekh-components.css`: `.otekh-topbar` (brand + context + status + user menu), `.otekh-statusbar`, `.otekh-toolbar`.
- Added the dropdown menu system: `.otekh-menu` / `.otekh-menu__btn` / `.otekh-menu__drop` / `.otekh-menu-item`, with `--warn`/`--danger` severity items, `.menuitem-admin` role gating, and the `.otekh-menu--toolbar` left-aligned variant for Project/Workspace switchers.
- Added `.otekh-login` sign-in card (masked password, inline error), `.otekh-landing`/`.otekh-tiles` tool chooser, and `.otekh-modal` overlay dialogs.
- `otekh-components.css` now `@import`s `tokens/otekh-tokens.css` and reads `--otekh-*` tokens directly; the old unprefixed variables remain as aliases for compatibility.
- `starter/starter-shell.html` uses the shared chrome classes, includes the canonical user menu, and ships the standard menu toggle script.
- Added `docs/SECURITY_PRIVACY.md` — the no-cookie ethics protocol (zero cookie tracking; header-token sessions; optional single-session-cookie fallback), plus the shared auth-file, masked-password, and role/admin patterns.
- `docs/STYLE_GUIDE.md` §7 documents the menu-toolbar navigation pattern and user menu; new §14 covers privacy/security.
- `docs/COMPONENT_SPECS.md` gained Dropdown menus, Sign-in card, Landing tiles, and Modals sections.
- `docs/QA_CHECKLIST.md` gained a Privacy and security section.
- Startup instructions bumped to v1.3 (`../../OTEKH_App_Startup_Instructions_v1.3.txt`).

## 1.1.0 — 2026-09-19

- Added Tkinter/CustomTkinter support for local desktop and Raspberry Pi apps.
- Added `tokens/otekh_tokens.py` — Python export of the design tokens (no value changes).
- Added `install_fonts/*/ttf/` — TTF builds of Bai Jamjuree + Inter for Tkinter (WOFF2 unsupported by Tk).
- Added `tkinter/otekh_shell.py` — reusable shell components (app bar, nav rail, panel, data well, status bar, dialog, buttons, font bootstrap).
- Added `starter/starter-shell-tkinter.py` — runnable five-region reference layout.
- Added `docs/TKINTER.md` — token→widget mapping and behaviour rules.
- Added `../RASPBERRY_PI.md` — Pi OS platform guideline (hardware, fonts, packaging, updates).

## 1.0.0 — 2026-07-24

- Established the OTEKH application colour, typography, spacing, geometry, and motion systems.
- Added cross-platform layout and component guidance.
- Added archive, AI, media, sensor, local-first, permissions, and provenance requirements.
- Added accessibility and release QA standards.
- Added JSON, CSS, and TypeScript design-token exports.
- Organized supplied logo, banner, icon, and interface reference assets.

