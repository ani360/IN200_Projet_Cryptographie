"""
ui/panels/substitution_panel.py  –  Panneau Substitution monoalphabétique
"""

import customtkinter as ctk
from ui.base_panel import BasePanel
from logic.crypto import substitution_encrypt, substitution_decrypt, substitution_crack

# TODO: remplace ce placeholder par ton import réel, ex:
# from logic.crypto import rng_alph
def rng_alph() -> str:
    """Placeholder — retourne un alphabet aléatoire de 26 lettres.
    # TODO : remplacer par ta propre implémentation.
    """
    import random, string
    alpha = list(string.ascii_uppercase)
    random.shuffle(alpha)
    return "".join(alpha)


_HINT = "26 lettres : ex QWERTYUIOPASDFGHJKLZXCVBNM"


class SubstitutionPanel(BasePanel):
    METHOD_NAME = "Chiffrement par Substitution"

    def _build_action_blocks(self, row: int) -> int:
        C = self.C

        # ── CHIFFRER ──────────────────────────────────────────────────────
        enc = self._action_card(self._scroll, "🔒  CHIFFRER", C["accent"])
        enc.grid(row=row, column=0, sticky="ew", padx=32, pady=(0, 12))
        enc.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(enc, text="Alphabet de substitution (26 lettres) :",
                     font=ctk.CTkFont(size=11), text_color=C["text_mid"],
                     ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 4))

        enc_row = ctk.CTkFrame(enc, fg_color="transparent")
        enc_row.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        enc_row.grid_columnconfigure(0, weight=1)

        self._enc_alpha = ctk.CTkEntry(
            enc_row, placeholder_text=_HINT,
            font=ctk.CTkFont(family="Courier New", size=12),
            fg_color=C["entry_bg"], border_color=C["border"], border_width=1,
            corner_radius=6, text_color=C["text"], height=34,
        )
        self._enc_alpha.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        ctk.CTkButton(
            enc_row, text="🎲",
            font=ctk.CTkFont(size=14),
            width=36, height=34,
            corner_radius=6,
            fg_color=C["card"], hover_color=C["hover"],
            text_color=C["accent2"], border_width=1, border_color=C["border"],
            command=lambda: self._fill_rng(self._enc_alpha),
        ).grid(row=0, column=1)

        self._action_button(enc, "🔒  Chiffrer", C["accent"], self._do_encrypt, row=3)

        # ── DÉCHIFFRER ────────────────────────────────────────────────────
        dec = self._action_card(self._scroll, "🔓  DÉCHIFFRER", C["success"])
        dec.grid(row=row + 1, column=0, sticky="ew", padx=32, pady=(0, 12))
        dec.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(dec, text="Alphabet de substitution (26 lettres) :",
                     font=ctk.CTkFont(size=11), text_color=C["text_mid"],
                     ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 4))

        dec_row = ctk.CTkFrame(dec, fg_color="transparent")
        dec_row.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        dec_row.grid_columnconfigure(0, weight=1)

        self._dec_alpha = ctk.CTkEntry(
            dec_row, placeholder_text=_HINT,
            font=ctk.CTkFont(family="Courier New", size=12),
            fg_color=C["entry_bg"], border_color=C["border"], border_width=1,
            corner_radius=6, text_color=C["text"], height=34,
        )
        self._dec_alpha.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        ctk.CTkButton(
            dec_row, text="🎲",
            font=ctk.CTkFont(size=14),
            width=36, height=34,
            corner_radius=6,
            fg_color=C["card"], hover_color=C["hover"],
            text_color=C["accent2"], border_width=1, border_color=C["border"],
            command=lambda: self._fill_rng(self._dec_alpha),
        ).grid(row=0, column=1)

        self._action_button(dec, "🔓  Déchiffrer", C["success"], self._do_decrypt, row=3)

        # ── SLIDER ITÉRATIONS ─────────────────────────────────────────────
        iter_card = self._card(self._scroll, "🔁  NOMBRE D'ITÉRATIONS (pour le cracker)")
        iter_card.grid(row=row + 2, column=0, sticky="ew", padx=32, pady=(0, 12))
        iter_card.grid_columnconfigure(0, weight=1)

        self._iter_val = ctk.IntVar(value=100000)

        iter_row = ctk.CTkFrame(iter_card, fg_color="transparent")
        iter_row.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 14))
        iter_row.grid_columnconfigure(0, weight=1)

        self._iter_lbl = ctk.CTkLabel(
            iter_row,
            text="100 000",
            font=ctk.CTkFont(family="Courier New", size=12, weight="bold"),
            text_color=C["warn"],
            width=90,
            anchor="e",
        )
        self._iter_lbl.grid(row=0, column=1, padx=(10, 0))

        ctk.CTkSlider(
            iter_row,
            from_=10000, to=200000,
            number_of_steps=200,
            variable=self._iter_val,
            fg_color=C["border"],
            progress_color=C["warn"],
            button_color=C["warn"],
            button_hover_color=C["accent"],
            command=self._update_iter_label,
        ).grid(row=0, column=0, sticky="ew")

        # ── CRACKER ───────────────────────────────────────────────────────
        crack = self._action_card(self._scroll, "💥  CRACKER (Méthode de Monte-Carlo par chaînes de Markov.)", C["warn"])
        crack.grid(row=row + 3, column=0, sticky="ew", padx=32, pady=(0, 16))
        crack.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(crack,
                     text="Compare les fréquences de lettres à celles de la langue cible.",
                     font=ctk.CTkFont(size=11), text_color=C["text_mid"],
                     ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))
        self._action_button(crack, "💥  Calculer / Décrypter", C["warn"], self._do_crack, row=2)

        return row + 4

    def _fill_rng(self, entry: ctk.CTkEntry):
        """Génère un alphabet aléatoire via rng_alph() et l'injecte dans le champ."""
        alpha = rng_alph()
        entry.delete(0, "end")
        entry.insert(0, alpha)

    def _validate_alpha(self, alpha: str) -> bool:
        alpha = alpha.upper().replace(" ", "")
        return len(alpha) == 26 and len(set(alpha)) == 26

    def _do_encrypt(self):
        alpha = self._enc_alpha.get().strip().upper()
        if not self._validate_alpha(alpha):
            self._set_result("⚠ L'alphabet doit contenir exactement 26 lettres distinctes.")
            return
        self._set_result(substitution_encrypt(self._get_input(), alpha,
                                              self._keep_acc.get(), self._keep_case.get(),
                                              self._language.get()))

    def _do_decrypt(self):
        alpha = self._dec_alpha.get().strip().upper()
        if not self._validate_alpha(alpha):
            self._set_result("⚠ L'alphabet doit contenir exactement 26 lettres distinctes.")
            return
        self._set_result(substitution_decrypt(self._get_input(), alpha,
                                              self._keep_acc.get(), self._keep_case.get(),
                                              self._language.get()))

    def _do_crack(self):
        self._set_result(substitution_crack(self._get_input(),
                                            self._keep_acc.get(), self._keep_case.get(),
                                            self._language.get(),
                                            self._iter_val.get()))
    def _update_iter_label(self, value):
        n = int(value)
        self._iter_lbl.configure(text=f"{n:,}".replace(",", " "))
