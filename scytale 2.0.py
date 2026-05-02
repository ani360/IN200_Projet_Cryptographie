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

def décryptage_scytale2(texte_encodé):
    messages_par_clé = {}
    clé_maximale = len(texte_encodé)-1
    IC_text = calcul_IC(texte_encodé)
    une_lettre = frozenset(LangDictJson[lang]["lettres seules impossibles"])
    bigrammes = frozenset(LangDictJson[lang]["bigrammes impossibles"])
    dico_deux_lettres = frozenset(LangDictJson[lang]["mots deux lettres possibles"])
    dico_trois_lettres = frozenset(LangDictJson[lang]["mots trois lettres possibles"])
    
    for clé in range(2, clé_maximale):
        messages_par_clé[clé] = décryptage_scytale2_cle(texte_encodé, clé).split()
    
    b = frozenset(messages_par_clé.keys())
    for clé in b :
        if frozenset(messages_par_clé[clé]).isdisjoint(une_lettre) == False :
                del messages_par_clé[clé]
                break
    b = frozenset(messages_par_clé.keys())         
    for clé in b :
        for mot in messages_par_clé[clé] :
            if {mot[i:i+2] for i in range(len(mot)-1)}.isdisjoint(bigrammes) == False :       
                    del messages_par_clé[clé]
                    break

    b = frozenset(messages_par_clé.keys())            
    for clé in b :
        for mot in messages_par_clé[clé]: 
            if len(mot) ==2 :
                if mot not in dico_deux_lettres :
                    del messages_par_clé[clé]
                    break
    b = frozenset(messages_par_clé.keys())
    for clé in b :
        for mot in messages_par_clé[clé]:
            if len(mot)==3 :
                if mot not in dico_trois_lettres :
                    del messages_par_clé[clé]
                    break
    
    print(messages_par_clé)
    



if __name__ == "__main__":
    texte_essai = cryptage_scytale2("scytale spartiate", 4 )
    print(texte_essai)
    print(décryptage_scytale2(texte_essai, "french"))
    
