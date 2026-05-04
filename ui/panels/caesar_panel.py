"""
ui/panels/caesar_panel.py  –  Panneau César
"""

import customtkinter as ctk
from ui.base_panel import BasePanel
from logic.crypto import caesar_encrypt, caesar_decrypt, caesar_crack


class CaesarPanel(BasePanel):
    METHOD_NAME = "Chiffre de César"

    def _build_action_blocks(self, row: int) -> int:
        C = self.C

        # ── CHIFFRER ──────────────────────────────────────────────────────
        enc = self._action_card(self._scroll, "🔒  CHIFFRER", C["accent"])
        enc.grid(row=row, column=0, sticky="ew", padx=32, pady=(0, 12))
        enc.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(enc, text="Décalage (entier) :",
                     font=ctk.CTkFont(size=11), text_color=C["text_mid"],
                     ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 4))
        self._enc_shift = ctk.CTkEntry(
            enc, placeholder_text="ex: 13",
            font=ctk.CTkFont(family="Courier New", size=12),
            fg_color=C["entry_bg"], border_color=C["border"], border_width=1,
            corner_radius=6, text_color=C["text"], height=34, width=120,
        )
        self._enc_shift.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 12))
        self._action_button(enc, "🔒  Chiffrer", C["accent"], self._do_encrypt, row=3)

        # ── DÉCHIFFRER ────────────────────────────────────────────────────
        dec = self._action_card(self._scroll, "🔓  DÉCHIFFRER", C["success"])
        dec.grid(row=row + 1, column=0, sticky="ew", padx=32, pady=(0, 12))
        dec.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(dec, text="Décalage (entier) :",
                     font=ctk.CTkFont(size=11), text_color=C["text_mid"],
                     ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 4))
        self._dec_shift = ctk.CTkEntry(
            dec, placeholder_text="ex: 13",
            font=ctk.CTkFont(family="Courier New", size=12),
            fg_color=C["entry_bg"], border_color=C["border"], border_width=1,
            corner_radius=6, text_color=C["text"], height=34, width=120,
        )
        self._dec_shift.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 12))
        self._action_button(dec, "🔓  Déchiffrer", C["success"], self._do_decrypt, row=3)

        # ── CRACKER ───────────────────────────────────────────────────────
        crack = self._action_card(self._scroll, "💥  CRACKER (analyse de fréquence)", C["warn"])
        crack.grid(row=row + 2, column=0, sticky="ew", padx=32, pady=(0, 16))
        crack.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(crack, text="Fait l'analyse de fréquence du code de césar.",
                     font=ctk.CTkFont(size=11), text_color=C["text_mid"],
                     ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))
        self._action_button(crack, "💥  Calculer / Décrypter", C["warn"], self._do_crack, row=2)

        return row + 3

    # ── Handlers ──────────────────────────────────────────────────────────

    def _do_encrypt(self):
        try:
            shift = int(self._enc_shift.get())
        except ValueError:
            self._set_result("⚠ Le décalage doit être un entier.")
            return
        result = caesar_encrypt(
            self._get_input(), shift,
            self._keep_acc.get(), self._keep_case.get(), self._language.get()
        )
        self._set_result(result)

    def _do_decrypt(self):
        try:
            shift = int(self._dec_shift.get())
        except ValueError:
            self._set_result("⚠ Le décalage doit être un entier.")
            return
        result = caesar_decrypt(
            self._get_input(), shift,
            self._keep_acc.get(), self._keep_case.get(), self._language.get()
        )
        self._set_result(result)

    def _do_crack(self):
        result = caesar_crack(
            self._get_input(),
            self._keep_acc.get(), self._keep_case.get(), self._language.get()
        )
        self._set_result(result)
