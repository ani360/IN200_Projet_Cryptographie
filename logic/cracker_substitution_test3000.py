"""
Crackeur de chiffrement par substitution monoalphabétique
=========================================================
Méthode : analyse de fréquences + hill-climbing stochastique (recuit simulé)

Hypothèses :
  - L'alphabet source est connu et ordonné (ex : ABCDEFGHIJKLMNOPQRSTUVWXYZ)
  - Au plus len(alphabet)//2 lettres ont été substituées
  - Le texte chiffré est suffisamment long pour que l'analyse statistique soit fiable

Utilisation :
  python crack_substitution.py

  Ou en import :
    from crack_substitution import crack
    cle, texte_clair = crack(texte_chiffre, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", langue="fr")
"""

import random
import math
import string
import re
from collections import Counter
from typing import Optional


# ---------------------------------------------------------------------------
# 1.  STATISTIQUES DE RÉFÉRENCE  (fréquences français / anglais)
# ---------------------------------------------------------------------------

# Fréquences de lettres (%) — source : analyse de corpus
FREQUENCES_FR = {
    'A': 7.636, 'B': 0.901, 'C': 3.260, 'D': 3.669, 'E': 14.715,
    'F': 1.066, 'G': 0.866, 'H': 0.737, 'I': 7.529, 'J': 0.613,
    'K': 0.049, 'L': 5.456, 'M': 2.968, 'N': 7.095, 'O': 5.378,
    'P': 3.021, 'Q': 1.362, 'R': 6.553, 'S': 7.948, 'T': 7.244,
    'U': 6.311, 'V': 1.628, 'W': 0.114, 'X': 0.387, 'Y': 0.308,
    'Z': 0.136,
}

FREQUENCES_EN = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
    'Z': 0.074,
}

# Bigrammes les plus fréquents en français (normalisés)
BIGRAMMES_FR = [
    'ES', 'LE', 'DE', 'EN', 'NT', 'ON', 'RE', 'TE', 'ER',
    'AN', 'SE', 'ET', 'IS', 'UN', 'AL', 'IT', 'OU', 'QU',
    'LA', 'EM', 'UT', 'LI', 'RI', 'AT', 'AI', 'ME', 'EC',
    'RA', 'IO', 'ND', 'ED', 'OR', 'EL', 'LE', 'IE', 'UR',
]

BIGRAMMES_EN = [
    'TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN',
    'ND', 'TI', 'ES', 'OR', 'TE', 'OF', 'ED', 'IS', 'IT',
    'AL', 'AR', 'ST', 'TO', 'NT', 'NG', 'SE', 'HA', 'AS',
    'OU', 'IO', 'LE', 'VE', 'CO', 'ME', 'DE', 'HI', 'RI',
]

LANGUES = {
    'fr': (FREQUENCES_FR, BIGRAMMES_FR),
    'en': (FREQUENCES_EN, BIGRAMMES_EN),
}


# ---------------------------------------------------------------------------
# 2.  SCORE D'UN DÉCHIFFREMENT
# ---------------------------------------------------------------------------

def score_texte(texte: str, freq_ref: dict, bigr_ref: list) -> float:
    """
    Calcule un score de vraisemblance linguistique pour `texte`.
    Plus le score est élevé, plus le texte ressemble à la langue cible.

    Composantes :
      - Corrélation de Pearson entre fréquences observées et référence  (60 %)
      - Proportion de bigrammes de référence présents dans le texte     (40 %)
    """
    lettres = re.sub(r'[^A-Z]', '', texte.upper())
    if not lettres:
        return -1e9

    n = len(lettres)
    total = Counter(lettres)

    # --- fréquences observées vs référence ---
    mots_ref = list(freq_ref.keys())
    obs   = [total.get(l, 0) / n * 100 for l in mots_ref]
    ref   = [freq_ref[l] for l in mots_ref]

    moy_obs = sum(obs) / len(obs)
    moy_ref = sum(ref) / len(ref)
    num = sum((o - moy_obs) * (r - moy_ref) for o, r in zip(obs, ref))
    den_obs = math.sqrt(sum((o - moy_obs) ** 2 for o in obs) + 1e-10)
    den_ref = math.sqrt(sum((r - moy_ref) ** 2 for r in ref) + 1e-10)
    correlation = num / (den_obs * den_ref)

    # --- bigrammes ---
    bigrammes_obs = Counter(lettres[i:i+2] for i in range(n - 1))
    total_bigr = sum(bigrammes_obs.values()) or 1
    score_bigr = sum(bigrammes_obs.get(b, 0) for b in bigr_ref) / total_bigr

    return 0.6 * correlation + 0.4 * score_bigr


