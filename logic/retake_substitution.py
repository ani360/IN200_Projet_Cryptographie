# on importe es outils necessaires 
import json, math, unicodedata, random, collections # pour respectivement lire le fichier Json ( dictionnaires des langues ), générer les accents ,une clé aléatoire 
from pathlib import Path # générer les chemins du fichier
 
script_dir = Path(__file__).parent
LangDict_path = script_dir.parent / "LangDict.json"
with open(LangDict_path, 'r', encoding='utf-8') as f: #file path, read, utf-8
    LangDictJson = json.load(f)
#on definit donc la fonction sanitize pour nettoyer le texte 

def sanitize(input : str)->str :  
    normalized = unicodedata.normalize('NFD', input) # par exemple remplace é par e' donc virer les accents
    result = "".join(char for char in normalized if unicodedata.category(char) != 'Mn')#on enleve les accents catégorie "Mn"
    final_list_char = []#on parcourt chaque caractere 
    for char in result: 
        if char.isalpha() or char.isspace():#on garde uniquement les lettres et les espaces 
            final_list_char.append(char.upper())#on met tout en majuscule 
    return "".join(final_list_char)# on transforme la liste en texte 

def monoalph(input : str, Dsub : dict, lang): 
    alphabet : str = LangDictJson[lang]['alphabet']
    input = sanitize(input)
    output : str = '' 
    for el in input :
        if el.isalpha() and el in Dsub.keys():
            output += Dsub[el]
        else :
            output += el
    return(output)

def config_generator(nsubstitution, lang):
    nsubstitution = nsubstitution%14
    alphabet : str = LangDictJson[lang]['alphabet']
    alphalist = list(alphabet)
    available_chars = alphalist[:]
    random.shuffle(available_chars)
    dsub = {}
    for _ in range(nsubstitution):
        char_a = available_chars.pop()
        char_b = available_chars.pop()
        dsub[char_a] = char_b
        dsub[char_b] = char_a
    return(dsub)

def freq_to_letter_simple(text):
    # 1. On nettoie et on compte (en utilisant ta logique habituelle)
    clean_text = "".join(c.upper() for c in text if c.isalpha())
    total = len(clean_text)
    if total == 0: return {}
    counts = collections.Counter(clean_text)
    dico_pp = { (count / total) * 100 : char for char, count in counts.items() }
    
    return dico_pp

def get_score_mcmc(text, lang):
    """
    Calcule un score basé sur les tétragrammes et les structures de la langue.
    """
    # On récupère la liste des tétragrammes (4 lettres)
    freqs = frozenset(LangDictJson[lang].get('tetragrams', []))
    bigrams = frozenset(LangDictJson[lang].get('bigrams', []))
    score = 0
    voyelles = frozenset([e for e in "AEIOUY"])
    
    # 1. Score des Tétragrammes (Fenêtre de 4)
    for i in range(len(text) - 3):
        tetra = text[i:i+4]
        if tetra in freqs:
            score += 15  # Bonus important pour un mot/groupe connu

    for i in range(len(text) - 1):
        if text[i:i+2] in bigrams:
            score += 5

    # 2. Score de structure (Bruit de fond pour guider l'algo)
    # Aide l'algo à ne pas rester bloqué en privilégiant les alternances probables
    for i in range(len(text) - 1):
        # Bonus si on a une Voyelle suivie d'une Consonne (très fréquent)
        if text[i] in voyelles and text[i+1] not in voyelles:
            score += 1
            
    return score

def crack_mcmc(cipher_text, lang, iterations=100000):
    alphabet_str = LangDictJson[lang]['alphabet']
    alphabet = list(alphabet_str)
    
    # Initialisation
    current_key = alphabet[:]
    random.shuffle(current_key)
    
    def apply_key(text, key_list):
        table = str.maketrans(alphabet_str, "".join(key_list))
        return text.translate(table)

    current_text = apply_key(cipher_text, current_key)
    current_score = get_score_mcmc(current_text, lang)
    
    best_key = current_key[:]
    best_score = current_score
    
    last_improvement = 0

    for i in range(iterations):
        # PROPOSITION : On échange deux lettres au hasard
        idx1, idx2 = random.sample(range(len(alphabet)), 2)
        proposal_key = current_key[:]
        proposal_key[idx1], proposal_key[idx2] = proposal_key[idx2], proposal_key[idx1]
        
        proposal_text = apply_key(cipher_text, proposal_key)
        proposal_score = get_score_mcmc(proposal_text, lang)
        
        # ACCEPTATION (Metropolis-Hastings)
        diff = proposal_score - current_score
        # On accepte si c'est meilleur (diff > 0) 
        # ou avec une probabilité si c'est moins bon (pour sortir des plateaux)
        if diff > 0 or random.random() < math.exp(diff / 2.0):
            current_key = proposal_key
            current_score = proposal_score
            
            if current_score > best_score:
                best_score = current_score
                best_key = proposal_key[:]
                last_improvement = i

        # MÉCANISME ANTI-BLOCAGE (RESTART)
        # Si on n'a pas progressé depuis 15 000 itérations, on "secoue" la clé
        if i - last_improvement > 15000:
            current_key = best_key[:]
            for _ in range(3): # On fait 3 échanges aléatoires pour changer de zone
                a, b = random.sample(range(len(alphabet)), 2)
                current_key[a], current_key[b] = current_key[b], current_key[a]
            current_score = get_score_mcmc(apply_key(cipher_text, current_key), lang)
            last_improvement = i 

        if i % 5000 == 0:
            print(f"It {i} | Meilleur Score: {best_score} | {apply_key(cipher_text, best_key)[:60]}...")

    return apply_key(cipher_text, best_key)




