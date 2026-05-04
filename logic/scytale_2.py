# version historiquement conforme de la scytale (déchiffrable !!)
from math import log, gcd
import json, unicodedata
from pathlib import Path

script_dir = Path(__file__).parent
LangDict_path = script_dir.parent / "LangDict.json"
with open(LangDict_path, 'r', encoding='utf-8') as f: #file path, read, utf-8
    LangDictJson = json.load(f)

def sanitize(input_str, alphabet_visee, garder_accents=False, maj=False):
    if garder_accents:
        result="".join(i for i in input_str if i.isalnum() or  i.isspace())
    else:
        normalized = unicodedata.normalize('NFD', input_str)
        result = "".join(char for char in normalized if unicodedata.category(char) != 'Mn')
    final_list_char = []
    resultat_temporaire=result.upper()
    for char in resultat_temporaire:
        if char in alphabet_visee or char.isspace() or char.isnumeric() :
            final_list_char.append(char)
    return "".join(final_list_char)

def cryptage_scytale2(texte, clé):
    nombre_colonnes = (len(texte)+clé-1)//clé
    ruban_sur_baton =[[] for k in range(clé)]
    message_encodé =""
    #texte = sanitize(texte, alphabet, accents, maj)
    texte = ''.join(i for i in texte if i.isalnum() or i.isspace())
    for n in range (clé) : 
        for k in range (nombre_colonnes*n, nombre_colonnes*(n+1)):
            if k< len(texte) :
                ruban_sur_baton[n].append(texte[k])
            else :
                ruban_sur_baton[n].append(" ")
    for b in range(nombre_colonnes): 
        for k in range(clé): 
            message_encodé += ruban_sur_baton[k][b]
    return(message_encodé)

def décryptage_scytale2_cle(text, cle): 
    message_decrypte = ""
    k= 0
    b= 0
    while k < len(text) :
        if b > (len(text) - 1) : 
            b = (b % (len(text)-1))
        message_decrypte += text[b]
        b+= cle
        k+=1
    return(message_decrypte)




def calcul_score_tetra(texte, lang) :
    trétragrammes= frozenset(LangDictJson[lang]["tetragrams"])
    itérations_par_tétra = {}
    nombre_tetra = 0
    for tetra in trétragrammes :
        itérations_par_tétra[tetra] = texte.count(tetra)
    if nombre_tetra ==0 :
        score_tetra = 0
    else : 
        score_tetra = sum([log(itér/nombre_tetra) for itér in itérations_par_tétra.values() if itér != 0])

    return score_tetra


"""
def décryptage_scytale_log( texte_encodé, lang) :
    bigrammes = frozenset(LangDictJson[lang]["bigrammes impossibles"])
    messages_par_clé = {}
    scores_tetra = {}
    scores_bigrm_interdit = {}
    texte_encodé = sanitize(texte_encodé)

    for clé in range(2, len(texte_encodé)):
        messages_par_clé[clé]= décryptage_scytale2_cle(texte_encodé, clé).split()
        scores_bigrm_interdit[clé]= 0
    
    for clé in messages_par_clé.keys() :       
        mots_au_moins2_lettres = [mot for mot in messages_par_clé[clé] if len(mot) >=2 ]
        for mot in mots_au_moins2_lettres :
            scores_bigrm_interdit[clé]+= len({mot[i:i+2] for i in range(len(mot)-1)}.intersection(bigrammes))
            
    score_min = min(scores_bigrm_interdit.values())

    clés_éligibles = [clé for clé in scores_bigrm_interdit.keys() if scores_bigrm_interdit[clé] == score_min]
    if len(clés_éligibles) != 1 :
        for clé in clés_éligibles :
            scores_tetra[clé]= calcul_score(messages_par_clé[clé], lang)
    
        score_max = max([score for score in scores_tetra.values() if score != 0])
        textes_output = [" ".join(messages_par_clé[clé]) for clé in scores_tetra.keys() if scores_tetra[clé]== score_max]
        for texte in textes_output :
            print(texte)
    else :
        print(" ".join(messages_par_clé[clés_éligibles[0]]))
 """

def craquage_scytale(texte_encodé : str, lang : str) : 
    trigrammes = frozenset(LangDictJson[lang]["trigrams"])
    taille_texte = len(texte_encodé)
    scores_texte_avec_clé = []
    scores = []

    for clé in range(2, taille_texte - 1): 
        if gcd(taille_texte-1, clé)==1 :
            texte_clé = décryptage_scytale2_cle(texte_encodé, clé)
            score_clé = sum(texte_clé.upper().count(trig) for trig in trigrammes)
            if score_clé >0 : 
                scores.append(score_clé)
                scores_texte_avec_clé.append([score_clé, clé, texte_clé])

    for texte in scores_texte_avec_clé :
        if texte[0] == max(scores) :
            #print("score : "+ str(texte[0]) +", clé : "+ str(texte[1]) + ", texte décrypté : "+ texte[2])
            return texte[0], texte[1], texte[2]


if __name__ == "__main__":
    #txt = "On peut tous affirmer que nous avons un but dans la vie, un objectif a atteindre pour donner un sens a notre existence afin de la considérer accomplie. Cette finalité est a l’unanimité considérée comme le bonheur. La morale est une une loi universelle qui définit la raison chez les humains, présente dans nos pensées et qui définit ce qui est juste et injuste, bon ou mauvais, nous sommes tout de même libres d’y obéir mais elle fonde le comportement idéal de l’homme"
    txt = "S'cytale 26 é Spariate."
    #texte_essai2 = cryptage_scytale2(txt,5)
    texte_essai2 = 'Sl aeceér y  i t2Sa a6pt '
    print(f"'{texte_essai2}'")
    print(f"'{décryptage_scytale2_cle(texte_essai2, 5)}'")
    #décryptage_scytale_log("C:/Users/Utilisateur/Desktop/IN200/essaidc.txt", "voici un potentiel texte décrypté", texte_essai2, "french")
    print(craquage_scytale(texte_essai2, "french_extended"))