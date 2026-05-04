# on importe es outils necessaires 
import json, unicodedata, random, collections # pour respectivement lire le fichier Json ( dictionnaires des langues ), générer les accents ,une clé aléatoire 
from pathlib import Path # générer les chemins du fichier

 
script_dir = Path(__file__).parent #on récupére le dossier ou se trouve ce fichier
 
LangDict_path = script_dir / "LangDict.json"#on construit le chemin vers le fichier JSON

with open(LangDict_path, 'r', encoding='utf-8') as f: # on ouvre le fichier json et on le charge dans une variable 
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

def monoalph(input : str, Dsub : dict, lang):# on cree la fonctionne de substitution monoalphabetique 
    alphabet : str = LangDictJson[lang]['alphabet']#on recupere l'alpabet de la langue 
    input = sanitize(input)#on nettoie le texte 
    output : str = ''# rend le texte finale 
    for el in input :#on parcourt chaque lettre du texte 
        if el.isalpha() and el in Dsub.keys():#si c'est une lettre et qu'elle existe dans la clé
            output += Dsub[el]# on remplca avec la clé
        else :#sinon on garde le caractére tel quel
            output += el
    return(output)

#on créé une clé aléatoire adaptée à l'alphabet 
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

"""
if __name__ == "__main__":#ici notre code s'excécute seulement si on lance le fichier 
    Dictsub = config_generator(12, 'french')# pour créer la clé
    print(Dictsub)
    print(len(Dictsub))
    txt =  input ( " ecrivait le texte à coder :")# pour permettre à l'utilisateur de tester le texte 
    encoded = monoalph(txt, Dictsub, 'french')#chiffrement 
    print(encoded)
    #puisqu'on connait la clé pour faire le déchiffrement il suffit juste de faire l'inverse du dictionnaire 
    decoded = monoalph(encoded, Dictsub, 'french')
    print(decoded)
"""

#on crée un craquage du chiffrement càd dechiffré sans connaitre la clé 
#pour la substitution monoalphabatique je pense que tester toute les clés est impossible car il y'a enormement de permutations de l'alphabet 
#donc je crée une brute de force mais limitée genre plus intelligent quoi 
#pour se faire on génére plusieurs clés au hasard , on déchiffre avec chacune , on donne un score au texte obtenu et on garde le meil
#print (LangDictJson.keys())
def cle_aleatoire(alphabet):#fonction qui va créer une clé de substitution 
    lettres = list(alphabet)#on transforme ici l'alphabet ( str) en liste du genre "ABC" qui devient ["A","B"?"C"]
    melange = lettres.copy()#copie le liste
    random.shuffle(melange)#mélange les lettres 
    return dict(zip(lettres, melange))  # clair -> chiffré qui crée le dictionnaire 


def inverser_cle(cle):
    return {v: k for k, v in cle.items()}# k est la lettre d'origine et v la lettre remplacé on echange les deux pour inverser la clef


def appliquer_cle(texte, cle_inverse):#on prend le texte et on applique une clef 
    resultat = ""
    #on parcourt chaque lettre si la lettre existe dans la clef on remplce sinon on garde 
    for c in texte:
        resultat += cle_inverse.get(c, c)
    return resultat


def score_tetragrammes(texte, tetragrams):#fonctions qui dit si le texte ressemple à une langue ( francais)
    score = 0
    for tetra in tetragrams:#on parcourt des morceaux de mots fréquents ( tetragrals de remy dans la bibliothéque )
        score += texte.count(tetra)#plus il ya de mots fréquents meilleur est le score 
    return score

#on essaie pleins de cles et on garde la meilleure c'est notre fonction principale

def brute_force_substitution(texte_chiffre, lang="french", essais=5000):# j'ai choisi 5000 parcequ'en réalite on s'en fiche du nombre je veux juste répéter un nombre assez important de fois 
    data = LangDictJson[lang]#on recupere la langue 
    alphabet = data["alphabet"]
    tetragrams = data["tetragrams"]

    texte = sanitize(texte_chiffre)# on nettoie le texte (puree j'aime trop la fonction sanitize bangger)

#on initialise le meilleur resultat et le meilleur score 
    meilleur_score = -1
    meilleur_texte = ""
    meilleure_cle = None

    for _ in range(essais):#on répéte 5000 fois plus on est fou plus on rit 
        cle = cle_aleatoire(alphabet)#genre à chaque tour on génére au hasard
        cle_inverse = inverser_cle(cle)#pour dechiffrer 

        texte_test = appliquer_cle(texte, cle_inverse)#on déchiffre avec cette clé 
        score = score_tetragrammes(texte_test, tetragrams)#on regarde si le texte est logique 

        if score > meilleur_score:#si c'est mieux que les autres on garde le resultat 
            meilleur_score = score
            meilleur_texte = texte_test
            meilleure_cle = cle_inverse

    return meilleur_texte, meilleure_cle, meilleur_score
