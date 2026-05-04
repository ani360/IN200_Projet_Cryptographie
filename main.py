"""
CryptoTool - Interface Graphique de Cryptographie

Architecture :
  - main.py         : Point d'entrée, fenêtre principale
  - ui/             : Composants d'interface
  - logic/          : Fonctions cryptographiques (placeholders TODO)
"""

import customtkinter as ctk
from ui.app import CryptoApp

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = CryptoApp()
    app.mainloop()