# ---------------------------------------------------------------------------
# 3.  APPLICATION / INVERSION D'UNE CLÉ
# ---------------------------------------------------------------------------

def appliquer_cle(texte: str, cle: dict) -> str:
    """Déchiffre `texte` en remplaçant chaque lettre selon `cle` (chiffré→clair)."""
    resultat = []
    for c in texte:
        cu = c.upper()
        if cu in cle:
            d = cle[cu]
            resultat.append(d if c.isupper() else d.lower())
        else:
            resultat.append(c)
    return ''.join(resultat)


def inverser_cle(cle_chiffrement: dict) -> dict:
    """Transforme clair→chiffré en chiffré→clair."""
    return {v: k for k, v in cle_chiffrement.items()}


# ---------------------------------------------------------------------------
# 4.  INITIALISATION PAR FRÉQUENCES
# ---------------------------------------------------------------------------

def initialiser_cle_par_frequences(texte_chiffre: str,
                                    alphabet: str,
                                    freq_ref: dict) -> dict:
    """
    Construit une première proposition de clé de déchiffrement en appariant
    les lettres par rang de fréquence (chiffré ↔ clair).

    Renvoie un dict  chiffré → clair  pour les lettres qui semblent substituées.
    Les lettres non substituées sont laissées identiques.
    """
    lettres = re.sub(r'[^A-Z]', '', texte_chiffre.upper())
    if not lettres:
        return {c: c for c in alphabet}

    freq_obs = Counter(lettres)

    # Trier l'alphabet chiffré par fréquence décroissante
    alpha_chiffre_tri = sorted(alphabet, key=lambda l: freq_obs.get(l, 0), reverse=True)
    # Trier l'alphabet clair par fréquence décroissante
    alpha_clair_tri   = sorted(alphabet, key=lambda l: freq_ref.get(l, 0), reverse=True)

    cle = {}
    for c_chiffre, c_clair in zip(alpha_chiffre_tri, alpha_clair_tri):
        cle[c_chiffre] = c_clair

    return cle  # chiffré → clair


# ---------------------------------------------------------------------------
# 5.  HILL-CLIMBING (recuit simulé)
# ---------------------------------------------------------------------------

def hill_climbing(texte_chiffre: str,
                  alphabet: str,
                  freq_ref: dict,
                  bigr_ref: list,
                  max_substitutions: int,
                  iterations: int = 10_000,
                  temperature_init: float = 5.0,
                  cooling: float = 0.9995,
                  graine: Optional[int] = None) -> tuple[dict, float]:
    """
    Optimise la clé de déchiffrement par recuit simulé.

    À chaque itération :
      - On tire aléatoirement deux lettres de l'alphabet et on échange
        leurs correspondances dans la clé courante.
      - On accepte le nouvel état si le score s'améliore, ou avec une
        probabilité exp(ΔS/T) si le score baisse (exploration).
      - La température T décroît exponentiellement.

    Contrainte : au plus `max_substitutions` lettres diffèrent de l'identité.

    Retourne (meilleure_cle_chiffre_vers_clair, meilleur_score).
    """
    rng = random.Random(graine)

    # Clé initiale par fréquences
    cle = initialiser_cle_par_frequences(texte_chiffre, alphabet, freq_ref)

    def score_cle(k):
        clair = appliquer_cle(texte_chiffre, k)
        return score_texte(clair, freq_ref, bigr_ref)

    score_courant = score_cle(cle)
    meilleure_cle = dict(cle)
    meilleur_score = score_courant

    T = temperature_init
    lettres = list(alphabet)

    for _ in range(iterations):
        # Choisir deux positions distinctes dans l'alphabet et échanger
        i, j = rng.sample(range(len(lettres)), 2)
        li, lj = lettres[i], lettres[j]

        nouvelle_cle = dict(cle)
        nouvelle_cle[li], nouvelle_cle[lj] = nouvelle_cle[lj], nouvelle_cle[li]

        # Vérifier la contrainte de max_substitutions
        nb_sub = sum(1 for l in lettres if nouvelle_cle[l] != l)
        if nb_sub > max_substitutions:
            T *= cooling
            continue

        nouveau_score = score_cle(nouvelle_cle)
        delta = nouveau_score - score_courant

        if delta > 0 or rng.random() < math.exp(delta / (T + 1e-10)):
            cle = nouvelle_cle
            score_courant = nouveau_score
            if score_courant > meilleur_score:
                meilleure_cle = dict(cle)
                meilleur_score = score_courant

        T *= cooling

    return meilleure_cle, meilleur_score


