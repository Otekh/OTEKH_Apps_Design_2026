# DEVIN.md — OTEKH Apps Design 2026

Agent instructions for working with this folder. General development rules live in `../agent.md` — read that first; this file adds OTEKH-specific rules.

## What this folder is

The standing design system and process guide for building **OTEKH applications**. When the user asks to build an app and confirms it is an OTEKH app (or says so upfront), this folder is the authoritative reference.

## Trigger behaviour

- If the user asks for app building **without specifying** whether it is an OTEKH app, ask: "Is this an OTEKH app?"
- If yes (or already specified): follow `OTEKH_App_Startup_Instructions_v1.3.txt` as the process and treat `Otekh_App_Shell/` as the authoritative visual/interface system.
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
- **Human-readable, human-editable code.** Apps must be written in a human-readable programming language — never delivered as binary or machine-language-only artifacts. Code must be clear and maintainable enough that a human user can make changes without agent assistance: sensible structure, meaningful names, comments where needed, no obfuscation or opaque generated-only code.
- **Cross-OS by design.** Structure all code for cross-platform functionality from the start — macOS and Linux are the priority targets; add Windows only when the user explicitly requests it. No platform-locked implementation choices without an equivalent on the other target.
- **Platforms: macOS + Linux only**, planned from the start. No Windows work unless explicitly requested. Linux specifics: `LINUX.md`.
- **Fonts**: bundle `install_fonts/` files with the app; keep licences; no runtime font downloads.
- **Assets**: use supplied logos/icons as-is (`Assets/`). Never invent replacements.
- **New components** may extend the Shell but must follow its tokens, geometry, typography, accessibility, and interaction rules.
- **No-cookie ethics protocol.** Web apps must function fully and securely with zero cookie tracking — no analytics, advertising, fingerprinting, or third-party identifiers. Sessions are header tokens (`Authorization: Bearer` / `X-Session-Token`); at most one optional first-party `HttpOnly; SameSite=Lax` session-cookie fallback, never required. Passwords masked and salted+hashed; bootstrap credentials in a gitignored `auth` file; admin features hidden per role in the UI and enforced server-side. Full spec: `Otekh_App_Shell/docs/SECURITY_PRIVACY.md`.

## Commenting standards

All code in OTEKH apps follows this standard, written as you code — never deferred. If a project's existing commenting exceeds it, match the higher standard.

- **File header**: every source file opens with a docstring (Python) or block comment (JS/CSS/HTML) stating what the file owns — which globals/functions it PROVIDES and which it CONSUMES, naming the source file for each (e.g. `App.api` from app.js, `WeatherStation` from sensors.py).
- **Import blocks**: comment what each import is for, especially imports from other project files (name the file and what it provides).
- **Section banners**: `# ---` / `/* --- */` banners separate major areas so readers can navigate.
- **Cross-file call sites**: when code calls a function or uses a global defined in another file and the relationship isn't obvious, add an inline note naming the source file.
- **Explain WHY and WHERE-FROM, not WHAT** — capture intent, data flow, and non-obvious constraints; don't narrate code line by line.
- **No stale comments** — if a change makes a comment wrong, fix or remove it in the same edit.

## Folder map

```
OTEKH_Apps_Design_2026/
├── README.md                                # overview and entry point
├── OTEKH_App_Startup_Instructions_v1.3.txt   # process — read first
├── DEVIN.md                                 # this file
├── agent.md                                 # same rules for non-DEVIN agents
├── LINUX.md                                 # Linux setup/packaging/testing
├── MACOS.md                                 # macOS setup/packaging/testing
├── RASPBERRY_PI.md                          # Pi OS + Tkinter for local apps
├── WINDOWS.md                               # Windows — only when explicitly requested
└── Otekh_App_Shell/                         # authoritative design system
    ├── Assets/                              # logos, app icons, UI reference image
    ├── components/                          # otekh-components.css + component-gallery.html
    ├── docs/                                # STYLE_GUIDE, COMPONENT_SPECS, FONTS, TKINTER,
    │                                        # NATIVE_DESKTOP (non-webapp design approach),
    │                                        # ICON_AND_LOGO_RULES, ACCESSIBILITY, QA_CHECKLIST,
    │                                        # SECURITY_PRIVACY (no-cookie protocol + auth/admin)
    ├── install_fonts/                       # Bai Jamjuree + Inter WOFF2 + licences;
    │                                        # */ttf/ TTF builds for Tkinter
    ├── tkinter/                             # otekh_shell.py — CustomTkinter shell toolkit
    ├── Log/CHANGELOG.md                     # design-system version history
    ├── starter/                             # starter-shell.html + starter-shell-tkinter.py
    ├── tokens/                              # design-tokens.json, otekh-tokens.css,
    │                                        # otekh-theme.ts, otekh_tokens.py
    └── _OTEKH_Application_Style_Guide_Final.pdf
```

## Known discrepancies (flag to user, don't silently "fix")

- `docs/FONTS.md` and `docs/STYLE_GUIDE.md` specify **IBM Plex Sans Condensed** (UI) and **IBM Plex Mono** (data), but the bundled fonts and all token files use **Inter** for both UI and mono roles. Until the user resolves this, the bundled fonts (Bai Jamjuree + Inter) are what actually ship — treat tokens/CSS as the working truth and ask before changing either side.
- `starter/starter-shell.html` and `components/component-gallery.html` contain leftover MSO/SharePoint XML comments — harmless, ignore.

## Before release

Run `Otekh_App_Shell/docs/QA_CHECKLIST.md` (identity, visual system, interaction, accessibility, data/trust, platform) plus the Linux checklist in `LINUX.md`.
