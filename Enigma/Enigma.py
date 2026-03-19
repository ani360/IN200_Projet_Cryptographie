import json
import os
import random
import unicodedata
from pathlib import Path
#from caesar import caesar_decrypt_freq #serat dans le fichier du code de césar

# Get the script dir
script_dir = Path(__file__).parent
LangDict_path = script_dir / "LangDict.json"
EniConfig_path = script_dir / "enigma_config.json"
#import json
with open(LangDict_path, 'r', encoding='utf-8') as f: #file path, read, utf-8
    LangDictJson = json.load(f)

with open(EniConfig_path, 'r', encoding='utf-8') as f:
    EnigmaConfigDict = json.load(f)

def sanitize(input : str)->str : #virer les accents
    normalized = unicodedata.normalize('NFD', input) #remplace é par e'
    result = "".join(char for char in normalized if unicodedata.category(char) != 'Mn')
    final_list_char = []
    for char in result:
        if char.isalpha() or char.isspace():
            final_list_char.append(char.upper())
    return "".join(final_list_char)

def save_config(data, path, filename="enigma_config.json"):
    filepath = os.path.join(path, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Configuration successfully saved to {filename}")

class rotor:
    def __init__(self,input, lang, number):
        self.alphabet : str = LangDictJson[lang]['alphabet']
        self.input : str = input
        self.forward_map : str = EnigmaConfigDict['rotors'][f"Custom Rotor {number}"]
        self.reverse_map : str = ''
        self.pos : int = 0
        self.L : int = len(self.alphabet)
        self.turn : int = self.pos%(len(self.alphabet)-1)
    
    def step(self):
        # This actuates the state automatically
        self.pos = (self.pos + 1) % self.L
        return self.pos == 0
    
    def shift(self, char : str, reverse : bool):
        #index + offset
        idx = (self.alphabet.index(char) + self.pos)%self.L

        #scramble
        if not reverse :
            idx = self.forward_map[idx]
        else :
            idx = self.reverse_map[idx]
        
        #index - offset
        return(self.alphabet[(idx - self.pos)%self.L])

class Reflector:
    def __init__(self, wiring_str, lang):
        self.alphabet : str = LangDictJson[lang]['alphabet']
        # Map: Index -> Target Index
        self.map = [self.alphabet.index(char) for char in wiring_str]

    def reflect(self, char):
        idx = self.alphabet.index(char)
        return self.alphabet[self.map[idx]]

class Plugboard:
    def __init__(self, cables, lang):
        self.alphabet : str = LangDictJson[lang]['alphabet']
        # Create a default map where A=A, B=B...
        self.mapping = {c: c for c in self.alphabet}
        # Apply the swaps from the JSON
        for char_a, char_b in cables:
            self.mapping[char_a] = char_b
            self.mapping[char_b] = char_a

    def swap(self, char):
        return self.mapping.get(char, char)

def setup_generator(nrotor : int, ncables : int, lang) : #n = rotor number
    alphabet : str = LangDictJson[lang]['alphabet']
    ncables = min(ncables, len(alphabet)//2)
    data = {
        "rotors": [],
        "reflector": "",
        "cables": []
    }
    alphalist = list(alphabet)
    for i in range(nrotor) :
        shuffled = alphalist[:]
        random.shuffle(shuffled)
        data["rotors"].append({
            "id": i + 1,
            "name": f"Custom Rotor {i + 1}",
            "wiring": "".join(shuffled)
        })
    
    # A reflector MUST swap letters in pairs. A cannot map to A.
    reflector_map = [None] * len(alphalist)
    available_indices = list(range(len(alphalist)))
    random.shuffle(available_indices)

    while available_indices :
        idx_a = available_indices.pop()
        idx_b = available_indices.pop()
        reflector_map[idx_a] = alphalist[idx_b]
        reflector_map[idx_b] = alphalist[idx_a]
    
    data["reflector"] = "".join(reflector_map)

    available_chars = alphalist[:]
    random.shuffle(available_chars)
    
    for _ in range(ncables):
        char_a = available_chars.pop()
        char_b = available_chars.pop()
        data["cables"].append([char_a, char_b])
        
    save_config(data, "Enigma")
    pass

print(setup_generator(3, 4, 'french'))