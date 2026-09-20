"""OTEKH shell components for CustomTkinter applications.

Drop-in toolkit that renders the OTEKH design system in Tkinter: the
chrome app bar with gold rule, left nav rail, bordered panels, dark data
wells, status bar, OTEKH-styled buttons, and modal dialogs — all driven by
tokens/otekh_tokens.py so values match the CSS/TS design system exactly.

Copy this file (and tokens/otekh_tokens.py) into a project, or import it
in place. Requires: customtkinter, Pillow (only for wordmark images).

PROVIDES: ensure_fonts(), Fonts, AppBar, NavRail, Panel, DataWell,
          StatusBar, Dialog, primary_button(), secondary_button().
CONSUMES: otekh_tokens.py (../tokens/) for every colour, font, and
          geometry value; install_fonts/*/ttf/ for bundled fonts.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tkinter.font as tkfont
from pathlib import Path

import customtkinter as ctk

# Locate the token module whether this file lives in the Shell layout
# (tkinter/ next to tokens/) or was copied into a project alongside it.
_HERE = Path(__file__).resolve().parent
for _candidate in (_HERE / ".." / "tokens", _HERE):
    if (_candidate / "otekh_tokens.py").exists():
        sys.path.insert(0, str(_candidate.resolve()))
        break
import otekh_tokens as T  # noqa: E402  (path fix must precede import)


# --- Fonts ---------------------------------------------------------------


def ensure_fonts(font_dirs: list[Path] | None = None) -> None:
    """Install bundled OTEKH TTFs so Tk can resolve them by family name.

    Tkinter discovers fonts through fontconfig at startup, so call this
    BEFORE creating the CTk root. Pass the directories that contain the
    bundled .ttf files (e.g. install_fonts/Bai_Jamjuree/ttf and
    install_fonts/Inter/ttf, or a project's resources/fonts/). Files are
    copied to ~/.local/share/fonts/otekh and fc-cache is refreshed; both
    steps are skipped when the families are already installed or the tools
    are missing (the UI then falls back to system fonts).
    """
    if font_dirs is None:
        shell_fonts = _HERE / ".." / "install_fonts"
        font_dirs = sorted(shell_fonts.glob("*/ttf")) if shell_fonts.is_dir() else []
    font_dirs = [d for d in font_dirs if Path(d).is_dir()]
    if not font_dirs:
        return

    # Fast path: both families already known to fontconfig.
    if shutil.which("fc-list"):
        try:
            out = subprocess.run(
                ["fc-list", ":", "family"],
                capture_output=True,
                text=True,
                timeout=10,
            ).stdout
            if "Bai Jamjuree" in out and "Inter" in out:
                return
        except (OSError, subprocess.SubprocessError):
            pass

    dst = Path.home() / ".local" / "share" / "fonts" / "otekh"
    try:
        dst.mkdir(parents=True, exist_ok=True)
        for d in font_dirs:
            for ttf in Path(d).glob("*.ttf"):
                target = dst / ttf.name
                if not target.exists():
                    shutil.copy2(ttf, target)
        if shutil.which("fc-cache"):
            subprocess.run(
                ["fc-cache", "-f", str(dst)], capture_output=True, timeout=30
            )
    except OSError:
        pass  # read-only home or similar — run with fallback fonts


class Fonts:
    """Resolved OTEKH font families + CTkFont factories.

    Create once, AFTER the Tk root exists (tkfont.families() needs it).
    Each bundled weight is a separate family name, so weight selection is
    done by family — never by Tk's weight flag.
    """

    def __init__(self) -> None:
        available = set(tkfont.families())
        self.display = self._pick(
            available, [T.FONT_DISPLAY, T.FONT_DISPLAY_REGULAR]
        )
        self.ui = self._pick(available, [T.FONT_UI])
        self.ui_medium = self._pick(available, [T.FONT_UI_MEDIUM, T.FONT_UI])
        self.ui_semibold = self._pick(
            available, [T.FONT_UI_SEMIBOLD, T.FONT_UI]
        )

    @staticmethod
    def _pick(available: set[str], candidates: list[str]) -> str:
        for name in candidates:
            if name in available:
                return name
        return T.FONT_FALLBACK

    def display_font(self, size: int) -> ctk.CTkFont:
        return ctk.CTkFont(family=self.display, size=size)

    def ui_font(self, size: int) -> ctk.CTkFont:
        return ctk.CTkFont(family=self.ui, size=size)

    def ui_medium_font(self, size: int) -> ctk.CTkFont:
        return ctk.CTkFont(family=self.ui_medium, size=size)

    def ui_semibold_font(self, size: int) -> ctk.CTkFont:
        return ctk.CTkFont(family=self.ui_semibold, size=size)


# --- Chrome regions --------------------------------------------------------


class AppBar(ctk.CTkFrame):
    """Top application bar: 64 px charcoal + 3 px harvest-gold rule.

    pack(fill="x") at the top of the window. `title` renders in Bai
    Jamjuree (product name), `context` in muted Inter. Pack controls into
    `self.right` with side="right" for status indicators and buttons.
    """

    def __init__(
        self,
        master,
        fonts: Fonts,
        title: str = "",
        context: str = "",
        wordmark: ctk.CTkImage | None = None,
    ) -> None:
        super().__init__(
            master, fg_color=T.SURFACE_CHROME, corner_radius=0, height=T.APP_BAR
        )
        self.pack_propagate(False)

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=T.SPACE_4)

        if wordmark is not None:
            ctk.CTkLabel(inner, image=wordmark, text="").pack(side="left")

        if title:
            ctk.CTkLabel(
                inner,
                text=title,
                font=fonts.display_font(20),
                text_color=T.TEXT_INVERSE,
            ).pack(side="left", padx=(T.SPACE_3 if wordmark else 0, 0))

        if context:
            ctk.CTkLabel(
                inner,
                text=context,
                font=fonts.ui_font(12),
                text_color=T.TEXT_INVERSE_MUTED,
            ).pack(side="left", padx=(T.SPACE_4, 0))

        # Right-side slot: pack status indicators/buttons side="right".
        self.right = ctk.CTkFrame(inner, fg_color="transparent")
        self.right.pack(side="right")

        # Harvest-gold rule separating chrome from canvas (starter shell).
        self.rule = ctk.CTkFrame(
            master, fg_color=T.BRAND_GOLD, corner_radius=0, height=T.GOLD_RULE
        )
        self.rule.pack(fill="x", side="bottom")
        self.rule.pack_propagate(False)


class StatusBar(ctk.CTkFrame):
    """Bottom status bar: 44 px charcoal with left/right text slots.

    pack(fill="x", side="bottom") BEFORE the expanding canvas so it keeps
    its height. Use set_left()/set_right() for status text.
    """

    def __init__(self, master, fonts: Fonts) -> None:
        super().__init__(
            master,
            fg_color=T.SURFACE_CHROME,
            corner_radius=0,
            height=T.STATUS_BAR,
        )
        self.pack_propagate(False)

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=T.SPACE_4)

        self._left = ctk.CTkLabel(
            inner,
            text="",
            font=fonts.ui_medium_font(11),
            text_color=T.TEXT_INVERSE_MUTED,
        )
        self._left.pack(side="left")

        self._right = ctk.CTkLabel(
            inner,
            text="",
            font=fonts.ui_font(11),
            text_color=T.TEXT_INVERSE_MUTED,
        )
        self._right.pack(side="right")

    def set_left(self, text: str, color: str = T.TEXT_INVERSE_MUTED) -> None:
        self._left.configure(text=text, text_color=color)

    def set_right(self, text: str, color: str = T.TEXT_INVERSE_MUTED) -> None:
        self._right.configure(text=text, text_color=color)


class NavRail(ctk.CTkFrame):
    """Left navigation on the recessed surface, gold mark on selection.

    items: list of labels. on_select(label) fires when an item is clicked.
    The selected item gets a 3 px gold left bar and semibold text, matching
    the starter shell's nav styling.
    """

    def __init__(
        self,
        master,
        fonts: Fonts,
        items: list[str],
        on_select=None,
        width: int = T.SIDEBAR,
    ) -> None:
        super().__init__(
            master,
            fg_color=T.SURFACE_RECESSED,
            corner_radius=0,
            width=width,
            border_color=T.BORDER_DEFAULT,
            border_width=0,
        )
        self.pack_propagate(False)
        self._fonts = fonts
        self._on_select = on_select
        self._rows: dict[str, tuple[ctk.CTkFrame, ctk.CTkLabel]] = {}
        self._selected: str | None = None

        for label in items:
            row = ctk.CTkFrame(self, fg_color="transparent")
            row.pack(fill="x", padx=(0, T.SPACE_2))
            accent = ctk.CTkFrame(
                row, fg_color="transparent", width=3, corner_radius=0
            )
            accent.pack(side="left", fill="y")
            accent.pack_propagate(False)
            btn = ctk.CTkButton(
                row,
                text=label,
                font=fonts.ui_medium_font(13),
                text_color=T.TEXT_PRIMARY,
                fg_color="transparent",
                hover_color=T.SURFACE_PANEL,
                anchor="w",
                height=T.CONTROL_COMPACT,
                corner_radius=0,
                command=lambda lbl=label: self.select(lbl),
            )
            btn.pack(side="left", fill="x", expand=True)
            self._rows[label] = (accent, btn)

    def select(self, label: str) -> None:
        """Mark an item current: gold accent bar + semibold label."""
        if self._selected in self._rows:
            accent, btn = self._rows[self._selected]
            accent.configure(fg_color="transparent")
            btn.configure(font=self._fonts.ui_medium_font(13))
        self._selected = label
        if label in self._rows:
            accent, btn = self._rows[label]
            accent.configure(fg_color=T.BRAND_GOLD)
            btn.configure(font=self._fonts.ui_semibold_font(13))
        if self._on_select:
            self._on_select(label)


# --- Surfaces --------------------------------------------------------------


class Panel(ctk.CTkFrame):
    """Raised panel: surface.panel, 1 px structural border, 4 px radius."""

    def __init__(self, master, **kwargs) -> None:
        kwargs.setdefault("fg_color", T.SURFACE_PANEL)
        kwargs.setdefault("border_color", T.BORDER_DEFAULT)
        kwargs.setdefault("border_width", T.BORDER_WIDTH)
        kwargs.setdefault("corner_radius", T.RADIUS_CONTAINER)
        super().__init__(master, **kwargs)


class DataWell(ctk.CTkFrame):
    """Dark recessed well for live data: charcoal, 2 px radius.

    Values on this surface use TEXT_INVERSE or status colours — matching
    the dark data surfaces in the OTEKH reference UI.
    """

    def __init__(self, master, **kwargs) -> None:
        kwargs.setdefault("fg_color", T.SURFACE_CHROME)
        kwargs.setdefault("corner_radius", T.RADIUS_CONTROL)
        super().__init__(master, **kwargs)


# --- Controls ----------------------------------------------------------------


def primary_button(
    master, text: str, command, fonts: Fonts, **kwargs
) -> ctk.CTkButton:
    """Gold primary action — one per control group (colour discipline)."""
    kwargs.setdefault("height", T.CONTROL_COMPACT)
    return ctk.CTkButton(
        master,
        text=text,
        font=fonts.ui_semibold_font(12),
        text_color=T.TEXT_PRIMARY,
        fg_color=T.ACTION_PRIMARY,
        hover_color=T.ACTION_PRESSED,
        corner_radius=T.RADIUS_CONTROL,
        command=command,
        **kwargs,
    )


def secondary_button(
    master, text: str, command, fonts: Fonts, **kwargs
) -> ctk.CTkButton:
    """Bordered secondary action on light surfaces."""
    kwargs.setdefault("height", T.CONTROL_COMPACT)
    return ctk.CTkButton(
        master,
        text=text,
        font=fonts.ui_medium_font(12),
        text_color=T.TEXT_PRIMARY,
        fg_color="transparent",
        hover_color=T.SURFACE_CANVAS,
        border_color=T.BORDER_DEFAULT,
        border_width=T.BORDER_WIDTH,
        corner_radius=T.RADIUS_CONTROL,
        command=command,
        **kwargs,
    )


def chrome_button(
    master, text: str, command, fonts: Fonts, **kwargs
) -> ctk.CTkButton:
    """Bordered button for dark chrome (app bar / status bar controls)."""
    kwargs.setdefault("height", T.CONTROL_COMPACT)
    return ctk.CTkButton(
        master,
        text=text,
        font=fonts.ui_medium_font(11),
        text_color=T.TEXT_INVERSE,
        fg_color="transparent",
        hover_color=T.SURFACE_DARK_OLIVE,
        border_color=T.BORDER_DEFAULT,
        border_width=T.BORDER_WIDTH,
        corner_radius=T.RADIUS_CONTROL,
        command=command,
        **kwargs,
    )


# --- Dialogs -----------------------------------------------------------------


class Dialog(ctk.CTkToplevel):
    """Modal OTEKH dialog: panel surface, Bai Jamjuree title, button row.

    dlg = Dialog(parent, fonts, "TITLE", width=440, height=200)
    dlg.set_body("Message text")
    dlg.add_button("APPLY", cmd, primary=True).pack(...) or use button_row.
    """

    def __init__(
        self,
        master,
        fonts: Fonts,
        title: str,
        width: int = 440,
        height: int = 200,
    ) -> None:
        super().__init__(master)
        self._fonts = fonts
        self.title(title)
        self.configure(fg_color=T.SURFACE_PANEL)
        self.transient(master)
        self.resizable(False, False)
        master.update_idletasks()
        x = master.winfo_rootx() + (master.winfo_width() - width) // 2
        y = master.winfo_rooty() + (master.winfo_height() - height) // 3
        self.geometry(f"{width}x{height}+{x}+{y}")

        ctk.CTkLabel(
            self,
            text=title,
            font=fonts.display_font(16),
            text_color=T.TEXT_PRIMARY,
        ).pack(anchor="w", padx=T.SPACE_4, pady=(T.SPACE_4, T.SPACE_1))

        self._body = ctk.CTkLabel(
            self,
            text="",
            font=fonts.ui_font(12),
            text_color=T.TEXT_SECONDARY,
            justify="left",
            wraplength=width - 2 * T.SPACE_4,
        )
        self._body.pack(
            anchor="w", padx=T.SPACE_4, pady=(0, T.SPACE_2)
        )

        # Pack buttons into this row with side="right".
        self.button_row = ctk.CTkFrame(self, fg_color="transparent")
        self.button_row.pack(
            fill="x", side="bottom", padx=T.SPACE_4, pady=T.SPACE_3
        )

        self.grab_set()

    def set_body(self, text: str) -> None:
        self._body.configure(text=text)

    def add_button(self, text: str, command, primary: bool = False):
        """Create an OTEKH-styled button inside the dialog's button row."""
        factory = primary_button if primary else secondary_button
        return factory(self.button_row, text, command, self._fonts)
