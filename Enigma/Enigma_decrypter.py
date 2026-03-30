import random
import time
from Enigma import EnigmaMachine, LangDictJson, sanitize

def generate_candidate_config(seed_val, n_rotors, n_cables, lang):
    random.seed(seed_val)
    alphabet = LangDictJson[lang]['alphabet']
    alphalist = list(alphabet)
    
    config = {"rotors": [], "reflector": "", "cables": []}
    
    # rotor
    for i in range(n_rotors):
        shuffled = alphalist[:]
        random.shuffle(shuffled)
        config["rotors"].append({"id": i + 1, "wiring": "".join(shuffled)})
    
    # reflector
    reflector_map = [None] * len(alphalist)
    available_indices = list(range(len(alphalist)))
    random.shuffle(available_indices)
    while available_indices:
        idx_a = available_indices.pop()
        idx_b = available_indices.pop()
        reflector_map[idx_a] = alphalist[idx_b]
        reflector_map[idx_b] = alphalist[idx_a]
    config["reflector"] = "".join(reflector_map)

    # cables
    available_chars = alphalist[:]
    random.shuffle(available_chars)
    for _ in range(n_cables):
        char_a = available_chars.pop()
        char_b = available_chars.pop()
        config["cables"].append([char_a, char_b])
        
    return config

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

def get_text_score(text, lang): #score
    if not text: return 0
    
    #tetragram score
    tetra_score = 0
    tetragrams = LangDictJson[lang]['tetragrams']
    text_upper = text.upper()
    for tetra in tetragrams:
        tetra_score += text_upper.count(tetra)

    #bonus for IC score
    try:
        current_ic = Calcul_IC(text, LangDictJson[lang]['alphabet'], 1)
        target_ic = LangDictJson[lang]['IC']
        if abs(current_ic - target_ic) < 0.01:
            tetra_score += len(text)//33
    except:
        pass
        
    return tetra_score

def crack_enigma(ciphertext, lang, target_timestamp, window_seconds=10, max_rotors=6, max_ncables=10):
    print(f"[*] starting attack on  (Timestamp: +/- {window_seconds}s)...")
    
    L_candidat = []

    # rotors
    for n_rotors in range(1, max_rotors + 1):
        print(f"[*] Test for {n_rotors} rotors...")
        
        # cables
        for n_cables in range(max_ncables + 1):
            
            # timestamp
            for current_seed in range(target_timestamp - window_seconds, target_timestamp + window_seconds):
                
                # test
                candidate_config = generate_candidate_config(current_seed, n_rotors, n_cables, lang)
                machine = EnigmaMachine(lang, custom_config=candidate_config)
                trial_decrypt = machine.process_text(ciphertext)

                score = get_text_score(trial_decrypt, lang)
                
                if score >= 1: 
                    print(f"[Candidat] Seed: {current_seed} | Score: {score} | Text: {trial_decrypt[:40]}...")
                    L_candidat.append([current_seed, score, trial_decrypt])
    
    best = 0
    for el in L_candidat :
        if el[1] > best :
            best = el[1]
            best_candidat = el
    try :
        return f"[Candidat] Seed: {best_candidat[0]} | Score: {best_candidat[1]} | Text: {best_candidat[2]}..."
    except :
        return "[-] Attack failure."


# --- TEST --- #on notera que ce programme NE RETOURNE PAS TOUJOURS LA BONNE SOLUTION mais cette dèrnière apparaît très souvent dans les candidats le calcul du score ne pouvant etre meilleure (surtout pour les messages les plus cours)
if __name__ == "__main__":
    # simulation
    instant_creation = int(time.time()) 
    langue = 'french'
    rotors_reels = 6
    cables_reels = 8
    
    # 1. Chiffrement
    config_reelle = generate_candidate_config(instant_creation, rotors_reels, cables_reels, langue)
    machine = EnigmaMachine(langue, custom_config=config_reelle)
    
    msg = "Le but de ce projet est de programmer des algorithmes capables de casser ces chiffrements anciens."
    msg = sanitize(msg)
    cipher = machine.process_text(msg)
    print(f"Ciphertext: {cipher}\n")

    # 2. Crack
    resultat = crack_enigma(cipher, langue, instant_creation, window_seconds=5, max_rotors=6, max_ncables=10)
    
    if resultat:
        print(f"\nDecrypted : {resultat}")
