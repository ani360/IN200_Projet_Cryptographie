import unicodedata
import json
from pathlib import Path

script_dir = Path(__file__).parent
LangDict_path = script_dir.parent / "LangDict.json"

with open(LangDict_path, 'r', encoding='utf-8') as f: 
    LangDictJson = json.load(f)

def sanitize(input_str):
    normalized = unicodedata.normalize('NFD', input_str)
    result = "".join(char for char in normalized if unicodedata.category(char) != 'Mn')
    final_list_char = []
    for char in result:
        if char.isalpha() or char.isspace():
            final_list_char.append(char.upper())
    return "".join(final_list_char)

def caesar(message, cle, alphabet):
    message_chiffre = ""
    taille = len(alphabet)
    for letter in message:
        if letter in alphabet:
            index = alphabet.find(letter)
            nouvel_index = (index + cle) % taille
            message_chiffre += alphabet[nouvel_index]
        else:
            message_chiffre += letter
    return message_chiffre

def brute_force(message, alphabet):
    tentatives_bruteforce = {}
    message_propre = sanitize(message)
    for k in range(len(alphabet)):
        tentatives_bruteforce[k] = caesar(message_propre, -k, alphabet)
    return tentatives_bruteforce


    
    

######## Remy comment ca marche l'analyse de frequence si j'ai bien compris je dois trouver la lettre la plus fréquente dans le texte puis je regarde dans  JSON quelle est la lettre la plus fréquente pour la langue choisie pour ensuite calculer la distance entre les deux pour en deduire la clé c'et bien ca ?
#pour l'analyse de frequence tu peut te baser sur ce que j'ai fait dans la class caesar de test crypto (attention j'ai aucune idée de si il  marche car je vien de le modifier) :

"""
def decrypt_freq(input : str, lang : str) -> int: #trouve la clée corresspondante par analyse de fréquence.
        l = float(len(input))
        dict_freq = LangDictJson[lang]['PP']
        alphabet = LangDictJson[lang]['alphabet']
        score : list = [0, 100]
        input = sanitize(input)
        for i in range (26):
            diff = sum(abs(b - dict_freq[a]) for a, b in enumerate([100 * lettre / l for lettre in map(input.count, alphabet)]))
            if diff < score[1]: 
                score = i, diff
            input : str = caesar(input, 1, alphabet)
        return score[0]
"""

#pour le main() je t'avais dit d'oublier, tu ne demande rien a l'utilisateur tu code juste les fonction je veut pas voir un input()
#qd tu fait  un test pour run ton code tu met : 
if __name__ == "__main__":
    langue_choisie = "french"
    alphabet = LangDictJson[langue_choisie]["alphabet"]
    texte_depart = "danièlli8!"
    cle_s= 1

    
    msg_propre = sanitize(texte_depart)
    print("Message propre :", msg_propre)
    
    msg_crypte = caesar(msg_propre, cle_s, alphabet)
    print("Message crypte + clé :", msg_crypte, cle_s)
    
    
    resultats = brute_force(msg_crypte, alphabet)
    
    for k in range(5):
        print("Decalage", k, ":", resultats[k])    
        
