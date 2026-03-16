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

class caesar :
    def __init__ (self, input : str,):
        self.input = input
        if type(input) != str :
            ("Input must be a string")
        self.dict_freq : dict = {
    "french": [
        7.636, 0.901, 3.260, 3.669, 14.715, 1.066, 0.866, 0.737, 7.529, 0.613,
        0.074, 5.456, 2.968, 7.095, 5.796, 2.521, 1.362, 6.693, 7.948, 7.244,
        6.311, 1.838, 0.049, 0.427, 0.128, 0.326
    ],
    "english": [
        8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153,
        0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056,
        2.758, 0.978, 2.360, 0.150, 1.974, 0.074
    ],
    "spanish": [
        11.525, 2.215, 4.019, 5.010, 12.181, 0.692, 1.768, 0.703, 6.247, 0.443,
        0.011, 4.967, 3.157, 6.712, 8.683, 2.510, 0.877, 6.871, 7.977, 4.632,
        2.927, 1.138, 0.017, 0.215, 1.008, 0.467
    ],
    "italian": [
        11.745, 0.927, 4.501, 3.736, 11.792, 1.113, 0.473, 0.640, 10.143, 0.011,
        0.009, 6.510, 2.512, 6.883, 9.832, 3.056, 0.505, 6.367, 4.981, 5.623,
        3.011, 2.097, 0.033, 0.003, 0.020, 1.181
    ],
    "german": [
        6.516, 1.886, 2.732, 5.076, 16.396, 1.656, 3.009, 4.577, 7.550, 0.268,
        1.417, 3.437, 2.534, 9.776, 2.594, 0.670, 0.018, 7.003, 7.270, 6.154,
        4.166, 0.846, 1.921, 0.034, 0.039, 1.134
    ],
    "neerlandais": [
        7.486, 1.584, 1.242, 5.933, 18.91, 0.805, 3.403, 2.380, 11.99, 1.46,
        2.248, 3.568, 2.213, 10.03, 6.063, 1.57, 0.009, 6.411, 3.73, 6.79,
        1.99, 2.85, 1.52, 0.036, 0.035, 1.39
    ],
    "suedois": [
        9.383, 1.535, 1.486, 4.702, 10.149, 2.027, 2.862, 2.090, 5.817, 0.614,
        3.140, 5.275, 3.471, 8.542, 4.484, 1.839, 0.020, 8.431, 6.590, 7.691,
        1.919, 2.415, 0.142, 0.159, 0.708, 0.070
    ],
    "russian": [ # Alphabet cyrillique (33 lettres)
        8.01, 1.59, 4.54, 1.70, 2.98, 8.45, 0.04, 0.94, 1.65, 7.35, 1.21, 3.49, 
        4.40, 3.21, 6.70, 10.97, 2.81, 4.73, 5.47, 6.26, 2.62, 0.26, 0.97, 0.48, 
        1.44, 0.73, 0.36, 0.04, 1.90, 1.74, 0.03, 1.10, 2.01
    ]
}
        #hardcode le dico des freq des langue pr l'instant mais go le mettre dans un json avec les autres dico après.

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

def sanitize(input : str)->str : #virer les accents
    normalized = unicodedata.normalize('NFD', input) #remplace é par e'
    result = "".join(char for char in normalized if unicodedata.category(char) != 'Mn')
    final_list_char = []
    for char in result:
        if char.isalpha() or char.isspace():
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

def vigenere_encode(input : str, key : str, lang : str) -> str:
        #example : cipher_letter = vigenere_table[key_letter][plain_letter]
        vigenere_table = generate_vigenere_encode_table(lang)
        encoded : str = ""
        key : str = "".join(char for char in key.upper() if char.isalpha())
        i :int = 0
        plaintext = sanitize(input)
        for char in plaintext :
            if char.isalpha():
                encoded += vigenere_table[key[i%(len(key))]][char]
                i+=1
            else :
                encoded += char
        return(encoded)

def vigenere_decode(input : str, key : str, lang : str) -> str:
        #example : cipher_letter = vigenere_table[key_letter][plain_letter]
        vigenere_table = generate_vigenere_decode_table(lang)
        decoded : str = ""
        key : str = "".join(char for char in key.upper() if char.isalpha())
        i :int = 0
        plaintext = sanitize(input)
        for char in plaintext :
            if char.isalpha():
                decoded += vigenere_table[key[i%(len(key))]][char]
                i+=1
            else :
                decoded += char
        return(decoded)

def vigenere_decrypt(input : int, lang : str) -> str:
    alphabet : str = LangDictJson[lang]["alphabet"]
    L : int = len(alphabet)
    plaintext : str = ''.join(char for char in input.upper() if char.isalpha())
    pas = 1
    while Calcul_IC(plaintext, alphabet, pas) < 0.065 :
        pas+=1
    fractionne = [plaintext[start::pas] for start in range(pas)]
    indices_cles = [caesar(bout).decrypt_freq(lang) for bout in fractionne]
    #indices_cles = [caesar_decrypt_freq(bout, lang) for bout in fractionne] #syntaxe attendue pour le decryptage par analyse de freq du code de cesar.
    key = ''.join(([alphabet[(L - i) % L] for i in indices_cles]))

    return(f'key = {key}, text = {vigenere_decode(input, key, lang)}')

txt = "Le but de ce projet est de programmer des algorithmes de chiffrements utilises avant l’utilisation d’algorithmes modernes, mais surtout de programmer des algorithmes capables de casser ces chiffrements anciens. Dans un premier temps, il faudra programmer en python le code de cesar, le chiffre de Vigenere ainsi que la scytale, et une substitution monoalphabetique generale. Toutes les descriptions peuvent etre trouves sur internet facilement."
#print(generate_vigenere_encode_table('english'))
encoded = vigenere_encode(txt, 'DEGAULLE', "french")
print(vigenere_decrypt(encoded, 'french'))