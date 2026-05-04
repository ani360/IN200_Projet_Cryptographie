"""
ui/sidebar.py  –  Menu latéral de navigation
"""

import customtkinter as ctk


ICONS = {
    "César":        "Ↄ",
    "Vigenère":     "V",
    "Substitution": "⇄",
    "Scytale":      "⌀",
    "Enigma":       "⚙",
}


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, methods: list[str], on_select, colors: dict):
        super().__init__(master, fg_color=colors["sidebar"],
                         corner_radius=0, width=220)
        self.grid_propagate(False)
        self.colors = colors
        self.on_select = on_select
        self._buttons: dict[str, ctk.CTkButton] = {}

        self._build(methods)

    def _build(self, methods):
        # ── Logo / titre ──────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(28, 24))

        logo_lbl = ctk.CTkLabel(
            header,
            text="🔐",
            font=ctk.CTkFont(size=30),
            text_color=self.colors["accent"],
        )
        logo_lbl.pack(anchor="w")

        title_lbl = ctk.CTkLabel(
            header,
            text="CryptoTool",
            font=ctk.CTkFont(family="Courier New", size=18, weight="bold"),
            text_color=self.colors["text"],
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = ctk.CTkLabel(
            header,
            text="Boîte à outils",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_dim"],
        )
        subtitle_lbl.pack(anchor="w")

        # ── Séparateur ────────────────────────────────────────────────────
        sep = ctk.CTkFrame(self, height=1, fg_color=self.colors["border"])
        sep.pack(fill="x", padx=16, pady=(0, 16))

        # ── Label section ─────────────────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="MÉTHODES",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=self.colors["text_dim"],
        ).pack(anchor="w", padx=20, pady=(0, 8))

        # ── Boutons de méthode ────────────────────────────────────────────
        for method in methods:
            icon = ICONS.get(method, "•")
            btn = ctk.CTkButton(
                self,
                text=f"  {icon}   {method}",
                font=ctk.CTkFont(family="Courier New", size=13),
                anchor="w",
                height=44,
                corner_radius=8,
                fg_color="transparent",
                hover_color=self.colors["hover"],
                text_color=self.colors["text_mid"],
                border_width=0,
                command=lambda m=method: self.on_select(m),
            )
            btn.pack(fill="x", padx=10, pady=2)
            self._buttons[method] = btn

        # ── Bas de sidebar ────────────────────────────────────────────────
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(side="bottom", fill="x", padx=16, pady=20)

        ctk.CTkFrame(self, height=1, fg_color=self.colors["border"]).pack(
            side="bottom", fill="x", padx=16, pady=(0, 8)
        )

        ctk.CTkLabel(
            footer,
            text="v1.0  –  Architecture MVC",
            font=ctk.CTkFont(size=9),
            text_color=self.colors["text_dim"],
        ).pack(anchor="w")

    def highlight(self, method: str):
        for name, btn in self._buttons.items():
            if name == method:
                btn.configure(
                    fg_color=self.colors["card"],
                    text_color=self.colors["accent"],
                    border_width=1,
                    border_color=self.colors["accent"],
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=self.colors["text_mid"],
                    border_width=0,
                )
