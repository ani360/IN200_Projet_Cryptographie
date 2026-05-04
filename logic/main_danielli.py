import unicodedata
import json
from pathlib import Path

script_dir = Path(__file__).parent
LangDict_path = script_dir / "LangDict.json"

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

def caesar(message, cle, langue):
    alphabet = LangDictJson[langue]["alphabet"]
    message_chiffre = ""
    message_propre = sanitize(message)
    taille = len(alphabet)
    for letter in message_propre:
        if letter in alphabet:
            index = alphabet.find(letter)
            nouvel_index = (index + cle) % taille
            message_chiffre += alphabet[nouvel_index]
        else:
            message_chiffre += letter
    return message_chiffre

def brute_force(message, langue):
    alphabet = LangDictJson[langue]["alphabet"]
    tentatives = {}
    message_propre = sanitize(message)
    for k in range(len(alphabet)):
        tentatives[k] = caesar(message_propre, -k, langue)
    return tentatives
"""
#Cette fonction est INUTILE.
def analyse_de_frequence(message, langue):
    message_propre=sanitize(message) 
    dict_freq = LangDictJson[langue]['PP']
    alphabet = LangDictJson[langue]['alphabet']
    taille=len(message_propre)
    frequences_apparition_lettres={}
    for lettre in alphabet:
        nombre_apparition=message_propre.count(lettre)
        frequences_apparition_lettres[lettre]=(nombre_apparition/taille)*100
    return frequences_apparition_lettres


#Celle là aussi (sérieusement pourquoi ???).
def genere_toutes_les_scores(message, langue):
    alphabet = LangDictJson[langue]['alphabet']
    dict_freq_json = LangDictJson[langue]['PP']
    message_propre = sanitize(message)
    l = len(message_propre)
    if l == 0: 
        return {}
    scores = {}
    for cle_test in range(len(alphabet)):
        test_texte = caesar(message_propre, -cle_test, langue)
        diff = 0
        for i in range(len(alphabet)):
            lettre = alphabet[i]
            freq_texte = (test_texte.count(lettre) / l) * 100
            diff += abs(freq_texte - dict_freq_json[i])
        scores[cle_test] = round(diff, 2)
    return scores
"""

def decrypt_freq(message, langue):
    alphabet = LangDictJson[langue]['alphabet']
    dict_freq_json = LangDictJson[langue]['PP']
    message_propre = sanitize(message)
    l = float(len(message_propre))
    if l == 0: 
        return 0
    score = [0, 500]
    for cle_test in range(len(alphabet)):
        test = caesar(message_propre, -cle_test, langue)
        diff = sum(abs(b - dict_freq_json[a]) for a, b in enumerate([100 * test.count(lettre) / l for lettre in alphabet]))
        if diff < score[1]:
            score = [cle_test, diff]
    return f"Clé détectée par l'analyse de fréquence : {score[0]} ; Message décrypté :{caesar(phrase_codee, -score[0], lang)}"

    
    

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

if __name__ == "__main__":
    lang = "french"
    phrase_a_crypter = "Le but de ce projet est de programmer des algorithmes de chiffrements utilises avant l’utilisation d’algorithmes modernes, mais surtout de programmer des algorithmes capables de casser ces chiffrements anciens. Dans un premier temps, il faudra programmer en python le code de cesar, le chiffre de Vigenere ainsi que la scytale, et une substitution monoalphabetique generale. Toutes les descriptions peuvent etre trouves sur internet facilement." 
    phrase_codee = caesar(phrase_a_crypter, 10, lang)
    print("phrase codée :", phrase_codee)
    print(decrypt_freq(phrase_codee, lang))
    #print(analyse_de_frequence(phrase_a_crypter,lang))
    #print(genere_toutes_les_scores(phrase_codee,lang))
        