#enfin on renvoie le meilleur texte trouvé la clef et le score 

#maintenant je fais par analyse de fréquence en utilisant les probabilités PP du JSON pour comparer les lettres les plus fréquentes du texte chiffré avec les letres les plus freéquentes de la langue choisi
from collections import Counter# pour trouver les lettres les plus fréquentes en comptant le nombre d'apparition 

def attaque_frequence(texte_chiffre,lang="french"):
    print("langues disponibles : ", LangDictJson.keys())
    data = LangDictJson[lang]#on prend es données de langue choisi ( alphabet , PP , tetragrams )
    alphabet = data["alphabet"]#on recupere l'alphabet 
    pp = data["PP"]#on recupére la probabitlite de chaque lettre 

    texte = sanitize(texte_chiffre)#nettoyer mon texte 

    # on parcourt le texte lettre par lettre 
    # on garde seulement les lettres de l'alphabet
    #on compte combien de fois xchaque lettre apparait 
    compteur = Counter(c for c in texte if c in alphabet)
    lettres_chiffrees = [lettre for lettre, _ in compteur.most_common()]#on trie les lettres du plus fréquents au moins 

    # Lettres de la langue triées de la plus fréquente à la moins fréquente
    lettres_langue = [
        lettre for _, lettre in sorted(zip(pp, alphabet), reverse=True)#pour trier les lettres de la langue 
    ]

    # on crée le clé
    cle_inverse = dict(zip(lettres_chiffrees, lettres_langue))
    # puis on crée le texte finale  
    resultat = ""#texte vide 
    for c in texte:#on parcourt chaque lettre 
        resultat += cle_inverse.get(c, c)

    return resultat, cle_inverse #enfin on envoie le texte déchiffré avec la clef trouve 


def crack_monoalph(txt, lang):
    alphabet : str = LangDictJson[lang]["alphabet"]#on recupere l'alphabet 
    pp :  list = LangDictJson[lang]["PP"]#on recupére la probabitlite de chaque lettre

    paires = list(zip(alphabet, pp))
    paires_triees = sorted(paires, key=lambda x: x[1], reverse=True)
    alphabet_trie = "".join([p[0] for p in paires_triees])

    if lang != "french_extended":
        texte = sanitize(txt)#nettoyer mon texte
    else : 
        texte = "".join(l for l in txt.upper() if l.isalnum() or l.isspace())
    
    plaintxt = "".join(l for l in texte if l.isalpha())
    counts = collections.Counter(plaintxt)
    sorted_chars = [item[0] for item in counts.most_common()]
    alphabet_txt_trie = "".join(sorted_chars)

    # Création d'un dictionnaire de correspondance (Mapping)
    # On associe la lettre la plus fréquente trouvée au 'E', etc.
    mapping = {}
    for i in range(len(alphabet_txt_trie)):
        if i < len(alphabet_trie):
            mapping[alphabet_txt_trie[i]] = alphabet_trie[i]
    return(mapping)

#en gros pour le bloc final comme avec la création du chiffrement sert juste à lancer le programe et tester les deux méthode 
if __name__ == "__main__":
    txt = "On peut tous affirmer que nous avons un but dans la vie, un objectif a atteindre pour donner un sens a notre existence afin de la considérer accomplie. Cette finalité est a l’unanimité considérée comme le bonheur. La morale est une une loi universelle qui définit la raison chez les humains, présente dans nos pensées et qui définit ce qui est juste et injuste, bon ou mauvais, nous sommes tout de même libres d’y obéir mais elle fonde le comportement idéal de l’homme"
    lang = 'french'
    Dictsub = config_generator(12, lang)
    texte_chiffre = monoalph(txt,Dictsub ,'french')
    cle = crack_monoalph(texte_chiffre, 'french')
    print(cle)
    print(Dictsub)
    print(texte_chiffre)
    print(monoalph(texte_chiffre, cle, lang))

    """print("\n--- Analyse de fréquence ---")
    resultat_freq, cle_freq = attaque_frequence(texte_chiffre,"french")
    print(resultat_freq)
    print(cle_freq)
    print(monoalph(texte_chiffre,cle_freq ,'french'))"""


    """
    print("\n--- Brute force ---")
    resultat_bf, cle_bf, score_bf = brute_force_substitution(texte_chiffre, lang, 5000)
    print(resultat_bf)
    print(cle_bf)
    print(score_bf)
    """