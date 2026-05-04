"""
ui/panels/enigma_panel.py  –  Panneau Enigma
"""

from __future__ import annotations
import json
import customtkinter as ctk
from tkinter import filedialog, messagebox
from ui.base_panel import BasePanel
from logic.crypto import enigma_encrypt, enigma_decrypt, enigma_crack, enigma_generate_config


class EnigmaPanel(BasePanel):
    METHOD_NAME = "Machine Enigma"

    def __init__(self, master, colors: dict):
        self._enigma_config: dict | None = None
        super().__init__(master, colors)

    def _build_action_blocks(self, row: int) -> int:
        C = self.C

        # ── CONFIGURATION ─────────────────────────────────────────────────
        cfg = self._card(self._scroll, "🔧  CONFIGURATION ENIGMA")
        cfg.grid(row=row, column=0, sticky="ew", padx=32, pady=(0, 12))
        cfg.grid_columnconfigure((0, 1), weight=1)

        # Statut config
        self._cfg_label = ctk.CTkLabel(
            cfg, text="Aucune configuration chargée",
            font=ctk.CTkFont(family="Courier New", size=11),
            text_color=C["warn"],
        )
        self._cfg_label.grid(row=1, column=0, columnspan=2, sticky="w",
                             padx=16, pady=(0, 12))

        # Bouton charger JSON
        load_btn = ctk.CTkButton(
            cfg, text="📂  Charger config JSON",
            font=ctk.CTkFont(size=11, weight="bold"),
            height=34, corner_radius=7,
            fg_color=C["card"], hover_color=C["hover"],
            text_color=C["text"], border_width=1, border_color=C["border"],
            command=self._load_json,
        )
        load_btn.grid(row=2, column=0, sticky="ew", padx=(16, 8), pady=(0, 12))

        # Bouton générer aléatoire
        rnd_btn = ctk.CTkButton(
            cfg, text="🎲  Générer aléatoirement",
            font=ctk.CTkFont(size=11, weight="bold"),
            height=34, corner_radius=7,
            fg_color=C["accent2"], hover_color=C["accent2"],
            text_color="#ffffff",
            command=self._generate_random,
        )
        rnd_btn.grid(row=2, column=1, sticky="ew", padx=(8, 16), pady=(0, 12))

        # Séparateur paramètres de génération
        sep = ctk.CTkFrame(cfg, height=1, fg_color=C["border"])
        sep.grid(row=3, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        ctk.CTkLabel(cfg, text="Paramètres de génération aléatoire :",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=C["text_dim"],
                     ).grid(row=4, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 8))

        # Rotors slider
        rotor_row = ctk.CTkFrame(cfg, fg_color="transparent")
        rotor_row.grid(row=5, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 6))
        rotor_row.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(rotor_row, text="Rotors :",
                     font=ctk.CTkFont(size=11), text_color=C["text_mid"],
                     width=90, anchor="w").grid(row=0, column=0, sticky="w")

        self._rotor_val = ctk.IntVar(value=3)
        self._rotor_lbl = ctk.CTkLabel(rotor_row, text="3",
                                       font=ctk.CTkFont(family="Courier New", size=11, weight="bold"),
                                       text_color=C["accent"], width=30)
        self._rotor_lbl.grid(row=0, column=2, padx=(8, 0))

        rotor_slider = ctk.CTkSlider(
            rotor_row, from_=1, to=10, number_of_steps=9,
            variable=self._rotor_val,
            fg_color=C["border"], progress_color=C["accent"],
            button_color=C["accent"], button_hover_color=C["accent2"],
            command=lambda v: self._rotor_lbl.configure(text=str(int(v))),
        )
        rotor_slider.grid(row=0, column=1, sticky="ew", padx=8)

        # Plugboard slider
        plug_row = ctk.CTkFrame(cfg, fg_color="transparent")
        plug_row.grid(row=6, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 14))
        plug_row.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(plug_row, text="Connexions :",
                     font=ctk.CTkFont(size=11), text_color=C["text_mid"],
                     width=90, anchor="w").grid(row=0, column=0, sticky="w")

        self._plug_val = ctk.IntVar(value=10)
        self._plug_lbl = ctk.CTkLabel(plug_row, text="10",
                                      font=ctk.CTkFont(family="Courier New", size=11, weight="bold"),
                                      text_color=C["accent2"], width=30)
        self._plug_lbl.grid(row=0, column=2, padx=(8, 0))

        plug_slider = ctk.CTkSlider(
            plug_row, from_=0, to=13, number_of_steps=13,
            variable=self._plug_val,
            fg_color=C["border"], progress_color=C["accent2"],
            button_color=C["accent2"], button_hover_color=C["accent"],
            command=lambda v: self._plug_lbl.configure(text=str(int(v))),
        )
        plug_slider.grid(row=0, column=1, sticky="ew", padx=8)

        # Bouton exporter la config
        exp_btn = ctk.CTkButton(
            cfg, text="💾  Exporter config JSON",
            font=ctk.CTkFont(size=10),
            height=28, corner_radius=6,
            fg_color="transparent", hover_color=C["hover"],
            text_color=C["text_dim"], border_width=1, border_color=C["border"],
            command=self._export_json,
        )
        exp_btn.grid(row=7, column=0, columnspan=2, sticky="w",
                     padx=16, pady=(0, 14))

        # ── CHIFFRER / DÉCHIFFRER ─────────────────────────────────────────
        enc = self._action_card(self._scroll, "🔒  CHIFFRER", C["accent"])
        enc.grid(row=row + 1, column=0, sticky="ew", padx=32, pady=(0, 12))
        enc.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(enc,
                     text="Utilise la configuration chargée ci-dessus.",
                     font=ctk.CTkFont(size=11), text_color=C["text_mid"],
                     ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))
        self._action_button(enc, "🔒  Chiffrer", C["accent"], self._do_encrypt, row=2)

        dec = self._action_card(self._scroll, "🔓  DÉCHIFFRER", C["success"])
        dec.grid(row=row + 2, column=0, sticky="ew", padx=32, pady=(0, 12))
        dec.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(dec,
                     text="Enigma est auto-réciproque : utilise la même configuration.",
                     font=ctk.CTkFont(size=11), text_color=C["text_mid"],
                     ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))
        self._action_button(dec, "🔓  Déchiffrer", C["success"], self._do_decrypt, row=2)

        # ── CRACKER ───────────────────────────────────────────────────────
        crack = self._action_card(self._scroll, "💥  CRACKER (brutforce/seed)", C["warn"])
        crack.grid(row=row + 3, column=0, sticky="ew", padx=32, pady=(0, 16))
        crack.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(crack,
                     text="Bruteforce sur la seed de création d'une config, nécéssite de connaître la date de création la configuration.",
                     font=ctk.CTkFont(size=11), text_color=C["text_mid"],
                     ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))
        self._action_button(crack, "💥  Calculer / Décrypter", C["warn"], self._do_crack, row=2)

        return row + 4

    # ── Handlers ──────────────────────────────────────────────────────────

    def _load_json(self):
        path = filedialog.askopenfilename(
            title="Charger une configuration Enigma",
            filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                self._enigma_config = json.load(f)
            self._cfg_label.configure(
                text=f"✓ Config chargée : {path.split('/')[-1]}  "
                     f"({len(self._enigma_config.get('rotors', []))} rotors)",
                text_color=self.C["success"],
            )
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier JSON :\n{e}")

    def _generate_random(self):
        n_rotors = int(self._rotor_val.get())
        n_plug   = int(self._plug_val.get())
        self._enigma_config = enigma_generate_config(n_rotors, n_plug, self._language.get())
        self._cfg_label.configure(
            text=f"✓ Config générée : {n_rotors} rotors, {n_plug} connexions (plugboard)",
            text_color=self.C["success"],
        )

    def _export_json(self):
        if self._enigma_config is None:
            messagebox.showwarning("Aucune config", "Générez ou chargez d'abord une configuration.")
            return
        path = filedialog.asksaveasfilename(
            title="Exporter la configuration Enigma",
            defaultextension=".json",
            filetypes=[("Fichiers JSON", "*.json")],
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self._enigma_config, f, indent=2, ensure_ascii=False)

    def _check_config(self) -> bool:
        if self._enigma_config is None:
            self._set_result("⚠ Veuillez d'abord charger ou générer une configuration Enigma.")
            return False
        return True

    def _do_encrypt(self):
        if not self._check_config():
            return
        self._set_result(enigma_encrypt(self._get_input(), self._enigma_config,
                                        self._keep_acc.get(), self._keep_case.get(),
                                        self._language.get()))

    def _do_decrypt(self):
        if not self._check_config():
            return
        self._set_result(enigma_decrypt(self._get_input(), self._enigma_config,
                                        self._keep_acc.get(), self._keep_case.get(),
                                        self._language.get()))

    def _do_crack(self):
        self._set_result(enigma_crack(self._get_input(),self._enigma_config,
                                      self._keep_acc.get(), self._keep_case.get(),
                                      self._language.get()))
