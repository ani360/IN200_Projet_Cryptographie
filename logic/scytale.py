import json
from random import randint as rng
from pathlib import Path
from Sanitizer import sanitize

script_dir = Path(__file__).parent
file_path = script_dir / "LangDict.json"

with open(file_path, 'r', encoding='utf-8') as f: #file path, read, utf-8
    LangDictJson = json.load(f)

# fonction de cryptage d'un texte en scytale avec la langue, le pas d'encodage et le texte en paramètres 
def cryptage_scytale(text,pas,lang):
    alphabet = LangDictJson[lang]['alphabet']
    L=len(alphabet)-1
    output = ''
    text = sanitize(text)
    text=''.join([a for a in text if a in alphabet])
    for char in text:
        output += char
        for k in range(pas):
            aléa = rng(0,L)
            output += alphabet[aléa]
    return(output)



# fonction de décodage d'un texte en scytale avec la clé 
def decodage_avec_cle(text_encode,clé):
    output= ''
    dernier_indice= len(text_encode) - 1
    for n in range(0, dernier_indice, clé):
        output += text_encode[n]
    return output

#alternative de la fonction ci-dessus pour être utilisée dans la fonction de décryptage sans clé

def lettres_texte_avec_pas(pas, dernier_indice, texte_encodé):
    output= ''
    for n in range(0, dernier_indice, pas):
        output += texte_encodé[n]
    return output




# fonction de calcul de l'IC pour un texte et une langue donnée : 
def calcul_IC(txt, lang): 
    nbre_caracteres = len(txt)
    alphabt = LangDictJson[lang]['alphabet']
    somme = 0
    for char in alphabt : 
        B= txt.count(char)
        somme += (B**2 - B )
    
    return (somme/((nbre_caracteres)**2 - nbre_caracteres))
    

#fonction de décryptage sans clé d'un texte encodé en scytale en fonction de la langue

def décryptage_scytale(texte_encodé, lang):
    IClang = LangDictJson[lang]['IC']
    indice_dernière_lettre = len(texte_encodé)-1
    messages_par_pas = {}
    écart_ICpas_IClang = {}
    clés_textes_éligibles = []
    longueur_texte = len(texte_encodé)


    
    if longueur_texte % 2 == 0 :
        pas_maximal = int(longueur_texte/2)
    else :
        pas_maximal = int((longueur_texte - 1)/2)
    
    for k in range(1, pas_maximal):
        texte_du_pas= lettres_texte_avec_pas(k, indice_dernière_lettre, texte_encodé)
        messages_par_pas[k] = texte_du_pas
        écart_ICpas_IClang[k] = abs(calcul_IC(texte_du_pas, lang) - IClang)
    
    valeursIC = écart_ICpas_IClang.values()
    valeur_min = min(valeursIC)
    for k, v in écart_ICpas_IClang.items() : 
        if v == valeur_min :
            clés_textes_éligibles.append(k)
    if len(clés_textes_éligibles) == 1 : 
        return messages_par_pas[clés_textes_éligibles[0]]
    else : 
        print("le programme rend plusieurs messages choisissez celui qui convient :")
        for k in clés_textes_éligibles :
              print(messages_par_pas[k])
















    
    


        



    

    






    


        





