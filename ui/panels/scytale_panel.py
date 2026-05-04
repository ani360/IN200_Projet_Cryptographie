"""
ui/panels/scytale_panel.py  –  Panneau Scytale
"""

import customtkinter as ctk
from ui.base_panel import BasePanel
from logic.crypto import scytale_encrypt, scytale_decrypt, scytale_crack


class ScytalePanel(BasePanel):
    METHOD_NAME = "Scytale (Transposition)"

    def _build_action_blocks(self, row: int) -> int:
        C = self.C

        # ── CHIFFRER ──────────────────────────────────────────────────────
        enc = self._action_card(self._scroll, "🔒  CHIFFRER", C["accent"])
        enc.grid(row=row, column=0, sticky="ew", padx=32, pady=(0, 12))
        enc.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(enc, text="Diamètre du bâton (nombre de colonnes) :",
                     font=ctk.CTkFont(size=11), text_color=C["text_mid"],
                     ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 4))

        enc_inner = ctk.CTkFrame(enc, fg_color="transparent")
        enc_inner.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 12))

        self._enc_diam = ctk.CTkEntry(
            enc_inner, placeholder_text="ex: 4",
            font=ctk.CTkFont(family="Courier New", size=12),
            fg_color=C["entry_bg"], border_color=C["border"], border_width=1,
            corner_radius=6, text_color=C["text"], height=34, width=100,
        )
        self._enc_diam.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(enc_inner, text="(entier ≥ 2)",
                     font=ctk.CTkFont(size=10), text_color=C["text_dim"],
                     ).pack(side="left")

        self._action_button(enc, "🔒  Chiffrer", C["accent"], self._do_encrypt, row=3)

        # ── DÉCHIFFRER ────────────────────────────────────────────────────
        dec = self._action_card(self._scroll, "🔓  DÉCHIFFRER", C["success"])
        dec.grid(row=row + 1, column=0, sticky="ew", padx=32, pady=(0, 12))
        dec.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(dec, text="Diamètre du bâton :",
                     font=ctk.CTkFont(size=11), text_color=C["text_mid"],
                     ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 4))
        self._dec_diam = ctk.CTkEntry(
            dec, placeholder_text="ex: 4",
            font=ctk.CTkFont(family="Courier New", size=12),
            fg_color=C["entry_bg"], border_color=C["border"], border_width=1,
            corner_radius=6, text_color=C["text"], height=34, width=100,
        )
        self._dec_diam.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 12))
        self._action_button(dec, "🔓  Déchiffrer", C["success"], self._do_decrypt, row=3)

        # ── CRACKER ───────────────────────────────────────────────────────
        crack = self._action_card(self._scroll, "💥  CRACKER (force brute)", C["warn"])
        crack.grid(row=row + 2, column=0, sticky="ew", padx=32, pady=(0, 16))
        crack.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(crack,
                     text="Teste tous les diamètres possibles de 2 à len(texte).",
                     font=ctk.CTkFont(size=11), text_color=C["text_mid"],
                     ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))
        self._action_button(crack, "💥  Calculer / Décrypter", C["warn"], self._do_crack, row=2)

        return row + 3

    def _parse_diam(self, entry) -> int | None:
        try:
            v = int(entry.get())
            if v < 2:
                raise ValueError
            return v
        except ValueError:
            return None

    def _do_encrypt(self):
        d = self._parse_diam(self._enc_diam)
        if d is None:
            self._set_result("⚠ Le diamètre doit être un entier ≥ 2.")
            return
        self._set_result(scytale_encrypt(self._get_input(), d,
                                         self._keep_acc.get(), self._keep_case.get(),
                                         self._language.get()))

    def _do_decrypt(self):
        d = self._parse_diam(self._dec_diam)
        if d is None:
            self._set_result("⚠ Le diamètre doit être un entier ≥ 2.")
            return
        self._set_result(scytale_decrypt(self._get_input(), d,
                                         self._keep_acc.get(), self._keep_case.get(),
                                         self._language.get()))

    def _do_crack(self):
        self._set_result(scytale_crack(self._get_input(),
                                       self._keep_acc.get(), self._keep_case.get(),
                                       self._language.get()))
