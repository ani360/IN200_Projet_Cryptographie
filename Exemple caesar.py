import json
import unicodedata
from pathlib import Path
#from caesar import caesar_decrypt_freq #serat dans le fichier du code de césar

# Get the script dir
script_dir = Path(__file__).parent
file_path = script_dir / "LangDict.json"

#import json
with open(file_path, 'r', encoding='utf-8') as f: #file path, read, utf-8
    LangDictJson = json.load(f)


def sanitize(input : str)->str : #virer les accents
    normalized = unicodedata.normalize('NFD', input) #remplace é par e'
    result = "".join(char for char in normalized if unicodedata.category(char) != 'Mn')
    final_list_char = []
    for char in result:
        if char.isalpha() or char.isspace():
            final_list_char.append(char.upper())
    return "".join(final_list_char)

def caesar(input : str, key : int, lang : str) -> str :
    output : str = ''
    input = sanitize(input)
    alphabet = LangDictJson[lang]['alphabet']
    L = len(alphabet)
    for el in input :
        if el in alphabet :
            output += alphabet[((alphabet.index(el))+key)%L]
        else :
            output+=el
    return(output)
print(caesar(txt, 5, 'french'))