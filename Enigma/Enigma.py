import json
import os
import random
import unicodedata
from pathlib import Path
#from caesar import caesar_decrypt_freq #serat dans le fichier du code de césar

# Get the script dir
script_dir = Path(__file__).parent


LangDict_path = script_dir / "LangDict.json"
with open(LangDict_path, 'r', encoding='utf-8') as f: #file path, read, utf-8
    LangDictJson = json.load(f)

EniConfig_path = script_dir / "config" / "enigma_config.json"
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

def save_config(data, filenameend="", overwrite=True):
    folder = os.path.join("enigma", "config")
    filename="enigma_config"

    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    if overwrite:
        target_filename = f"{filename}.json"
    else:
        target_filename = f"{filename}_{filenameend}.json"
        if os.path.exists(os.path.join(folder, target_filename)):
            yn : bool = int(input('Le fichier existe déjà voulez vous le remplacer (0 : oui ; 1 : non)'))
            if yn == 1 :
                return('Could not resolve config saving.')
    filepath = os.path.join(folder, target_filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Config saved to: {filepath}")
    return filepath

class rotor:
    def __init__(self,forward_map, lang):
        self.alphabet : str = LangDictJson[lang]['alphabet']
        self.input : str = input
        self.pos : int = 0
        self.L : int = len(self.alphabet)
        self.forward_map : str = forward_map
        rev_list = [None] * self.L
        for i, char in enumerate(self.forward_map):
            target_index = self.alphabet.index(char)
            rev_list[target_index] = self.alphabet[i]
        self.reverse_map: str = "".join(rev_list)

    def step(self):
        # This actuates the state automatically
        self.pos = (self.pos + 1) % self.L
        return self.pos == 0
    
    def shift(self, char: str, reverse: bool):
        # 1. Entry Index + Position
        idx = (self.alphabet.index(char) + self.pos) % self.L

        # 2. Substitution (Scramble)
        if not reverse:
            char_out = self.forward_map[idx]
        else:
            char_out = self.reverse_map[idx]
        
        # 3. FIX: Convert result back to index to perform subtraction
        new_idx = self.alphabet.index(char_out)
        return self.alphabet[(new_idx - self.pos) % self.L]

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

class EnigmaMachine:
    def __init__(self, lang):
        self.alphabet : str = LangDictJson[lang]['alphabet']
        self.plugboard : list[list[str]] = Plugboard(EnigmaConfigDict['cables'], lang)
        self.rotors = [rotor(r['wiring'], lang) for r in EnigmaConfigDict['rotors']]
        self.reflector = Reflector(EnigmaConfigDict['reflector'], lang)

    def process_text(self, text : str): #fonctionne dans les deux sens moyennant même config de départ.
        result : str = ""
        for char in text.upper():
            if char not in self.alphabet:
                result += char
                continue
            
            # --- STEP 1: ACTUATION (The Odometer) ---
            # Every keypress moves the first rotor.
            if self.rotors[0].step():
                if self.rotors[1].step():
                    self.rotors[2].step()

            # --- STEP 2: FORWARD PASS ---
            # Signal enters via Plugboard
            current_char = self.plugboard.swap(char)
            
            # Signal goes through rotors (R1 -> R2 -> R3)
            for r in self.rotors:
                current_char = r.shift(current_char, reverse=False)

            # --- STEP 3: REFLECTION ---
            # Signal hits the "Mirror"
            current_char = self.reflector.reflect(current_char)

            # --- STEP 4: BACKWARD PASS ---
            # Signal goes back through rotors (R3 -> R2 -> R1)
            for r in reversed(self.rotors):
                current_char = r.shift(current_char, reverse=True)

            # --- STEP 5: FINAL PLUGBOARD ---
            # Signal exits via Plugboard to the Lampboard
            current_char = self.plugboard.swap(current_char)
            
            result += current_char
            
        return result


def setup_generator(nrotor : int, ncables : int, lang, overwrite : bool) : #n = rotor number
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
    
    if not overwrite :
        ending = input('name your folder : ')

    save_config(data, ending, overwrite)
    pass


print(setup_generator(6, 8, 'french', False))

txt = "Le but de ce projet est de programmer des algorithmes de chiffrements utilises avant l’utilisation d’algorithmes modernes, mais surtout de programmer des algorithmes capables de casser ces chiffrements anciens. Dans un premier temps, il faudra programmer en python le code de cesar, le chiffre de Vigenere ainsi que la scytale, et une substitution monoalphabetique generale. Toutes les descriptions peuvent etre trouves sur internet facilement."
txt = sanitize(txt)
encoded = EnigmaMachine('french').process_text(txt)
print(encoded)
decoded = EnigmaMachine('french').process_text(encoded)
print(decoded)