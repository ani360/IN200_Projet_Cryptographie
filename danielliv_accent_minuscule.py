import unicodedata
import json
from pathlib import Path

script_dir = Path(__file__).parent
LangDict_path = script_dir.parent / "LangDict.json"

with open(LangDict_path, 'r', encoding='utf-8') as f: 
    LangDictJson = json.load(f)

def remake_lowcase(txt1 : str, txt2 :str) -> str : #note : does not work well with french_extended bcse of accents.
    txt1_2 = ''
    for char in txt1 :
        if char.isalpha() or char.isspace() :
            txt1_2 +=char
    L=[]
    for i in range(len(txt1_2)) :
        if txt1_2[i].isalpha() and txt1_2[i].islower():
            L.append(txt2[i].lower())
        else : 
            L.append(txt2[i])
    return("".join(L))

def sanitize(input_str, alphabet_visee, garder_accents=False):
    if garder_accents:
        result=input_str
    else:
        normalized = unicodedata.normalize('NFD', input_str)
        result = "".join(char for char in normalized if unicodedata.category(char) != 'Mn')
    final_list_char = []
    resultat_temporaire=result.upper()
    for char in resultat_temporaire:
        if char in alphabet_visee or char.isspace():
            final_list_char.append(char)
    return "".join(final_list_char)


def caesar(message, cle, alphabet,garder_minuscules=False, garder_accents=False):
    message_original=message
    message_de_travail=sanitize(message,alphabet,garder_accents)
    message_chiffre = ""
    taille = len(alphabet)
    for letter in message_de_travail:
        if letter in alphabet:
            index = alphabet.find(letter)
            nouvel_index = (index + cle) % taille
            message_chiffre += alphabet[nouvel_index]
        else:
            message_chiffre += letter
    if garder_minuscules:
        return remake_lowcase(message_original, message_chiffre)
    return message_chiffre

def brute_force(message, alphabet,garder_minuscules=False,garder_accents=False):
    tentatives = {}
    for k in range(len(alphabet)):
        tentatives[k] = caesar(message, -k, alphabet,garder_minuscules,garder_accents)
    return tentatives

"""""def analyse_de_frequence(message, langue,garder_accents):
    message_propre=sanitize(message) 
    dict_freq = LangDictJson[langue]['PP']
    alphabet = LangDictJson[langue]['alphabet']
    taille=len(message_propre)
    frequences_apparition_lettres={}
    for lettre in alphabet:
        nombre_apparition=message_propre.count(lettre)
        frequences_apparition_lettres[lettre]=(nombre_apparition/taille)*100
    return frequences_apparition_lettres """

"""def genere_toutes_les_scores(message, langue):
    alphabet = LangDictJson[langue]['alphabet']
    dict_freq_json = LangDictJson[langue]['PP']
    message_propre = sanitize(message)
    l = len(message_propre)
    if l == 0: 
        return {}
    scores = {}
    for cle_test in range(len(alphabet)):
        test_texte = caesar(message_propre, -cle_test, alphabet)
        diff = 0
        for i in range(len(alphabet)):
            lettre = alphabet[i]
            freq_texte = (test_texte.count(lettre) / l) * 100
            diff += abs(freq_texte - dict_freq_json[i])
        scores[cle_test] = round(diff, 2)
    return scores
"""
def decrypt_freq(message, langue,garder_accents=False):
    alphabet = LangDictJson[langue]['alphabet']
    dict_freq_json = LangDictJson[langue]['PP']
    message_propre = sanitize(message,alphabet,garder_accents)
    l = float(len(message_propre))
    if l == 0: 
        return 0
    score = [0, 500]
    for cle_test in range(len(alphabet)):
        test = caesar(message_propre, -cle_test, alphabet, False, garder_accents)
        diff = sum(abs(b - dict_freq_json[a]) for a, b in enumerate([100 * test.count(lettre) / l for lettre in alphabet]))
        if diff < score[1]:
            score = [cle_test, diff]
    return score[0]



if __name__ == "__main__":
    message_test = "C'est l'été !"
    alphabet_ext = LangDictJson["french_extended"]["alphabet"]

    print("on garde tout")
    res1 = caesar(message_test, 3, alphabet_ext, garder_minuscules=True, garder_accents=True)
    print("Resultat:", res1)

    print("majuscule+accents")
    res2 = caesar(message_test, 3, alphabet_ext, garder_minuscules=False, garder_accents=True)
    print("Resultat:", res2)

    print("sans accents et majuscules")
    res3 = caesar(message_test, 3, alphabet_ext, garder_minuscules=False, garder_accents=False)
    print("Resultat:", res3)
   
    