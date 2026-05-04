# on importe les outils nécessaires
import json,unicodedata,random
from pathlib import Path

# on récupère le dossier où se trouve ce fichier
script_dir = Path(__file__).parent

# on construit le chemin vers le fichier JSON
LangDict_path = script_dir / "LangDict.json"

# on ouvre le fichier JSON et on le charge dans une variable
with open(LangDict_path, "r", encoding="utf-8") as f:
    LangDictJson = json.load(f)


# on définit la fonction sanitize pour nettoyer le texte
def sanitize(input: str) -> str:
    normalized = unicodedata.normalize("NFD", input)  # enlève les accents
    result = "".join(
        char for char in normalized
        if unicodedata.category(char) != "Mn"
    )

    final_list_char = []

    for char in result:
        if char.isalpha() or char.isspace():
            final_list_char.append(char.upper())

    return "".join(final_list_char)


# on crée la fonction de substitution monoalphabétique
def monoalph(input: str, Dsub: dict, lang: str):
    lang = lang.strip().lower()

    if lang not in LangDictJson:
        raise ValueError(f"Langue inconnue : {lang}. Langues disponibles : {list(LangDictJson.keys())}")

    input = sanitize(input)
    output = ""

    for el in input:
        if el.isalpha() and el in Dsub:
            output += Dsub[el]
        else:
            output += el

    return output


# on crée une clé aléatoire adaptée à l'alphabet
def config_generator(nsubstitution, lang):
    lang = lang.strip().lower()

    alphabet = LangDictJson[lang]["alphabet"]
    nsubstitution = nsubstitution % (len(alphabet) // 2)

    alphalist = list(alphabet)
    available_chars = alphalist.copy()

    random.shuffle(available_chars)

    dsub = {}

    for _ in range(nsubstitution):
        char_a = available_chars.pop()
        char_b = available_chars.pop()

        dsub[char_a] = char_b
        dsub[char_b] = char_a

    return dsub


# on inverse une clé pour passer du chiffrement au déchiffrement
def inverser_cle(cle):
    return {v: k for k, v in cle.items()}


# on applique une clé à un texte
def appliquer_cle(texte, cle_inverse):
    resultat = ""

    for c in texte:
        resultat += cle_inverse.get(c, c)

    return resultat


# fonction qui crée une clé complètement aléatoire
def cle_aleatoire(alphabet):
    lettres = list(alphabet)
    melange = lettres.copy()

    random.shuffle(melange)

    return dict(zip(lettres, melange))


# fonction de score avec les tétragrammes
def score_tetragrammes(texte, tetragrams):
    score = 0

    for tetra in tetragrams:
        score += texte.count(tetra)

    return score


# attaque par brute force limitée
def brute_force_substitution(texte_chiffre, lang="french", essais=5000):
    lang = lang.strip().lower()

    if lang not in LangDictJson:
        raise ValueError(f"Langue inconnue : {lang}. Langues disponibles : {list(LangDictJson.keys())}")

    data = LangDictJson[lang]
    alphabet = data["alphabet"]
    tetragrams = data["tetragrams"]

    texte = sanitize(texte_chiffre)

    meilleur_score = -1
    meilleur_texte = ""
    meilleure_cle = None

    for _ in range(essais):
        cle = cle_aleatoire(alphabet)
        cle_inverse = inverser_cle(cle)

        texte_test = appliquer_cle(texte, cle_inverse)
        score = score_tetragrammes(texte_test, tetragrams)

        if score > meilleur_score:
            meilleur_score = score
            meilleur_texte = texte_test
            meilleure_cle = cle_inverse

    return meilleur_texte, meilleure_cle, meilleur_score

#maintenant je fais par analyse de fréquence en utilisant les probabilités PP du JSON pour comparer les lettres les plus fréquentes du texte chiffré avec les letres les plus freéquentes de la langue choisi
from collections import Counter# pour trouver les lettres les plus fréquentes en comptant le nombre d'apparition 
# attaque par analyse de fréquence
def attaque_frequence(texte_chiffre, lang="french"):
    lang = lang.strip().lower()

    if lang not in LangDictJson:
        raise ValueError(f"Langue inconnue : {lang}. Langues disponibles : {list(LangDictJson.keys())}")

    data = LangDictJson[lang]

    alphabet = data["alphabet"]
    pp = data["PP"]

    texte = sanitize(texte_chiffre)

    compteur = Counter(c for c in texte if c in alphabet)

    lettres_chiffrees = [
        lettre for lettre, _ in compteur.most_common()
    ]

    lettres_langue = [
        lettre for _, lettre in sorted(zip(pp, alphabet), reverse=True)
    ]

    cle_inverse = dict(zip(lettres_chiffrees, lettres_langue))

    resultat = ""

    for c in texte:
        resultat += cle_inverse.get(c, c)

    return resultat, cle_inverse


# bloc final pour tester le programme
if __name__ == "__main__":
    print("Langues disponibles :", list(LangDictJson.keys()))

    texte = input("Écris le texte à coder : ")
    lang = input("Langue choisie (french, english...) : ").strip().lower()

    Dictsub = config_generator(12, lang)

    print("\n--- Clé de chiffrement ---")
    print(Dictsub)

    encoded = monoalph(texte, Dictsub, lang)

    print("\n--- Texte chiffré ---")
    print(encoded)

    cle_inverse = inverser_cle(Dictsub)
    decoded = monoalph(encoded, cle_inverse, lang)

    print("\n--- Texte déchiffré avec la clé connue ---")
    print(decoded)

    print("\n--- Analyse de fréquence ---")
    resultat_freq, cle_freq = attaque_frequence(encoded, lang)
    print(resultat_freq)
    print(cle_freq)

    print("\n--- Brute force ---")
    resultat_bf, cle_bf, score_bf = brute_force_substitution(encoded, lang, 5000)
    print(resultat_bf)
    print(cle_bf)
    print(score_bf)