def log_vraisemblance(text: str, log_tetragrams: dict, lang: str) -> float:
    """
    Calcule le score log-vraisemblance d'un texte basé sur les tétagrammes.
    Plus le score est élevé, plus le texte ressemble à la langue cible.
    """
    score = 0.0
    floor = math.log(1e-10)  # valeur plancher pour les tétagrammes inconnus
    for i in range(len(text) - 3):
        tetragram = text[i:i+4]
        if ' ' in tetragram:
            continue
        score += log_tetragrams.get(tetragram, floor)
    return score


def build_log_tetragrams(lang: str) -> dict:
    """
    Construit un dictionnaire de log-probabilités des tétagrammes
    à partir des fréquences de la langue (PP) en utilisant une estimation
    basée sur les PP individuelles comme approximation.
    On utilise ici directement la liste de tétagrammes du JSON comme présents/absents.
    """
    tetragrams_list = LangDictJson[lang]['tetragrams']
    # Chaque tétagramme connu reçoit une probabilité uniforme,
    # on normalise et on prend le log
    n = len(tetragrams_list)
    log_prob = math.log(1.0 / n)
    return {tg: log_prob for tg in tetragrams_list}


def apply_key(ciphertext: str, key: dict) -> str:
    """Déchiffre le texte avec la clé proposée."""
    return ''.join(key.get(c, c) for c in ciphertext)


def swap_two(key: dict) -> dict:
    """
    Génère une clé voisine en échangeant deux substitutions au hasard.
    C'est la "proposition" de Metropolis-Hastings.
    """
    new_key = key.copy()
    chars = list(new_key.keys())
    a, b = random.sample(chars, 2)
    # on échange les valeurs (ce à quoi a et b sont mappés)
    new_key[a], new_key[b] = new_key[b], new_key[a]
    return new_key


def mcmc_crack(ciphertext: str, lang: str,
               iterations: int = 10_000,
               verbose: bool = True) -> tuple[dict, str]:
    """
    Attaque par MCMC (Metropolis-Hastings) d'une substitution monoalphabétique.

    Paramètres
    ----------
    ciphertext  : texte chiffré (sera sanitisé automatiquement)
    lang        : langue cible (ex: 'french')
    iterations  : nombre d'itérations de la chaîne de Markov
    verbose     : affiche la progression toutes les 1000 itérations

    Retourne
    --------
    (best_key, best_plaintext) : la meilleure clé trouvée et le texte déchiffré
    """
    # --- Préparation ---
    ciphertext = sanitize(ciphertext)
    alphabet = LangDictJson[lang]['alphabet']           # ex: "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    log_tetragrams = build_log_tetragrams(lang)

    # Clé initiale aléatoire : permutation complète de l'alphabet
    shuffled = list(alphabet)
    random.shuffle(shuffled)
    current_key = dict(zip(alphabet, shuffled))

    # Évaluation initiale
    current_plain = apply_key(ciphertext, current_key)
    current_score = log_vraisemblance(current_plain, log_tetragrams, lang)

    best_key = current_key.copy()
    best_score = current_score
    best_plain = current_plain

    # --- Boucle MCMC ---
    for iteration in range(iterations):

        # 1. Proposer une clé voisine (swap de 2 lettres)
        proposed_key = swap_two(current_key)
        proposed_plain = apply_key(ciphertext, proposed_key)
        proposed_score = log_vraisemblance(proposed_plain, log_tetragrams, lang)

        # 2. Critère d'acceptation de Metropolis-Hastings
        #    On accepte toujours si le score s'améliore,
        #    sinon on accepte avec probabilité exp(delta)
        delta = proposed_score - current_score
        if delta > 0 or random.random() < math.exp(delta):
            current_key = proposed_key
            current_plain = proposed_plain
            current_score = proposed_score

        # 3. Mémoriser le meilleur état global
        if current_score > best_score:
            best_score = current_score
            best_key = current_key.copy()
            best_plain = current_plain

        # 4. Log de progression
        if verbose and (iteration + 1) % 1000 == 0:
            print(f"[{iteration+1:>6}] score={best_score:.2f} | aperçu: {best_plain[:60]}")

    return best_key, best_plain

if __name__ == "__main__":
    txt = "On peut tous affirmer que nous avons un but dans la vie, un objectif a atteindre pour donner un sens a notre existence afin de la considérer accomplie. Cette finalité est a l’unanimité considérée comme le bonheur. La morale est une une loi universelle qui définit la raison chez les humains, présente dans nos pensées et qui définit ce qui est juste et injuste, bon ou mauvais, nous sommes tout de même libres d’y obéir mais elle fonde le comportement idéal de l’homme"
    lang = 'french'
    Dictsub = config_generator(12, lang)
    texte_chiffre = monoalph(txt, Dictsub ,'french')
    #print(texte_chiffre)
    print(mcmc_crack(texte_chiffre, 'french', 100000))
    #print(freq_to_letter_simple(texte_chiffre))
    #print(crack_mcmc(texte_chiffre, lang, 500000))