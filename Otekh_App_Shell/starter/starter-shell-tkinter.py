"""OTEKH starter shell — Tkinter/CustomTkinter reference layout.

Runnable twin of starter-shell.html: the same five regions (app bar, nav,
canvas, inspector, status bar) built with tkinter/otekh_shell.py and
tokens/otekh_tokens.py. Use it as the starting point for OTEKH Tkinter
apps (Raspberry Pi local apps, desktop tools) or as a visual reference.

Run from this directory:
    uv run --with customtkinter --with pillow python starter-shell-tkinter.py
or in a project venv with customtkinter + Pillow installed:
    python starter-shell-tkinter.py

PROVIDES: a runnable demo app (main()).
CONSUMES: tkinter/otekh_shell.py (components + font bootstrap),
          tokens/otekh_tokens.py (via otekh_shell), Assets/logos/
          OTEKH_wordmark.png (app-bar brand, if present).
"""

from __future__ import annotations

import sys
from pathlib import Path

import customtkinter as ctk

# Make tkinter/ importable when run from the Shell layout.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tkinter"))

import otekh_shell as shell  # noqa: E402
import otekh_tokens as T  # noqa: E402

WORDMARK = (
    Path(__file__).resolve().parent.parent
    / "Assets"
    / "logos"
    / "OTEKH_wordmark.png"
)


class StarterShell(ctk.CTk):
    """Five-region OTEKH layout: app bar / nav / canvas / inspector / status."""

    def __init__(self) -> None:
        shell.ensure_fonts()  # must precede Tk root creation
        super().__init__()
        self.title("OTEKH Starter Shell")
        self.geometry("1024x640")
        self.minsize(760, 480)
        ctk.set_appearance_mode("Light")
        self.configure(fg_color=T.SURFACE_CANVAS)

        fonts = shell.Fonts()

        # --- Top chrome: wordmark + product name + context + status ---
        wordmark_img = self._load_wordmark()
        bar = shell.AppBar(
            self,
            fonts,
            title="STARTER SHELL",
            context="Project / Example",
            wordmark=wordmark_img,
        )
        bar.pack(fill="x")
        ctk.CTkLabel(
            bar.right,
            text="● CONNECTED",
            font=fonts.ui_medium_font(12),
            text_color=T.STATUS_GOOD,
        ).pack(side="right")

        # --- Bottom chrome first so the canvas fills remaining space ---
        status = shell.StatusBar(self, fonts)
        status.pack(fill="x", side="bottom")
        status.set_left("● SYSTEM OPERATIONAL", T.STATUS_GOOD)
        status.set_right("v1.0.0")

        # --- Left navigation (recessed surface, gold selection mark) ---
        nav = shell.NavRail(
            self,
            fonts,
            items=["Overview", "Live data", "Inputs", "Process", "Output",
                   "Reports", "Settings"],
            on_select=lambda label: print(f"nav: {label}"),
        )
        nav.pack(fill="y", side="left")
        nav.select("Live data")

        # --- Right inspector ---
        inspector = shell.Panel(self, width=T.INSPECTOR, corner_radius=0)
        inspector.pack(fill="y", side="right")
        inspector.pack_propagate(False)
        ctk.CTkLabel(
            inspector,
            text="INSPECTOR",
            font=fonts.ui_medium_font(11),
            text_color=T.TEXT_SECONDARY,
        ).pack(anchor="w", padx=T.SPACE_3, pady=(T.SPACE_3, 0))
        ctk.CTkLabel(
            inspector,
            text="Properties, metadata, permissions,\nparameters, and history.",
            font=fonts.ui_font(12),
            text_color=T.TEXT_SECONDARY,
            justify="left",
        ).pack(anchor="w", padx=T.SPACE_3, pady=T.SPACE_2)

        # --- Main canvas ---
        canvas = ctk.CTkFrame(self, fg_color=T.SURFACE_CANVAS, corner_radius=0)
        canvas.pack(expand=True, fill="both")
        ctk.CTkLabel(
            canvas,
            text="LIVE DATA",
            font=fonts.display_font(20),
            text_color=T.BRAND_OLIVE,
        ).pack(anchor="w", padx=T.SPACE_4, pady=(T.SPACE_3, T.SPACE_2))

        panel = shell.Panel(canvas)
        panel.pack(expand=True, fill="both", padx=T.SPACE_4, pady=T.SPACE_2)
        ctk.CTkLabel(
            panel,
            text="PRIMARY WORK CANVAS",
            font=fonts.ui_medium_font(11),
            text_color=T.TEXT_SECONDARY,
        ).pack(anchor="w", padx=T.SPACE_3, pady=(T.SPACE_3, 0))
        well = shell.DataWell(panel)
        well.pack(expand=True, fill="both", padx=T.SPACE_3, pady=T.SPACE_3)
        ctk.CTkLabel(
            well,
            text="Place the active chart, media viewer, editor,\ntable, map, or project material here.",
            font=fonts.ui_font(13),
            text_color=T.TEXT_INVERSE_MUTED,
            justify="center",
        ).pack(expand=True)

        # Demo dialog button so the Dialog/button styles are visible.
        shell.primary_button(
            canvas,
            "OPEN DIALOG",
            lambda: self._demo_dialog(fonts),
            fonts,
        ).pack(anchor="e", padx=T.SPACE_4, pady=T.SPACE_2)

    def _load_wordmark(self) -> ctk.CTkImage | None:
        """Load the official wordmark for the app bar, if the asset exists."""
        if not WORDMARK.exists():
            return None
        try:
            from PIL import Image

            img = Image.open(WORDMARK)
            ratio = img.width / img.height
            return ctk.CTkImage(light_image=img, size=(int(30 * ratio), 30))
        except Exception:
            return None

    def _demo_dialog(self, fonts: shell.Fonts) -> None:
        dlg = shell.Dialog(self, fonts, "APPLY CHANGES", width=440, height=190)
        dlg.set_body(
            "You have unsaved changes.\nThis action cannot be undone."
        )
        dlg.add_button("APPLY", dlg.destroy, primary=True).pack(
            side="right", padx=(T.SPACE_2, 0)
        )
        dlg.add_button("CANCEL", dlg.destroy).pack(side="right")


def main() -> None:
    app = StarterShell()
    app.mainloop()


if __name__ == "__main__":
    main()
