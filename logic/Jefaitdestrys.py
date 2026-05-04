"""
mcmc_cracker_v2.py — MCMC amélioré pour substitution monoalphabétique

Améliorations vs v1 :
  1. Modèle bigramme COMPLET et cohérent (pas de bonus arbitraire)
  2. Score multi-ordre : bigrammes + tétragrammes pondérés
  3. Redémarrages périodiques depuis best_key (évite la dérive)
  4. Recuit simulé avec schedule log-linéaire plus long
  5. Initialisation par analyse de fréquence (clé de départ meilleure)
"""

import json, math, unicodedata, random, collections
from pathlib import Path

# ─── Chargement ──────────────────────────────────────────────────────────────

script_dir    = Path(__file__).parent
LangDict_path = script_dir / "LangDict.json"

with open(LangDict_path, 'r', encoding='utf-8') as f:
    LangDictJson = json.load(f)

# ─── Sanitisation ────────────────────────────────────────────────────────────

def sanitize(text: str) -> str:
    normalized = unicodedata.normalize('NFD', text)
    result = "".join(c for c in normalized if unicodedata.category(c) != 'Mn')
    return "".join(c.upper() for c in result if c.isalpha() or c.isspace())


def monoalph(text: str, dsub: dict) -> str:
    return "".join(dsub.get(c, c) for c in text)

# ─── Amélioration 1 : modèle bigramme COMPLET ────────────────────────────────
#
# Principe : on estime P(AB) = P(A) * P(B|A)
# On n'a pas P(B|A) dans le JSON, mais on peut construire une matrice de
# transition réaliste depuis :
#   • les bigrammes connus (français) → probabilité haute
#   • les bigrammes absents             → interpolation de Laplace sur P(A)*P(B)
#
# Le résultat est un dict PLAT {bigram -> log_prob} couvrant TOUS les bigrammes
# possibles, sans discontinuité de score.

def build_bigram_model(lang: str) -> dict[str, float]:
    """
    Construit un modèle de log-probabilités bigrammes cohérent.

    Stratégie (interpolation linéaire) :
        log P(AB) = log[ λ * P_known(AB) + (1-λ) * P(A)*P(B) ]

    • Les bigrammes listés dans le JSON reçoivent P_known élevée (uniforme
      sur la liste, normalisée).
    • Les autres reçoivent uniquement P(A)*P(B).
    • λ = 0.7 : fort poids sur les bigrammes connus, mais pas de coupure nette.
    """
    data     = LangDictJson[lang]
    alphabet = data['alphabet']
    pp       = data['PP']
    freq     = {letter: pp[i] / 100.0 for i, letter in enumerate(alphabet)}

    known_bigrams: set[str] = set(data.get('bigrams', []))

    # Probabilité marginale de chaque bigramme connu (distribution uniforme)
    n_known   = len(known_bigrams) if known_bigrams else 1
    p_known   = 1.0 / n_known          # prob uniforme dans la liste connue

    lam       = 0.7                    # poids interpolation
    floor     = 1e-9

    model: dict[str, float] = {}
    for a in alphabet:
        for b in alphabet:
            bg        = a + b
            p_indep   = freq.get(a, floor) * freq.get(b, floor)
            p_bg      = lam * p_known + (1 - lam) * p_indep if bg in known_bigrams \
                        else (1 - lam) * p_indep
            model[bg] = math.log(max(p_bg, floor))

    return model, freq


def build_tetragram_model(lang: str, freq: dict) -> dict[str, float]:
    """
    Modèle de tétragrammes depuis la liste JSON.
    Les tétragrammes connus reçoivent un score élevé cohérent.
    Les inconnus reçoivent le score plancher (indépendance des lettres).
    Le score plancher est calibré pour être continu avec les connus.
    """
    data           = LangDictJson[lang]
    known_tetras   = data.get('tetragrams', [])
    n_known        = len(known_tetras) if known_tetras else 1
    floor          = 1e-9

    # Probabilité moyenne d'un tétragramme connu :
    # on veut que log P(connu) soit significativement > log P(inconnu)
    # On pose P(connu) = 1/(n_known) renormalisé sur l'alphabet^4
    p_known  = 1.0 / n_known

    model: dict[str, float] = {}
    for tg in known_tetras:
        tg = tg.upper()
        if len(tg) == 4 and all(c in freq for c in tg):
            model[tg] = math.log(max(p_known, floor))

    return model


