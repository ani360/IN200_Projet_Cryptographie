"""
ui/app.py  –  Fenêtre principale de CryptoTool
"""

import customtkinter as ctk
from ui.sidebar import Sidebar
from ui.panels.caesar_panel import CaesarPanel
from ui.panels.vigenere_panel import VigenerePanel
from ui.panels.substitution_panel import SubstitutionPanel
from ui.panels.scytale_panel import ScytalePanel
from ui.panels.enigma_panel import EnigmaPanel

# Palette de couleurs
C = {
    "bg":        "#0d0f14",
    "sidebar":   "#12151c",
    "panel":     "#161a24",
    "card":      "#1c2133",
    "border":    "#252d42",
    "accent":    "#4f8ef7",
    "accent2":   "#7c3aed",
    "success":   "#10b981",
    "danger":    "#ef4444",
    "warn":      "#f59e0b",
    "text":      "#e2e8f0",
    "text_dim":  "#64748b",
    "text_mid":  "#94a3b8",
    "entry_bg":  "#0f1319",
    "hover":     "#1e2a40",
}

METHODS = ["César", "Vigenère", "Substitution", "Scytale", "Enigma"]

PANEL_MAP = {
    "César":        CaesarPanel,
    "Vigenère":     VigenerePanel,
    "Substitution": SubstitutionPanel,
    "Scytale":      ScytalePanel,
    "Enigma":       EnigmaPanel,
}


class CryptoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CryptoTool — Boîte à outils de cryptographie")
        self.geometry("1280x820")
        self.minsize(1024, 700)
        self.configure(fg_color=C["bg"])

        self._current_method = ctk.StringVar(value="César")
        self._current_panel = None

        self._build_layout()
        self._switch_method("César")

    # ── Layout principal ──────────────────────────────────────────────────

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Barre latérale
        self.sidebar = Sidebar(
            self,
            methods=METHODS,
            on_select=self._switch_method,
            colors=C,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Conteneur du panneau central
        self.panel_host = ctk.CTkFrame(self, fg_color=C["bg"], corner_radius=0)
        self.panel_host.grid(row=0, column=1, sticky="nsew")
        self.panel_host.grid_columnconfigure(0, weight=1)
        self.panel_host.grid_rowconfigure(0, weight=1)

    # ── Changement de méthode ─────────────────────────────────────────────

    def _switch_method(self, method: str):
        self._current_method.set(method)
        self.sidebar.highlight(method)

        if self._current_panel is not None:
            self._current_panel.destroy()

        PanelClass = PANEL_MAP[method]
        self._current_panel = PanelClass(self.panel_host, colors=C)
        self._current_panel.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
