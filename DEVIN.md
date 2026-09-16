# DEVIN.md — OTEKH Apps Design 2026

Agent instructions for working with this folder. General development rules live in `../agent.md` — read that first; this file adds OTEKH-specific rules.

## What this folder is

The standing design system and process guide for building **OTEKH applications**. When the user asks to build an app and confirms it is an OTEKH app (or says so upfront), this folder is the authoritative reference.

## Trigger behaviour

- If the user asks for app building **without specifying** whether it is an OTEKH app, ask: "Is this an OTEKH app?"
- If yes (or already specified): follow `OTEKH_App_Startup_Instructions_v1.1.txt` as the process and treat `Otekh_App_Shell/` as the authoritative visual/interface system.
- If no: proceed normally under `../agent.md` rules.

## Process (from the startup instructions)

1. **Do not code immediately.** After loading the guide, ask "What are we building?"
2. **Discovery** — work conversationally to define purpose, users, data, tasks, screens, offline needs, and first-version scope.
3. **Layout exploration** — present 2–3 plain-text layout options before coding.
4. **Approval point** — confirm a compact summary (name, purpose, v1 features, layout, screens, inputs, platforms, deferred items) before building.
5. **Build** — smallest useful working version first, in testable pieces: shell/layout → data loading → work view → controls → inspectors → save/export → accessibility/error states → packaging.
6. **Iterate** — Build → Run → Test → Discuss → Revise → Add. Preserve approved work; change only what is being discussed.

## Hard rules

- **The Shell is authoritative.** Do not redesign, recolour, substitute fonts, recreate logos, or add gradients/shadows/gloss. Use exact tokens and supplied assets.
- **Platforms: macOS + Linux only**, planned from the start. No Windows work unless explicitly requested. Linux specifics: `LINUX.md`.
- **Fonts**: bundle `install_fonts/` files with the app; keep licences; no runtime font downloads.
- **Assets**: use supplied logos/icons as-is (`Assets/`). Never invent replacements.
- **New components** may extend the Shell but must follow its tokens, geometry, typography, accessibility, and interaction rules.

## Folder map

```
OTEKH_Apps_Design_2026/
├── README.md                                # overview and entry point
├── OTEKH_App_Startup_Instructions_v1.1.txt   # process — read first
├── DEVIN.md                                 # this file
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
    ├── starter/starter-shell.html           # reference layout (top bar / nav / canvas / inspector / status)
    ├── tokens/                              # design-tokens.json, otekh-tokens.css, otekh-theme.ts
    └── _OTEKH_Application_Style_Guide_Final.pdf
```

## Known discrepancies (flag to user, don't silently "fix")

- `docs/FONTS.md` and `docs/STYLE_GUIDE.md` specify **IBM Plex Sans Condensed** (UI) and **IBM Plex Mono** (data), but the bundled fonts and all token files use **Inter** for both UI and mono roles. Until the user resolves this, the bundled fonts (Bai Jamjuree + Inter) are what actually ship — treat tokens/CSS as the working truth and ask before changing either side.
- `starter/starter-shell.html` and `components/component-gallery.html` contain leftover MSO/SharePoint XML comments — harmless, ignore.

## Before release

Run `Otekh_App_Shell/docs/QA_CHECKLIST.md` (identity, visual system, interaction, accessibility, data/trust, platform) plus the Linux checklist in `LINUX.md`.
