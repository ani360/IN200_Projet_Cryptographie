"""
ui/panels/vigenere_panel.py  –  Panneau Vigenère
"""

import customtkinter as ctk
from ui.base_panel import BasePanel
from logic.crypto import vigenere_encrypt, vigenere_decrypt, vigenere_crack


class VigenerePanel(BasePanel):
    METHOD_NAME = "Chiffre de Vigenère"

    def _build_action_blocks(self, row: int) -> int:
        C = self.C

        # ── CHIFFRER ──────────────────────────────────────────────────────
        enc = self._action_card(self._scroll, "🔒  CHIFFRER", C["accent"])
        enc.grid(row=row, column=0, sticky="ew", padx=32, pady=(0, 12))
        enc.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(enc, text="Mot-clé :", font=ctk.CTkFont(size=11),
                     text_color=C["text_mid"]).grid(row=1, column=0, sticky="w",
                                                    padx=16, pady=(0, 4))
        self._enc_key = ctk.CTkEntry(
            enc, placeholder_text="ex: SECRET",
            font=ctk.CTkFont(family="Courier New", size=12),
            fg_color=C["entry_bg"], border_color=C["border"], border_width=1,
            corner_radius=6, text_color=C["text"], height=34,
        )
        self._enc_key.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        self._action_button(enc, "🔒  Chiffrer", C["accent"], self._do_encrypt, row=3)

        # ── DÉCHIFFRER ────────────────────────────────────────────────────
        dec = self._action_card(self._scroll, "🔓  DÉCHIFFRER", C["success"])
        dec.grid(row=row + 1, column=0, sticky="ew", padx=32, pady=(0, 12))
        dec.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(dec, text="Mot-clé :", font=ctk.CTkFont(size=11),
                     text_color=C["text_mid"]).grid(row=1, column=0, sticky="w",
                                                    padx=16, pady=(0, 4))
        self._dec_key = ctk.CTkEntry(
            dec, placeholder_text="ex: SECRET",
            font=ctk.CTkFont(family="Courier New", size=12),
            fg_color=C["entry_bg"], border_color=C["border"], border_width=1,
            corner_radius=6, text_color=C["text"], height=34,
        )
        self._dec_key.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        self._action_button(dec, "🔓  Déchiffrer", C["success"], self._do_decrypt, row=3)

        # ── CRACKER ───────────────────────────────────────────────────────
        crack = self._action_card(self._scroll, "💥  CRACKER (Kasiski)", C["warn"])
        crack.grid(row=row + 2, column=0, sticky="ew", padx=32, pady=(0, 16))
        crack.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(crack,
                     text="Analyse l'indice de coïncidence pour retrouver la clé.",
                     font=ctk.CTkFont(size=11), text_color=C["text_mid"],
                     ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))
        self._action_button(crack, "💥  Calculer / Décrypter", C["warn"], self._do_crack, row=2)

        return row + 3

    def _do_encrypt(self):
        key = self._enc_key.get().strip()
        if not key:
            self._set_result("⚠ Veuillez entrer un mot-clé.")
            return
        self._set_result(vigenere_encrypt(self._get_input(), key,
                                          self._keep_acc.get(), self._keep_case.get(),
                                          self._language.get()))

    def _do_decrypt(self):
        key = self._dec_key.get().strip()
        if not key:
            self._set_result("⚠ Veuillez entrer un mot-clé.")
            return
        self._set_result(vigenere_decrypt(self._get_input(), key,
                                          self._keep_acc.get(), self._keep_case.get(),
                                          self._language.get()))

    def _do_crack(self):
        self._set_result(vigenere_crack(self._get_input(),
                                        self._keep_acc.get(), self._keep_case.get(),
                                        self._language.get()))
