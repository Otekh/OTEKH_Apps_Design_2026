# OTEKH Apps Design 2026

The standing design system and process guide for building **OTEKH applications** — universal desktop apps for **macOS and Linux** (no Windows unless explicitly requested).

## How to use this folder

1. **Start here**: `OTEKH_App_Startup_Instructions_v1.1.txt` — the process for every new OTEKH app (discovery → layout options → approval → build in pieces → iterate).
2. **Design source of truth**: `Otekh_App_Shell/` — tokens, components, fonts, assets, and docs. Treat it as authoritative; do not redesign or substitute.
3. **Platform specifics**: `LINUX.md` and `MACOS.md` — environment setup, fonts, paths, packaging, and testing. `WINDOWS.md` exists only for projects where the user explicitly requests Windows (not a default target).
4. **Agent instructions**: `DEVIN.md` — how an AI assistant should apply this guide.

## Contents

```
OTEKH_Apps_Design_2026/
├── README.md                                # this file
├── OTEKH_App_Startup_Instructions_v1.1.txt  # process — read first
├── DEVIN.md                                 # agent instructions
├── LINUX.md                                 # Linux setup/packaging/testing
├── MACOS.md                                 # macOS setup/packaging/testing
├── WINDOWS.md                               # Windows — only when explicitly requested
└── Otekh_App_Shell/                         # authoritative design system
    ├── Assets/                              # logos, app icons, UI reference image
    ├── components/                          # otekh-components.css + component-gallery.html
    ├── docs/                                # STYLE_GUIDE, COMPONENT_SPECS, FONTS,
    │                                        # ICON_AND_LOGO_RULES, ACCESSIBILITY, QA_CHECKLIST
    ├── install_fonts/                       # Bai Jamjuree + Inter WOFF2 + licences
    ├── Log/CHANGELOG.md                     # design-system version history
    ├── starter/starter-shell.html           # reference app layout
    ├── tokens/                              # design-tokens.json, otekh-tokens.css, otekh-theme.ts
    └── _OTEKH_Application_Style_Guide_Final.pdf
```

## Quick preview

Open these in a browser to see the system:

- `Otekh_App_Shell/starter/starter-shell.html` — the five-region app layout (top bar, nav, canvas, inspector, status bar).
- `Otekh_App_Shell/components/component-gallery.html` — every styled component.

For correct fonts in the preview, install the bundled fonts first — see `LINUX.md`.

## Core rules in one paragraph

The Shell is authoritative: use the exact tokens, bundled fonts (Bai Jamjuree + Inter), and supplied logos/icons — no redesigns, recolours, gradients, or invented assets. Gold is for selection and primary action only. Build for macOS and Linux from day one, offline-capable, accessible (WCAG 2.2 AA), and in small testable pieces. New components may extend the Shell but must follow its rules.