# ---------------------------------------------------------------------------
# 6.  FONCTION PRINCIPALE DE CRACKAGE
# ---------------------------------------------------------------------------

def crack(texte_chiffre: str,
          alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
          langue: str = 'fr',
          nb_essais: int = 5,
          iterations_par_essai: int = 150000) -> tuple[dict, str]:
    """
    Tente de retrouver la clé de substitution et le texte clair.

    Paramètres
    ----------
    texte_chiffre       : texte à décrypter
    alphabet            : alphabet source (ordonné), connu à l'avance
    langue              : 'fr' ou 'en' pour les statistiques de référence
    nb_essais           : nombre de redémarrages aléatoires (robustesse)
    iterations_par_essai: itérations de recuit simulé par essai

    Retourne
    --------
    (cle_dechiffrement, texte_clair)
    cle_dechiffrement : dict  lettre_chiffree → lettre_claire
    """
    if langue not in LANGUES:
        raise ValueError(f"Langue '{langue}' non supportée. Choisissez parmi : {list(LANGUES)}")

    freq_ref, bigr_ref = LANGUES[langue]
    alphabet = alphabet.upper()
    max_sub = len(alphabet) // 2

    meilleure_cle   = {c: c for c in alphabet}
    meilleur_score  = -1e9

    for essai in range(nb_essais):
        graine = essai * 1337
        cle, score = hill_climbing(
            texte_chiffre,
            alphabet,
            freq_ref,
            bigr_ref,
            max_substitutions=max_sub,
            iterations=iterations_par_essai,
            graine=graine,
        )
        print(f"  Essai {essai + 1}/{nb_essais}  →  score = {score:.4f}")
        if score > meilleur_score:
            meilleur_score = score
            meilleure_cle  = cle

    texte_clair = appliquer_cle(texte_chiffre, meilleure_cle)
    return meilleure_cle, texte_clair


# ---------------------------------------------------------------------------
# 7.  UTILITAIRES
# ---------------------------------------------------------------------------

def chiffrer(texte: str, cle_chiffrement: dict) -> str:
    """
    Chiffre `texte` avec la clé clair→chiffré fournie.
    Pratique pour générer des cas de test.
    """
    resultat = []
    for c in texte:
        cu = c.upper()
        if cu in cle_chiffrement:
            d = cle_chiffrement[cu]
            resultat.append(d if c.isupper() else d.lower())
        else:
            resultat.append(c)
    return ''.join(resultat)


def afficher_cle(cle: dict, alphabet: str) -> None:
    """Affiche joliment la clé de déchiffrement."""
    alpha = alphabet.upper()
    print("Clé trouvée (chiffré → clair) :")
    print("  Chiffré : " + " ".join(alpha))
    print("  Clair   : " + " ".join(cle.get(c, c) for c in alpha))
    subs = [(c, cle[c]) for c in alpha if cle.get(c, c) != c]
    if subs:
        print(f"\n  Substitutions actives ({len(subs)}) :")
        for chiffre, clair in subs:
            print(f"    {chiffre} → {clair}")
    else:
        print("  Aucune substitution détectée (texte déjà en clair ?).")