# ─── Amélioration 2 : score multi-ordre ──────────────────────────────────────
#
# On combine bigrammes + tétragrammes avec pondération :
#   score = w_bi * Σ log P(bigram) + w_tetra * Σ log P(tetragram)
#
# Les bigrammes couvrent tout le texte sans trous → signal stable.
# Les tétragrammes guident vers les mots réels → signal fort mais bruité.

def score_text(text: str,
               bigram_model:   dict,
               tetra_model:    dict,
               freq:           dict,
               w_bi:   float = 1.0,
               w_tetra: float = 2.0) -> float:
    """
    Score log-vraisemblance combinant bigrammes et tétragrammes.
    Seules les lettres sont prises en compte (espaces ignorés).
    """
    letters = [c for c in text if c.isalpha()]
    if len(letters) < 2:
        return -1e9

    floor_indep = -30.0   # plancher pour n-gramme impossible

    # Bigrammes
    bi_score = 0.0
    for i in range(len(letters) - 1):
        bg = letters[i] + letters[i+1]
        bi_score += bigram_model.get(bg, floor_indep)

    # Tétragrammes
    tetra_score = 0.0
    if len(letters) >= 4:
        for i in range(len(letters) - 3):
            tg = "".join(letters[i:i+4])
            if tg in tetra_model:
                tetra_score += tetra_model[tg]
            else:
                # Indépendance : sum log P(lettre)
                tetra_score += sum(math.log(freq.get(c, 1e-9)) for c in tg)

    return w_bi * bi_score + w_tetra * tetra_score


# ─── Amélioration 3 : initialisation par analyse de fréquence ────────────────
#
# On trie les lettres du texte chiffré par fréquence décroissante et on les
# mappe sur les lettres de la langue cible dans le même ordre.
# C'est une clé de départ déjà raisonnable → l'algorithme part moins loin.

def freq_init_key(ciphertext: str, lang: str) -> dict:
    """Clé initiale par correspondance de fréquences."""
    data     = LangDictJson[lang]
    alphabet = list(data['alphabet'])
    pp       = data['PP']

    # Fréquences cibles triées par probabilité décroissante
    target_order = [letter for letter, _ in
                    sorted(zip(alphabet, pp), key=lambda x: -x[1])]

    # Fréquences observées dans le chiffré
    letters     = [c for c in ciphertext.upper() if c.isalpha() and c in alphabet]
    counter     = collections.Counter(letters)
    cipher_order = [c for c, _ in counter.most_common()]

    # Lettres du chiffré non observées → ajout à la fin
    unseen = [c for c in alphabet if c not in cipher_order]
    cipher_order += unseen

    key = {}
    for cipher_c, plain_c in zip(cipher_order, target_order):
        key[cipher_c] = plain_c
    # Lettres non couvertes → identité
    for c in alphabet:
        if c not in key:
            key[c] = c
    return key


# ─── Cœur MCMC avec redémarrages ─────────────────────────────────────────────

