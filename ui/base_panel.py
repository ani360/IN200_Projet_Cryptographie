"""
ui/base_panel.py  –  Panneau de base partagé par toutes les méthodes.
Fournit :
  • Zone d'entrée du message + import de fichier
  • Paramètres globaux (langue, accents, casse)
  • Section résultat avec bouton Copier
  • Méthodes utilitaires pour les sous-classes
"""

from __future__ import annotations
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox


class BasePanel(ctk.CTkFrame):
    # Sous-classes doivent définir METHOD_NAME
    METHOD_NAME: str = "Méthode"

    def __init__(self, master, colors: dict):
        super().__init__(master, fg_color=colors["bg"], corner_radius=0)
        self.C = colors
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Variables globales
        self._language   = ctk.StringVar(value="french")
        self._keep_acc   = ctk.BooleanVar(value=True)
        self._keep_case  = ctk.BooleanVar(value=True)

        self._build_ui()

    # ─────────────────────────────────────────────────────────────────────
    #  Construction générale
    # ─────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Scrollable container
        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color=self.C["bg"], corner_radius=0,
            scrollbar_button_color=self.C["border"],
            scrollbar_button_hover_color=self.C["accent"],
        )
        self._scroll.grid(row=0, column=0, sticky="nsew")
        self._scroll.grid_columnconfigure(0, weight=1)

        row = 0

        # ── En-tête ───────────────────────────────────────────────────────
        row = self._build_header(row)

        # ── Entrée message ────────────────────────────────────────────────
        row = self._build_input_section(row)

        # ── Paramètres globaux ────────────────────────────────────────────
        row = self._build_global_params(row)

        # ── Blocs d'actions (injectés par sous-classes) ────────────────────
        row = self._build_action_blocks(row)

        # ── Résultat ──────────────────────────────────────────────────────
        self._build_result_section(row)

    # ── En-tête ───────────────────────────────────────────────────────────

    def _build_header(self, row: int) -> int:
        hdr = ctk.CTkFrame(self._scroll, fg_color="transparent")
        hdr.grid(row=row, column=0, sticky="ew", padx=32, pady=(28, 8))
        hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            hdr, text=self.METHOD_NAME,
            font=ctk.CTkFont(family="Courier New", size=26, weight="bold"),
            text_color=self.C["accent"],
        ).grid(row=0, column=0, sticky="w")

        # Ligne décorative
        line = ctk.CTkFrame(self._scroll, height=2, fg_color=self.C["border"])
        line.grid(row=row + 1, column=0, sticky="ew", padx=32, pady=(4, 20))
        return row + 2

    # ── Entrée ────────────────────────────────────────────────────────────

    def _build_input_section(self, row: int) -> int:
        card = self._card(self._scroll, "📝  MESSAGE D'ENTRÉE")
        card.grid(row=row, column=0, sticky="ew", padx=32, pady=(0, 16))
        card.grid_columnconfigure(0, weight=1)

        self._input_text = ctk.CTkTextbox(
            card,
            height=110,
            font=ctk.CTkFont(family="Courier New", size=12),
            fg_color=self.C["entry_bg"],
            border_color=self.C["border"],
            border_width=1,
            corner_radius=6,
            text_color=self.C["text"],
            wrap="word",
        )
        self._input_text.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 10))

        import_btn = ctk.CTkButton(
            card, text="📂  Importer un fichier .txt",
            font=ctk.CTkFont(size=11),
            height=30,
            fg_color="transparent",
            hover_color=self.C["hover"],
            text_color=self.C["text_dim"],
            border_width=1,
            border_color=self.C["border"],
            corner_radius=6,
            command=self._import_file,
        )
        import_btn.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 14))

        return row + 1

    # ── Paramètres globaux ────────────────────────────────────────────────

    def _build_global_params(self, row: int) -> int:
        card = self._card(self._scroll, "⚙  PARAMÈTRES GÉNÉRAUX")
        card.grid(row=row, column=0, sticky="ew", padx=32, pady=(0, 16))
        card.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(
            card, text="Langue :",
            font=ctk.CTkFont(size=12),
            text_color=self.C["text_mid"],
        ).grid(row=1, column=0, padx=16, pady=(0, 14), sticky="w")

        ctk.CTkOptionMenu(
            card,
            values=["french", "english", "spanish", "german", "italian", "portuguese", "russian"],
            variable=self._language,
            font=ctk.CTkFont(size=12),
            fg_color=self.C["card"],
            button_color=self.C["border"],
            button_hover_color=self.C["hover"],
            dropdown_fg_color=self.C["card"],
            text_color=self.C["text"],
            width=150,
            height=30,
            corner_radius=6,
        ).grid(row=1, column=1, padx=4, pady=(0, 14), sticky="w")

        ctk.CTkCheckBox(
            card, text="Conserver accents",
            variable=self._keep_acc,
            font=ctk.CTkFont(size=12),
            text_color=self.C["text_mid"],
            fg_color=self.C["accent"],
            hover_color=self.C["accent2"],
            border_color=self.C["border"],
            checkmark_color="#ffffff",
        ).grid(row=1, column=2, padx=16, pady=(0, 14), sticky="w")

        ctk.CTkCheckBox(
            card, text="Conserver majuscules",
            variable=self._keep_case,
            font=ctk.CTkFont(size=12),
            text_color=self.C["text_mid"],
            fg_color=self.C["accent"],
            hover_color=self.C["accent2"],
            border_color=self.C["border"],
            checkmark_color="#ffffff",
        ).grid(row=1, column=3, padx=16, pady=(0, 14), sticky="w")

        return row + 1

    # ── Blocs d'actions — OVERRIDE dans les sous-classes ──────────────────

    def _build_action_blocks(self, row: int) -> int:
        """Sous-classes surchargent cette méthode pour injecter leurs blocs."""
        return row

    # ── Résultat ──────────────────────────────────────────────────────────

    def _build_result_section(self, row: int):
        card = self._card(self._scroll, "📤  RÉSULTAT")
        card.grid(row=row, column=0, sticky="ew", padx=32, pady=(0, 32))
        card.grid_columnconfigure(0, weight=1)

        self._result_text = ctk.CTkTextbox(
            card,
            height=130,
            font=ctk.CTkFont(family="Courier New", size=12),
            fg_color=self.C["entry_bg"],
            border_color=self.C["accent"],
            border_width=1,
            corner_radius=6,
            text_color=self.C["success"],
            wrap="word",
            state="disabled",
        )
        self._result_text.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 10))

        copy_btn = ctk.CTkButton(
            card,
            text="📋  Copier dans le presse-papier",
            font=ctk.CTkFont(size=11, weight="bold"),
            height=32,
            corner_radius=6,
            fg_color=self.C["card"],
            hover_color=self.C["hover"],
            text_color=self.C["accent"],
            border_width=1,
            border_color=self.C["accent"],
            command=self._copy_result,
        )
        copy_btn.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 14))

    # ─────────────────────────────────────────────────────────────────────
    #  Helpers UI réutilisables
    # ─────────────────────────────────────────────────────────────────────

    def _card(self, parent, title: str) -> ctk.CTkFrame:
        """Crée un bloc carte avec un titre de section."""
        frame = ctk.CTkFrame(
            parent,
            fg_color=self.C["panel"],
            corner_radius=10,
            border_width=1,
            border_color=self.C["border"],
        )
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame, text=title,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.C["text_dim"],
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 8),
               columnspan=10)
        return frame

    def _action_card(self, parent, title: str, color: str) -> ctk.CTkFrame:
        """Crée un bloc action coloré (Chiffrer / Déchiffrer / Cracker)."""
        frame = ctk.CTkFrame(
            parent,
            fg_color=self.C["panel"],
            corner_radius=10,
            border_width=1,
            border_color=color,
        )
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame, text=title,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=color,
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 6),
               columnspan=10)
        return frame

    def _action_button(self, parent, text: str, color: str,
                       command, row=1, col=0, colspan=1):
        btn = ctk.CTkButton(
            parent,
            text=text,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36,
            corner_radius=8,
            fg_color=color,
            hover_color=color,
            text_color="#ffffff",
            command=command,
        )
        btn.grid(row=row, column=col, columnspan=colspan,
                 sticky="ew", padx=16, pady=(0, 14))
        return btn

    def _key_entry(self, parent, label: str, row=1,
                   col=0, placeholder="") -> ctk.CTkEntry:
        ctk.CTkLabel(
            parent, text=label,
            font=ctk.CTkFont(size=11),
            text_color=self.C["text_mid"],
        ).grid(row=row, column=col, sticky="w", padx=16, pady=(0, 4))

        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            font=ctk.CTkFont(family="Courier New", size=12),
            fg_color=self.C["entry_bg"],
            border_color=self.C["border"],
            border_width=1,
            corner_radius=6,
            text_color=self.C["text"],
            height=34,
        )
        entry.grid(row=row + 1, column=col, sticky="ew",
                   padx=16, pady=(0, 12))
        return entry

    # ─────────────────────────────────────────────────────────────────────
    #  Actions communes
    # ─────────────────────────────────────────────────────────────────────

    def _get_input(self) -> str:
        return self._input_text.get("1.0", "end").rstrip("\n")

    def _set_result(self, text: str):
        self._result_text.configure(state="normal")
        self._result_text.delete("1.0", "end")
        self._result_text.insert("1.0", text)
        self._result_text.configure(state="disabled")

    def _import_file(self):
        path = filedialog.askopenfilename(
            title="Importer un fichier texte",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
        )
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self._input_text.delete("1.0", "end")
                self._input_text.insert("1.0", content)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lire le fichier :\n{e}")

    def _copy_result(self):
        text = self._result_text.get("1.0", "end").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
