"""OTEKH design tokens for Python/Tkinter applications.

Mirrors design-tokens.json (same directory) so Tkinter apps use the exact
same values as the CSS/TS token files — do not substitute colours, spacing,
or radii. Import this module instead of copying hex values into app code.

PROVIDES: all token constants below; consumed by tkinter/otekh_shell.py and
          by OTEKH Tkinter apps (e.g. Raspberry Pi local apps).
CONSUMES: nothing — this file is the source of truth alongside
          design-tokens.json and otekh-tokens.css.
"""

# --- Brand colours ---

BRAND_OLIVE = "#646A44"  # identity, logo, selected family surfaces
BRAND_GOLD = "#CAA133"  # brand accent, icons, highlights
BRAND_BLACK = "#000000"  # pictograms and highest-contrast marks
BRAND_SILVER = "#C0C0C0"  # small logo details only

# --- Interface surfaces (light theme — the OTEKH default) ---

SURFACE_CHROME = "#282B24"  # top/bottom chrome, dark panels, data wells
SURFACE_DARK_OLIVE = "#4E4F37"  # secondary dark surface, hover on chrome
SURFACE_CANVAS = "#C1C1BD"  # principal light workspace
SURFACE_PANEL = "#C7C7C4"  # cards, inspectors, grouped regions
SURFACE_RECESSED = "#ADACA6"  # selected wells, inactive fields, nav surface
SURFACE_MUTED = "#818377"  # secondary navigation, disabled regions

# --- Borders ---

BORDER_DEFAULT = "#818377"  # panel and control borders
BORDER_STRONG = "#606255"  # focused structure, dark-light boundaries

# --- Text ---

TEXT_PRIMARY = "#282B24"  # on light surfaces
TEXT_SECONDARY = "#4E4F37"  # secondary on light
TEXT_INVERSE = "#F0F0EA"  # on dark chrome
TEXT_INVERSE_MUTED = "#C7C7C4"  # secondary on dark chrome
TEXT_DISABLED = "#606255"  # disabled

# --- Actions ---

ACTION_PRIMARY = "#CFA134"  # selected tab, primary action, active data
ACTION_PRESSED = "#B28926"  # pressed/active interaction state
ACTION_FOCUS = "#CAA133"  # focus ring (same as brand gold)

# --- Status (always pair with text or an icon — never colour alone) ---

STATUS_GOOD = "#AEC76F"  # connected, valid, operational
STATUS_ATTENTION = "#CFA134"  # review, pending, changed
STATUS_ERROR = "#A52B32"  # failed, blocked, destructive
STATUS_INFO = "#5C7880"  # neutral system information

# --- Dark theme overrides (mirrors [data-otekh-theme="dark"] in CSS) ---

DARK_SURFACE_CANVAS = "#282B24"
DARK_SURFACE_PANEL = "#3D4135"
DARK_SURFACE_RECESSED = "#4E4F37"
DARK_TEXT_PRIMARY = "#F0F0EA"
DARK_TEXT_SECONDARY = "#C7C7C4"
DARK_BORDER = "#606255"

# --- Typography ---

# Tkinter resolves fonts by family name through fontconfig; each bundled
# weight installs as its OWN family, so pick the family, not a weight flag.
# (CSS stacks are in design-tokens.json; these are the installed TTF names.)
FONT_DISPLAY = "Bai Jamjuree SemiBold"  # product name, page/section titles
FONT_DISPLAY_MEDIUM = "Bai Jamjuree Medium"
FONT_DISPLAY_REGULAR = "Bai Jamjuree"
FONT_UI = "Inter"  # labels, body, status text
FONT_UI_MEDIUM = "Inter Medium"  # navigation, card titles
FONT_UI_SEMIBOLD = "Inter SemiBold"  # controls, data values
# Fallbacks if the bundled fonts are not installed:
FONT_FALLBACK = "TkDefaultFont"

# Weights (for reference — Tk uses the per-weight family names above)
WEIGHT_REGULAR = 400
WEIGHT_MEDIUM = 500
WEIGHT_SEMIBOLD = 600

# --- Spacing (4 px base unit) ---

SPACE_1 = 4
SPACE_2 = 8
SPACE_3 = 12
SPACE_4 = 16
SPACE_6 = 24
SPACE_8 = 32
SPACE_12 = 48
SPACE_16 = 64

# --- Sizes ---

CONTROL_COMPACT = 32  # compact control height
CONTROL_DEFAULT = 40  # default control height
CONTROL_TOUCH = 44  # touch-capable control height
APP_BAR = 64  # top application bar height
STATUS_BAR = 44  # bottom status bar height
SIDEBAR = 256  # left navigation width (240–280 acceptable)
INSPECTOR = 320  # right inspector width (300–360 acceptable)
GOLD_RULE = 3  # harvest-gold rule under the app bar (starter shell)

# --- Borders / radii ---

BORDER_WIDTH = 1
RADIUS_CONTROL = 2  # buttons, inputs, data wells
RADIUS_CONTAINER = 4  # panels, dialogs, app-level containers

# --- Motion (ms — Tkinter has no CSS transitions; keep animation minimal) ---

MOTION_FAST = 100
MOTION_PANEL = 180

# --- Breakpoints ---

BREAKPOINT_COMPACT = 720  # below: single column, collapse nav/inspector
BREAKPOINT_WIDE = 1200