def mcmc_crack(ciphertext:     str,
               lang:           str   = 'french',
               n_iter:         int   = 50_000,
               T:              float = 1.0,
               restart_every:  int   = 5_000,
               restart_noise:  int   = 3,
               w_bi:           float = 1.0,
               w_tetra:        float = 2.0,
               freq_init:      bool  = True,
               seed:           int | None = None,
               verbose:        bool  = True,
               verbose_every:  int   = 5_000) -> tuple[dict, str, float]:
    """
    MCMC Metropolis-Hastings avec redémarrages périodiques.

    Paramètres clés
    ---------------
    restart_every : toutes les N itérations, si on n'a pas amélioré best,
                    on repart de best_key + restart_noise swaps aléatoires.
    restart_noise : nombre de swaps de perturbation au redémarrage.
    freq_init     : si True, initialise la clé par analyse de fréquence.
    w_bi / w_tetra: poids bigrammes / tétragrammes dans le score.
    """
    if seed is not None:
        random.seed(seed)

    alphabet    = list(LangDictJson[lang]['alphabet'])
    cipher_in   = sanitize(ciphertext)
    bigram_m, freq = build_bigram_model(lang)
    tetra_m        = build_tetragram_model(lang, freq)

    def decode(key):
        return monoalph(cipher_in, key)

    def sc(text):
        return score_text(text, bigram_m, tetra_m, freq, w_bi, w_tetra)

    # ── Clé initiale ──────────────────────────────────────────────────────────
    if freq_init:
        current_key = freq_init_key(cipher_in, lang)
    else:
        current_key = {c: c for c in alphabet}

    current_plain = decode(current_key)
    current_score = sc(current_plain)
    best_key, best_plain, best_score = current_key.copy(), current_plain, current_score
    last_improvement = 0
    accepted = 0

    # ── Boucle principale ─────────────────────────────────────────────────────
    for it in range(1, n_iter + 1):

        # Proposition : swap de deux lettres dans la clé
        a, b = random.sample(alphabet, 2)
        prop_key             = current_key.copy()
        prop_key[a], prop_key[b] = prop_key[b], prop_key[a]
        prop_plain = decode(prop_key)
        prop_score = sc(prop_plain)

        delta = prop_score - current_score
        if delta > 0 or random.random() < math.exp(delta / T):
            current_key, current_plain, current_score = prop_key, prop_plain, prop_score
            accepted += 1

        if current_score > best_score:
            best_key, best_plain, best_score = current_key.copy(), current_plain, current_score
            last_improvement = it

        # ── Amélioration 3 : redémarrage depuis best_key ──────────────────────
        if it - last_improvement >= restart_every:
            current_key = best_key.copy()
            # Petite perturbation aléatoire pour explorer le voisinage
            for _ in range(restart_noise):
                a, b = random.sample(alphabet, 2)
                current_key[a], current_key[b] = current_key[b], current_key[a]
            current_plain = decode(current_key)
            current_score = sc(current_plain)
            last_improvement = it
            if verbose:
                print(f"  ↺ redémarrage à l'itération {it}")

        if verbose and it % verbose_every == 0:
            rate = accepted / it * 100
            print(f"[{it:>7}/{n_iter}]  score={current_score:>12.1f}"
                  f"  best={best_score:>12.1f}"
                  f"  accept={rate:.1f}%"
                  f"  aperçu: {best_plain[:60]!r}")

    if verbose:
        print(f"\n{'─'*60}")
        print(f"Meilleur score   : {best_score:.2f}")
        print(f"Texte déchiffré  :\n{best_plain}")

    return best_key, best_plain, best_score


# ─── Recuit simulé amélioré ───────────────────────────────────────────────────

def run_annealing(ciphertext:     str,
                  lang:           str   = 'french',
                  T_start:        float = 8.0,
                  T_end:          float = 0.1,
                  n_stages:       int   = 15,
                  iter_per_stage: int   = 5_000,
                  restart_every:  int   = 8_000,
                  restart_noise:  int   = 2,
                  w_bi:           float = 1.0,
                  w_tetra:        float = 2.0,
                  freq_init:      bool  = True,
                  seed:           int | None = None,
                  verbose:        bool  = True) -> tuple[dict, str, float]:
    """
    Recuit simulé avec :
      - schedule log-linéaire (plus de temps en haute température)
      - redémarrages depuis best_key si stagnation
      - initialisation par fréquence
    """
    if seed is not None:
        random.seed(seed)

    alphabet    = list(LangDictJson[lang]['alphabet'])
    cipher_in   = sanitize(ciphertext)
    bigram_m, freq = build_bigram_model(lang)
    tetra_m        = build_tetragram_model(lang, freq)

    def decode(key):  return monoalph(cipher_in, key)
    def sc(text):     return score_text(text, bigram_m, tetra_m, freq, w_bi, w_tetra)

    current_key   = freq_init_key(cipher_in, lang) if freq_init else {c: c for c in alphabet}
    current_plain = decode(current_key)
    current_score = sc(current_plain)
    best_key, best_plain, best_score = current_key.copy(), current_plain, current_score
    last_improvement = 0
    total_iter = 0

    # Schedule log-linéaire : plus de temps aux T élevées
    log_start = math.log(T_start)
    log_end   = math.log(T_end)
    temps     = [math.exp(log_start + (log_end - log_start) * i / (n_stages - 1))
                 for i in range(n_stages)]

    for stage, T in enumerate(temps):
        accepted = 0
        for _ in range(iter_per_stage):
            total_iter += 1
            a, b = random.sample(alphabet, 2)
            pk             = current_key.copy()
            pk[a], pk[b]   = pk[b], pk[a]
            pp_            = decode(pk)
            ps             = sc(pp_)
            delta = ps - current_score
            if delta > 0 or random.random() < math.exp(delta / T):
                current_key, current_plain, current_score = pk, pp_, ps
                accepted += 1
            if current_score > best_score:
                best_key, best_plain, best_score = current_key.copy(), current_plain, current_score
                last_improvement = total_iter

            # Redémarrage si stagnation prolongée
            if total_iter - last_improvement >= restart_every:
                current_key = best_key.copy()
                for _ in range(restart_noise):
                    a, b = random.sample(alphabet, 2)
                    current_key[a], current_key[b] = current_key[b], current_key[a]
                current_plain = decode(current_key)
                current_score = sc(current_plain)
                last_improvement = total_iter

        if verbose:
            rate = accepted / iter_per_stage * 100
            print(f"Étape {stage+1:>2}/{n_stages}  T={T:.4f}"
                  f"  best={best_score:.1f}"
                  f"  accept={rate:.1f}%"
                  f"  aperçu: {best_plain[:55]!r}")

    if verbose:
        print(f"\nTexte déchiffré :\n{best_plain}")

    return best_key, best_plain, best_score


