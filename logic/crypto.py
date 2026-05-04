"""
logic/crypto.py
================
Fonctions cryptographiques — PLACEHOLDERS
Remplace chaque corps de fonction par ta propre implémentation.
La signature et les paramètres sont intentionnellement stables.
"""

from __future__ import annotations
import json
import random
import string
import time
from logic.proper_vigener import vigenere_encode, vigenere_decode, vigenere_decrypt as vigenere_cracking
from logic.danielliv_accent_minuscule import caesar, decrypt_freq as caesar_decrypt_freq
from logic.Substitution_monoalphabetique import encode_monoalph, decode_monoalph, generer_alphabet
from logic.retake_substitution import mcmc_crack
from logic.scytale_2 import cryptage_scytale2, décryptage_scytale2_cle, craquage_scytale
from logic.Enigma.Enigma import EnigmaMachine, setup_generator
from logic.Enigma.Enigma_decrypter import crack_enigma


# ─────────────────────────────────────────────
#  Helpers communs
# ─────────────────────────────────────────────
"""
def preprocess(text: str, keep_accents: bool, keep_case: bool) -> str:
    "
    Normalise le texte avant traitement.
    - keep_accents : si False, remplace les caractères accentués par leur équivalent ASCII
    - keep_case    : si False, met tout en majuscules
    # TODO : implémenter la conversion accents → ASCII (ex: unicodedata)
    "
    if not keep_case:
        text = text.upper()
    if not keep_accents:
        # TODO: unicodedata.normalize('NFD', text) + filtrer les combinaisons
        pass
    return text
"""
# ─────────────────────────────────────────────
#  CÉSAR
# ─────────────────────────────────────────────

def caesar_encrypt(text: str, shift: int,
                   keep_accents: bool = True, keep_case: bool = True,
                   language: str = "french") -> str:
    """
    Chiffre `text` par le chiffre de César avec le décalage `shift`.
    """
    if keep_accents and language == "french" :
        language = "french_extended"
    txt = caesar(text, shift, language, keep_case, keep_accents)
    return f"[César chiffré | décalage={shift}] {txt}"


def caesar_decrypt(text: str, shift: int,
                   keep_accents: bool = True, keep_case: bool = True,
                   language: str = "french") -> str:
    """
    Déchiffre `text` par le chiffre de César avec le décalage `shift`.
    """
    if keep_accents and language == "french" :
        language = "french_extended"
    txt = caesar(text, -shift, language, keep_case, keep_accents)
    return f"[César déchiffré | décalage={shift}] {txt}"


def caesar_crack(text: str, keep_accents: bool = True,
                 keep_case: bool = True, language: str = "french") -> str:
    """
    Attaque par force brute — teste les 25 décalages possibles.
    Retourne le résultat le plus probable selon l'analyse de fréquence.
    """
    if keep_accents and language == "french" :
        language = "french_extended"
    shift, txt = caesar_decrypt_freq(text, language, keep_accents, keep_case)
    return f"[César cracké | décalage={shift}] {txt}"


# ─────────────────────────────────────────────
#  VIGENÈRE
# ─────────────────────────────────────────────

def vigenere_encrypt(text: str, key: str,
                     keep_accents: bool = True, keep_case: bool = True,
                     language: str = "french") -> str:
    """
    Chiffre `text` avec le chiffre de Vigenère et la clé `key`.
    """
    if keep_accents and language == "french" :
        language = "french_extended"
    text = vigenere_encode(text, key, language, keep_case)
    return f"[Vigenère chiffré | clé={key!r}] {text}"


def vigenere_decrypt(text: str, key: str,
                     keep_accents: bool = True, keep_case: bool = True,
                     language: str = "french") -> str:
    """
    Déchiffre `text` avec le chiffre de Vigenère et la clé `key`.
    """
    if keep_accents and language == "french" :
        language = "french_extended"
    text = vigenere_decode(text, key, language, keep_case)
    return f"[Vigenère déchiffré | clé={key!r}] {text}"


def vigenere_crack(text: str, keep_accents: bool = True,
                   keep_case: bool = True, language: str = "french") -> str:
    """
    Attaque Kasiski / Friedman pour retrouver la clé Vigenère.
    """
    if keep_accents and language == "french" :
        language = "french_extended"
    key, txt = vigenere_cracking(text, language, keep_case)
    return f"[Vigenère cracké | clé={key!r}] {txt}"