# ---------------------------------------------------------------------------
# 8.  DÉMONSTRATION
# ---------------------------------------------------------------------------

def demo():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # --- Texte source (extrait littéraire français) ---
    texte_clair_original = (
        "La cryptographie est la science et l'art de transformer des messages afin de les rendre inintelligibles pour ceux qui ne disposent pas d'une clé secrète. Elle joue un rôle fondamental dans la sécurité informatique moderne. Les chiffrements par substitution furent parmi les premiers "
        "systèmes utilisés dans l'histoire. Jules César lui-même employait un "
        "décalage simple pour protéger ses communications militaires. Aujourd'hui, "
        "l'analyse des fréquences permet de casser ces codes en comparant la "
        "distribution des lettres dans le message chiffré avec celles de la langue "
        "naturelle. Cette méthode statistique est très efficace dès lors que le "
        "texte chiffré est suffisamment long pour être représentatif."
    ).upper()

    # --- Construction d'une clé de chiffrement aléatoire (≤ 13 substitutions) ---
    nb_substitutions = random.randint(3, 13)
    lettres_modifiables = list(alphabet)
    random.shuffle(lettres_modifiables)
    paires = []
    pool = lettres_modifiables[:]
    for _ in range(nb_substitutions):
        if len(pool) < 2:
            break
        a, b = pool.pop(), pool.pop()
        paires.append((a, b))

    cle_chiffrement = {c: c for c in alphabet}  # identité par défaut
    for a, b in paires:
        cle_chiffrement[a] = b
        cle_chiffrement[b] = a

    subs_reelles = [(c, cle_chiffrement[c]) for c in alphabet if cle_chiffrement[c] != c]
    print("=" * 60)
    print("DÉMONSTRATION — Crackeur de substitution monoalphabétique")
    print("=" * 60)
    print(f"\nNombre de substitutions secrètes : {len(subs_reelles) // 2}")
    print("Clé de chiffrement réelle (clair → chiffré) :")
    for a, b in paires:
        print(f"  {a} ↔ {b}")

    # --- Chiffrement ---
    texte_chiffre = chiffrer(texte_clair_original, cle_chiffrement)
    print(f"\nTexte clair (extrait) :\n  {texte_clair_original[:120]}...")
    print(f"\nTexte chiffré (extrait) :\n  {texte_chiffre[:120]}...")

    # --- Crackage ---
    print("\n--- Lancement du crackage ---")
    cle_trouvee, texte_clair_trouve = crack(
        texte_chiffre,
        alphabet=alphabet,
        langue='fr',
        nb_essais=6,
        iterations_par_essai=200000,
    )

    # --- Résultats ---
    print("\n--- Résultats ---")
    afficher_cle(cle_trouvee, alphabet)

    # Calcul de la précision
    nb_correct = sum(1 for c in alphabet if cle_trouvee.get(c, c) == cle_chiffrement.get(c, c))
    precision = nb_correct / len(alphabet) * 100
    print(f"\nPrécision de la clé trouvée : {nb_correct}/{len(alphabet)} lettres ({precision:.1f} %)")

    print(f"\nTexte déchiffré (extrait) :\n  {texte_clair_trouve[:120]}...")
    print(f"\nTexte original  (extrait) :\n  {texte_clair_original[:120]}...")

    # Comparer caractère par caractère
    n_lettres = sum(1 for c in texte_clair_original if c.isalpha())
    n_ok = sum(
        1 for a, b in zip(texte_clair_original, texte_clair_trouve)
        if a == b and a.isalpha()
    )
    print(f"\nPrécision sur le texte : {n_ok}/{n_lettres} lettres correctes ({n_ok/n_lettres*100:.1f} %)")
    print("=" * 60)


if __name__ == "__main__":
    demo()