# ─── Utilitaires ─────────────────────────────────────────────────────────────

def index_of_coincidence(text: str) -> float:
    letters = [c for c in text.upper() if c.isalpha()]
    n = len(letters)
    if n < 2:
        return 0.0
    counter = collections.Counter(letters)
    return sum(v * (v - 1) for v in counter.values()) / (n * (n - 1))


def config_generator(nsubstitution: int, lang: str) -> dict:
    nsubstitution = nsubstitution % 14
    alphabet  = list(LangDictJson[lang]['alphabet'])
    available = alphabet[:]
    random.shuffle(available)
    dsub = {}
    for _ in range(nsubstitution):
        a = available.pop()
        b = available.pop()
        dsub[a] = b
        dsub[b] = a
    return dsub


# ─── Point d'entrée ───────────────────────────────────────────────────────────

if __name__ == '__main__':

    LANG      = 'french'
    PLAINTEXT = (
        "Le chiffrement par substitution monoalphabétique est une technique "
        "de cryptographie classique où chaque lettre du texte clair est "
        "remplacée par une lettre fixe du texte chiffré selon une clé secrète. "
        "Bien que simple à implémenter il est vulnérable à l analyse de "
        "fréquence car la distribution des lettres est conservée."
    )

    random.seed(42)
    true_key   = config_generator(10, LANG)
    inv_key    = {v: k for k, v in true_key.items()}
    ciphertext = monoalph(sanitize(PLAINTEXT), true_key)

    print("═" * 60)
    print("TEXTE CLAIR   :", sanitize(PLAINTEXT)[:80])
    print("TEXTE CHIFFRÉ :", ciphertext[:80])
    print(f"IC du chiffré  : {index_of_coincidence(ciphertext):.4f}")
    print("═" * 60, "\n")

    # ── Méthode 1 : MCMC avec redémarrages ───────────────────────────────────
    print("── MCMC avec redémarrages ──────────────────────────────")
    key1, plain1, sc1 = mcmc_crack(
        ciphertext, lang=LANG,
        n_iter=120_000, T=1.0,
        restart_every=5_000, restart_noise=3,
        w_bi=1.0, w_tetra=2.0,
        freq_init=True, seed=0, verbose=True, verbose_every=10_000
    )

    # ── Méthode 2 : Recuit simulé ─────────────────────────────────────────────
    print("\n── Recuit simulé amélioré ──────────────────────────────")
    key2, plain2, sc2 = run_annealing(
        ciphertext, lang=LANG,
        T_start=8.0, T_end=0.1,
        n_stages=15, iter_per_stage=5_000,
        restart_every=8_000, restart_noise=2,
        w_bi=1.0, w_tetra=2.0,
        freq_init=True, seed=0, verbose=True
    )

    # ── Comparaison ───────────────────────────────────────────────────────────
    alphabet = list(LangDictJson[LANG]['alphabet'])
    for label, key in [("MCMC", key1), ("Recuit", key2)]:
        correct = sum(1 for c in alphabet if key.get(c) == inv_key.get(c, c))
        print(f"\n{label} — Lettres correctes : {correct}/{len(alphabet)}")
    print("\nClé vraie :", {k: v for k, v in inv_key.items() if k != v})
    print("Clé MCMC  :", {k: v for k, v in key1.items() if k != v})
    print("Clé recuit:", {k: v for k, v in key2.items() if k != v})