import json, unicodedata, random
from pathlib import Path

script_dir = Path(__file__).parent

LangDict_path = script_dir / "LangDict.json"
with open(LangDict_path, 'r', encoding='utf-8') as f: #file path, read, utf-8
    LangDictJson = json.load(f)

def sanitize(input : str)->str : #virer les accents
    normalized = unicodedata.normalize('NFD', input) #remplace é par e'
    result = "".join(char for char in normalized if unicodedata.category(char) != 'Mn')
    final_list_char = []
    for char in result:
        if char.isalpha() or char.isspace():
            final_list_char.append(char.upper())
    return "".join(final_list_char)

def monoalph(input : str, Dsub : dict, lang):
    alphabet : str = LangDictJson[lang]['alphabet']
    input = sanitize(input)
    output : str = ''
    for el in input :
        if el.isalpha() and el in Dsub.keys():
            output += Dsub[el]
        else :
            output += el
    return(output)

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

if __name__ == "__main__":
    Dictsub = config_generator(12, 'french')
    print(Dictsub)
    print(len(Dictsub))
    txt = "Le but de ce projet est de programmer des algorithmes de chiffrements utilises avant l’utilisation d’algorithmes modernes, mais surtout de programmer des algorithmes capables de casser ces chiffrements anciens. Dans un premier temps, il faudra programmer en python le code de cesar, le chiffre de Vigenere ainsi que la scytale, et une substitution monoalphabetique generale. Toutes les descriptions peuvent etre trouves sur internet facilement."
    encoded = monoalph(txt, Dictsub, 'french')
    print(encoded)
    decoded = monoalph(encoded, Dictsub, 'french')
    print(decoded)