# ─────────────────────────────────────────────
#  SUBSTITUTION
# ─────────────────────────────────────────────

def substitution_encrypt(text: str, alphabet_key: str,
                         keep_accents: bool = True, keep_case: bool = True,
                         language: str = "french") -> str:
    """
    Chiffre `text` par substitution monoalphabétique.
    `alphabet_key` : 26 lettres représentant le nouvel alphabet (ex: 'QWERTYUIOPASDFGHJKLZXCVBNM')
    """
    if keep_accents and language == 'french':
        language = 'french_extended'
    text = encode_monoalph(text, alphabet_key, language, keep_case, keep_accents)
    return f"[Substitution chiffré | alphabet={alphabet_key!r}] {text}"


def substitution_decrypt(text: str, alphabet_key: str,
                         keep_accents: bool = True, keep_case: bool = True,
                         language: str = "french") -> str:
    """
    Déchiffre `text` par substitution monoalphabétique (inverse de `alphabet_key`).
    """
    if keep_accents and language == 'french':
        language = 'french_extended'
    text = decode_monoalph(text, alphabet_key, language, keep_case, keep_accents)
    return f"[Substitution déchiffré | alphabet={alphabet_key!r}] {text}"


def substitution_crack(text: str, keep_accents: bool = True,
                       keep_case: bool = True, language: str = "french", iter:int = 10000) -> str:
    """
    Attaque par analyse de fréquence pour la substitution monoalphabétique.
    # TODO : comparer les fréquences du texte aux fréquences de la langue
    """
    key, txt = mcmc_crack(text, language, iter)
    alph = ''.join(key[a] for a in key.keys())
    return f"Alphabet probable : {alph}, texte : {txt}"


def rng_alph(language : str = 'french', keep_accents : bool = True) :
    if keep_accents and language == 'french':
        language = 'french_extended'
    return(generer_alphabet(language))


# ─────────────────────────────────────────────
#  SCYTALE
# ─────────────────────────────────────────────

def scytale_encrypt(text: str, diameter: int,
                    keep_accents: bool = True, keep_case: bool = True,
                    language: str = "french") -> str:
    """
    Chiffre `text` avec la Scytale (transposition par colonne).
    `diameter` : nombre de colonnes (= diamètre du bâton)
    """
    text = cryptage_scytale2(text, diameter)
    return f"[Scytale chiffré | diamètre={diameter}] '{text}'"


def scytale_decrypt(text: str, diameter: int,
                    keep_accents: bool = True, keep_case: bool = True,
                    language: str = "french") -> str:
    """
    Déchiffre `text` avec la Scytale.
    """
    print(f"DEBUG reçu: {repr(text)}")   # ← affiche les espaces/caractères invisibles
    print(f"DEBUG longueur: {len(text)}")
    txt = décryptage_scytale2_cle(text, diameter)
    return f"[Scytale déchiffré | diamètre={diameter}] '{txt}'"


def scytale_crack(text: str, keep_accents: bool = True,
                  keep_case: bool = True, language: str = "french") -> str:
    """
    Attaque par force brute — teste tous les diamètres possibles.
    """
    if keep_accents and language == 'french':
        language = 'french_extended'
    score, cle, text = craquage_scytale(text, language)
    return f"Score : {score}, Clée : {cle}, Texte : {text}"


# ─────────────────────────────────────────────
#  ENIGMA
# ─────────────────────────────────────────────

def enigma_generate_config(num_rotors: int = 3, num_plugboard: int = 10, language : str = 'french') -> dict:
    return(setup_generator(num_rotors,num_plugboard, language, False))


def enigma_encrypt(text: str, config: dict,
                   keep_accents: bool = True, keep_case: bool = True,
                   language: str = "french") -> str:
    text = EnigmaMachine(language, config).process_text(text)
    return f"[Enigma chiffré]\n{text}"


def enigma_decrypt(text: str, config: dict,
                   keep_accents: bool = True, keep_case: bool = True,
                   language: str = "french") -> str:
    text = EnigmaMachine(language, config).process_text(text)
    return f"[Enigma déchiffré]\n{text}"


def enigma_crack(text: str, config: dict, keep_accents: bool = True,
                 keep_case: bool = True, language: str = "french") -> str:
    """
    Attaque de la machine Enigma (ex: méthode de la bombe).
    """
    timestamp = int(round(int(config['creation'])))
    return crack_enigma(text, language, timestamp, 10, max_rotors=10, max_ncables=10)
