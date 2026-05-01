# version historiquement conforme de la scytale (déchiffrable !!)

import json
from random import randint
from pathlib import Path
from Sanitizer import sanitize

script_dir = Path(__file__).parent
file_path = script_dir / "LangDict.json"

with open(file_path, 'r', encoding='utf-8') as f: #file path, read, utf-8
    LangDictJson = json.load(f)

def cryptage_scytale2(texte, clé): 
    nombre_colonnes = (len(texte)+clé-1)//clé
    ruban_sur_baton =[[] for k in range(clé)]
    message_encodé =""
    texte = sanitize(texte)
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


texte_essai = cryptage_scytale2("scytale spartiate", 4 )
    
print(texte_essai)
def décryptage_scytale2_cle(text, cle): 
    message_decrypte = ""
    k= 0
    b= 0
    while k < len(text) :
        if b > (len(text) - 1) : 
            b = (b % (len(text)-1))
        print(b)
        message_decrypte += text[b]
        b+= cle
        k+=1
    return(message_decrypte)

print(décryptage_scytale2_cle(texte_essai, 4))


# fonction de calcul de l'IC pour un texte et une langue donnée : 
def calcul_IC(txt, lang): 
    nbre_caracteres = len(txt)
    alphabt = LangDictJson[lang]['alphabet']
    somme = 0
    for char in alphabt : 
        B= txt.count(char)
        somme += (B**2 - B )
    
    return (somme/((nbre_caracteres)**2 - nbre_caracteres))






# fonction de décryptage en bruteforce 

def décryptage_scytale2(texte_encodé, lang):
    IClang = LangDictJson[lang]['IC']
    messages_par_clé = {}
    écart_ICpas_IClang = {}
    clés_textes_éligibles = []
    clé_maximale = len(texte_encodé)-1
    
    for k in range(2, clé_maximale):
        texte_du_pas= décryptage_scytale2_cle(texte_encodé, k)
        messages_par_clé[k] = texte_du_pas
  




    


    





