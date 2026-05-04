import json
import unicodedata
from pathlib import Path
#from caesar import caesar_decrypt_freq #serat dans le fichier du code de césar

# Get the script dir
script_dir = Path(__file__).parent
file_path = script_dir.parent / "LangDict.json"

#import json
with open(file_path, 'r', encoding='utf-8') as f: #file path, read, utf-8
    LangDictJson = json.load(f)

class caesar :
    def __init__ (self, input : str,):
        self.input = input
        if type(input) != str :
            ("Input must be a string")
    def encode(self, inc : int) -> str:
        output : str = ''
        for char in self.input :
            if char.isalpha() :
                base = 65 + (32 * char.islower()) #change l'ordonné de base en fonction de maj ou min
                output += chr((ord(char)-base+inc)%26+base)
            else :
                output += char
        return(output)
    
    def decode(self, inc : int) -> str:
        output : str = ''
        for char in self.input :
            if char.isalpha() :
                base = 65 + (32 * char.islower())
                output += chr((ord(char)-base-inc)%26+base)
            else :
                output += char
        return(output)

    def decrypt(self) -> str: #bruteforce
        output : dict = {}
        for i in range(26):
            charstring : str = ''
            for char in self.input :
                letter = chr(ord(char)-i)
                if letter.isalpha() :
                    charstring += letter
                elif char == ' ' :
                    charstring += char
                else :
                    break
            output[i] = charstring
        return(output)

    def decrypt_freq(self, lang : str) -> int: #trouve la clée corresspondante par analyse de fréquence.
        self.dict_freq : dict = {lang : LangDictJson[lang]['PP']}
        l = float(len(self.input))
        score : list = [0, 100]
        for i in range (26):
            diff = sum(abs(b - self.dict_freq[lang][a]) for a, b in enumerate([100 * lettre / l for lettre in map(self.input.upper().count, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")]))
            if diff < score[1]: 
                score = i, diff
            self.input : str = self.encode(1)
            #print(self.input, score)
        return score[0]

    def decode_freq(self, lang : str):
        return(self.decode(26-self.decrypt_freq(lang)))

def Calcul_IC(input : str, alphabet : str, pas : int) -> int : #calcul de l'indice de coincidence utile dans plusieurs autres fonctions
    somf : list = []
    somme = lambda nb : nb * (nb - 1)
    input = ''.join([c for c in input if c.isalpha()])
    for i in range(pas):
        lettres : list = [0]*int(len(alphabet))
        for n, lettre in enumerate(input[i::pas]) : #lettre est la lettre dans l'input et n est son occurence
            lettres[ord(lettre)-65] +=1 #ajoute l'occurence dans la liste lettre.
        somf.append(sum(map(somme, lettres))/float(n*(n+1))) #calcul de l'indice
    return(sum(somf)/float(len(somf))) #return moyenne des indices

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

def sanitize(input : str)->str : #virer les charspec
    normalized = unicodedata.normalize('NFD', input) #remplace é par e'
    result = "".join(char for char in normalized if unicodedata.category(char) != 'Mn')
    final_list_char = []
    for char in result:
        if char.isalnum() or char.isspace():
            final_list_char.append(char.upper())
    return "".join(final_list_char)

def generate_vigenere_encode_table(lang):
    alphabet = LangDictJson[lang]['alphabet']
    vigenere_map = {}
    n = len(alphabet)
    for i in range(n):
        key_char = alphabet[i]
        row_map = {}
        for j in range(n):
            current_char = alphabet[j]
            cipher_char = alphabet[(i + j) % n]
            row_map[current_char] = cipher_char
        vigenere_map[key_char] = row_map
    return vigenere_map

def generate_vigenere_decode_table(lang):
    alphabet = LangDictJson[lang]['alphabet']
    vigenere_map = {}
    n = len(alphabet)
    for i in range(n):
        key_char = alphabet[i]
        row_map = {}
        for j in range(n):
            current_char = alphabet[(j+i) % n]
            ciphered_char = alphabet[j]
            row_map[current_char] = ciphered_char
        vigenere_map[key_char] = row_map
    return(vigenere_map)

def vigenere_encode(input : str, key : str, lang : str, keep_lowercase : bool) -> str:
        #example : cipher_letter = vigenere_table[key_letter][plain_letter]
        vigenere_table = generate_vigenere_encode_table(lang)
        encoded : str = ""
        key : str = "".join(char for char in key.upper() if char.isalpha())
        i :int = 0
        if lang == "french_extended" :
            plaintext = "".join(char for char in input.upper() if char.isalnum() or char.isspace())
        else :
            plaintext = sanitize(input)
        for char in plaintext :
            if char.isalpha():
                encoded += vigenere_table[key[i%(len(key))]][char]
                i+=1
            else :
                encoded += char
        if keep_lowercase :
            encoded = remake_lowcase(input, encoded)
        return(encoded)

def vigenere_decode(input : str, key : str, lang : str, keep_lowercase : bool) -> str:
        #example : cipher_letter = vigenere_table[key_letter][plain_letter]
        vigenere_table = generate_vigenere_decode_table(lang)
        decoded : str = ""
        key : str = "".join(char for char in key.upper() if char.isalpha())
        i :int = 0
        if lang == "french_extended" :
            plaintext = "".join(char for char in input.upper() if char.isalnum() or char.isspace())
        else :
            plaintext = sanitize(input)
        for char in plaintext :
            if char.isalpha():
                decoded += vigenere_table[key[i%(len(key))]][char]
                i+=1
            else :
                decoded += char
        if keep_lowercase :
            decoded = remake_lowcase(input, decoded)
        return(decoded)

def vigenere_decrypt(input : int, lang : str, keep_lowercase : bool):
    if lang == "french_extended":
        alphabet : str = LangDictJson["french"]["alphabet"]
    else :
        alphabet : str = LangDictJson[lang]["alphabet"]
    IC : float = LangDictJson[lang]["IC"]
    L : int = len(alphabet)
    plaintext : str = sanitize(input)
    plaintext = ''.join(char for char in plaintext if char.isalpha())
    pas = 1
    while Calcul_IC(plaintext, alphabet, pas) < IC :
        pas+=1
    fractionne = [plaintext[start::pas] for start in range(pas)]
    indices_cles = [caesar(bout).decrypt_freq(lang) for bout in fractionne]
    #indices_cles = [caesar_decrypt_freq(bout, lang) for bout in fractionne] #syntaxe attendue pour le decryptage par analyse de freq du code de cesar.
    key = ''.join(([alphabet[(L - i) % L] for i in indices_cles]))
    
    decrypted = vigenere_decode(input, key, lang, False)
    if keep_lowercase :
        decrypted = remake_lowcase(input, decrypted)
    
    return key, decrypted

if __name__ == "__main__": #DECRYPTER WON'T WORK EVERY TIME ESPECIALLY WITH LONGER KEYS OR TEXTS WITH UNEVEN LETTER DISTRIBUTION.
    #raw_texts
    frtxt = "Le but de ce projet est de programmer des algorithmes de chiffrements utilises avant l’utilisation d’algorithmes modernes, mais surtout de programmer des algorithmes capables de casser ces chiffrements anciens. Dans un premier temps, il faudra programmer en python le code de cesar, le chiffre de Vigenere ainsi que la scytale, et une substitution monoalphabetique generale. Toutes les descriptions peuvent etre trouves sur internet facilement."
    entxt = "Letter frequency is the number of times letters of the alphabet appear on average in written language. Letter frequency analysis dates back to the Arab mathematician Al-Kindi"
    frext = "Le Comte de Monte-Cristo est un roman d'Alexandre Dumas, écrit avec la collaboration d'Auguste Maquet et dont la publication commence pendant l'été 1844. Il est partiellement inspiré du récit d'un fait divers, « Le Diamant et la Vengeance » (voir Pierre Picaud), publié en 1838 dans les Mémoires tirés des archives de la police (tome V, chapitre LXXIV), mémoires apocryphes rédigés en large partie par l'écrivain Étienne-Léon de Lamothe-Langon à partir des notes de Jacques Peuchet, archiviste de la préfecture de police."
    
    #Test for lang = "french"
    """
    FRencoded = vigenere_encode(frtxt, 'DEGAULLE', "french", True)
    print(FRencoded)
    print(vigenere_decode(FRencoded, 'DEGAULLE', "french", True))
    print(vigenere_decrypt(FRencoded, "french", True))
    """
    
    #test for lang = "english"
    """
    #print(generate_vigenere_encode_table("english"))
    ENencoded = vigenere_encode(entxt, 'KINDI', "english", True)
    print(ENencoded)
    print(vigenere_decode(ENencoded, 'KINDI', "english", True))
    print(vigenere_decrypt(ENencoded, "english", True))
    """

    
    #test for french extended :
    """
    test1 = vigenere_encode(frext, 'DEGAULLE', "french_extended", True)
    print(test1)
    print(vigenere_decode(test1, 'DEGAULLE', "french_extended", True))
    print(vigenere_decrypt(test1, "french_extended", True))
    """