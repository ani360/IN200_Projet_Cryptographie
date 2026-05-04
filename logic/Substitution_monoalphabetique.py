import json, unicodedata, random
from pathlib import Path
from random import shuffle


script_dir = Path(__file__).parent

LangDict_path = script_dir.parent / "LangDict.json"
with open(LangDict_path, 'r', encoding='utf-8') as f: #file path, read, utf-8
    LangDictJson = json.load(f)

def remake_lowcase(txt1 : str, txt2 :str) -> str : #note : does not work well with french_extended bcse of accents.
    txt1_2 = ''
    for char in txt1 :
        if char.isalnum() or char.isspace() :
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

def encode_monoalph(input : str, sub_alph : str , lang, keep_case=False, keep_accent=False):
    alphabet : str = LangDictJson[lang]['alphabet']
    plaintext = sanitize(input, alphabet, keep_accent)
    res = ''
    for caractere in plaintext :
        if caractere in alphabet:
            position = alphabet.index(caractere)
            res += sub_alph[position]
        else:
            res += caractere
    if keep_case :
        res = remake_lowcase(input, res)
    return res

def decode_monoalph(input : str, sub_alph : str , lang, keep_case=False, keep_accent=False):
    alphabet : str = LangDictJson[lang]['alphabet']
    plaintext = sanitize(input, alphabet, keep_accent)
    res = ''
    for caractere in plaintext :
        if caractere in alphabet:
            position = sub_alph.index(caractere)
            res += alphabet[position]
        else:
            res += caractere
    if keep_case :
        res = remake_lowcase(input, res)
    return res

def generer_alphabet(lang):
    substitution_alphabet = list(LangDictJson[lang]['alphabet'])
    shuffle(substitution_alphabet)
    return "".join(a for a in substitution_alphabet)

if __name__ == "__main__":
    lang = 'french_extended'
    substitution_alphabet = generer_alphabet(lang)
    print(substitution_alphabet)
    print(len(substitution_alphabet))
    #txt = "Le but de ce projet est de programmer des algorithmes de chiffrements utilises avant l’utilisation d’algorithmes modernes, mais surtout de programmer des algorithmes capables de casser ces chiffrements anciens. Dans un premier temps, il faudra programmer en python le code de cesar, le chiffre de Vigenere ainsi que la scytale, et une substitution monoalphabetique generale. Toutes les descriptions peuvent etre trouves sur internet facilement."
    txt = "Le Comte de Monte-Cristo est un roman d'Alexandre Dumas, écrit avec la collaboration d'Auguste Maquet et dont la publication commence pendant l'été 1844."
    encoded = encode_monoalph(txt, substitution_alphabet, lang, True, True)
    print(encoded)
    decoded = decode_monoalph(encoded, substitution_alphabet, lang, True, True)
    print(decoded)
    