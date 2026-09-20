# OTEKH Apps Design 2026

The standing design system and process guide for building **OTEKH applications** — universal desktop apps for **macOS and Linux** (no Windows unless explicitly requested).

## How to use this folder

1. **Start here**: `OTEKH_App_Startup_Instructions_v1.2.txt` — the process for every new OTEKH app (discovery → layout options → approval → build in pieces → iterate).
2. **Design source of truth**: `Otekh_App_Shell/` — tokens, components, fonts, assets, and docs. Treat it as authoritative; do not redesign or substitute.
3. **Platform specifics**: `LINUX.md` and `MACOS.md` — environment setup, fonts, paths, packaging, and testing. `RASPBERRY_PI.md` — Pi OS + Tkinter/CustomTkinter for local apps (sensor stations, kiosks). `WINDOWS.md` exists only for projects where the user explicitly requests Windows (not a default target).
4. **Agent instructions**: `DEVIN.md` — how an AI assistant should apply this guide.

## Contents

```
OTEKH_Apps_Design_2026/
├── README.md                                # this file
├── OTEKH_App_Startup_Instructions_v1.2.txt  # process — read first
├── DEVIN.md                                 # agent instructions (DEVIN)
├── agent.md                                 # agent instructions (any agent)
├── LINUX.md                                 # Linux setup/packaging/testing
├── MACOS.md                                 # macOS setup/packaging/testing
├── RASPBERRY_PI.md                          # Pi OS + Tkinter for local apps
├── WINDOWS.md                               # Windows — only when explicitly requested
└── Otekh_App_Shell/                         # authoritative design system
    ├── Assets/                              # logos, app icons, UI reference image
    ├── components/                          # otekh-components.css + component-gallery.html
    ├── docs/                                # STYLE_GUIDE, COMPONENT_SPECS, FONTS, TKINTER,
    │                                        # ICON_AND_LOGO_RULES, ACCESSIBILITY, QA_CHECKLIST
    ├── install_fonts/                       # Bai Jamjuree + Inter WOFF2 + licences;
    │                                        # */ttf/ TTF builds for Tkinter
    ├── tkinter/                             # otekh_shell.py — CustomTkinter shell toolkit
    ├── Log/CHANGELOG.md                     # design-system version history
    ├── starter/                             # starter-shell.html + starter-shell-tkinter.py
    ├── tokens/                              # design-tokens.json, otekh-tokens.css,
    │                                        # otekh-theme.ts, otekh_tokens.py
    └── _OTEKH_Application_Style_Guide_Final.pdf
```

## Quick preview

Open these in a browser to see the system:

- `Otekh_App_Shell/starter/starter-shell.html` — the five-region app layout (top bar, nav, canvas, inspector, status bar).
- `Otekh_App_Shell/components/component-gallery.html` — every styled component.

For correct fonts in the preview, install the bundled fonts first — see `LINUX.md`.

## Core rules in one paragraph

The Shell is authoritative: use the exact tokens, bundled fonts (Bai Jamjuree + Inter), and supplied logos/icons — no redesigns, recolours, gradients, or invented assets. Gold is for selection and primary action only. Build for macOS and Linux from day one, offline-capable, accessible (WCAG 2.2 AA), and in small testable pieces. All code must be human-readable source — never binary or machine-language-only deliverables — structured for cross-OS functionality (macOS + Linux priority, Windows only on request), and maintainable by a human user without agent assistance. New components may extend the Shell but must follow its rules.
