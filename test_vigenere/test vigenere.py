#frequence des lettres
frequence_theorique = [
        7.636, 0.901, 3.260, 3.669, 14.715, 1.066, 0.866, 0.737, 7.529, 0.613,
        0.074, 5.456, 2.968, 7.095, 5.796, 2.521, 1.362, 6.693, 7.948, 7.244,
        6.311, 1.838, 0.049, 0.427, 0.128, 0.326
    ]
#fonction decaler = chiffre de cesar de clef d
decaler = lambda code, d : ''.join([chr((ord(lettre)- 65 + d) % 26 + 65)if lettre.isalpha() else lettre for lettre in code])


def calculer_IC (code, pas):
    """
        calcule l'indice de coincidence de 'code'
        en decoupant'code' en 'pas' sous-textes
    """
    somme = lambda nb : nb * (nb - 1)
    IC = []
    for i in range (pas):
        nb_lettre = [0] * 26
        for compteur, lettre in enumerate(code [i::pas]):
            nb_lettre [ord(lettre)- 65] += 1
        IC.append(sum(map(somme, nb_lettre)) / float(compteur * (compteur + 1)))
    return sum(IC) / float(len(IC))

def calculer_decalage (code):
    longueur = float(len(code))
    m = [0, 100]
    for i in range (26):
        diff = sum(abs(b - frequence_theorique[a]) for a, b in enumerate([100 * lettre / longueur for lettre in map(code.count, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")]))
        if diff < m[1]: m = i, diff
        code = decaler (code, 1)
    return m [0]


def calculer_decalage_v2(segment):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    n = len(segment)
    freq_theo = frequence_theorique # tes % théoriques
    
    meilleur_score = float('inf') # On cherche le score le plus BAS
    cle_detectee = 0
    
    for decalage in range(26):
        # 1. On crée le texte testé pour ce décalage
        test = decaler(segment, -decalage)
        
        score_chi2 = 0
        for i, lettre in enumerate(alphabet):
            # 2. Nombre d'apparitions observées
            observe = test.count(lettre)
            
            # 3. Nombre d'apparitions espérées (Fréquence % * Taille du texte / 100)
            espere = (freq_theo[i] * n) / 100.0
            
            # 4. Calcul du Khi-deux pour cette lettre
            if espere > 0:
                score_chi2 += ((observe - espere) ** 2) / espere
        
        # 5. On garde le décalage qui minimise le score
        if score_chi2 < meilleur_score:
            meilleur_score = score_chi2
            cle_detectee = decalage
            
    return cle_detectee

def calculer_decalage_propre(code):
    f_theo = frequence_theorique
    meilleur_score = [0, 1000]
    
    for i in range(26):        
        test = decaler(code, -i) 
        counts = [test.upper().count(l) for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        freq_obs = [100 * c / len(code) for c in counts]
        diff = sum(abs(o - t) for o, t in zip(freq_obs, f_theo)) # Somme des différences
        if diff < meilleur_score[1]:
            meilleur_score = [i, diff]
        
    return meilleur_score[0]

def recoller (liste):
    f = ''
    try :
        for i in range (len(liste[0])):
            for z in liste: f += z[i]
    except : pass
    return f

def decrypter (code, plancher = 0.065):
    code = code.upper()
    pas = 1
    while calculer_IC(code, pas) < plancher :
        pas += 1
    code_fractionne = [code[dep::pas] for dep in range(pas)]
    print(code_fractionne)
    print([calculer_decalage_v2(bout) for bout in code_fractionne])
    print(['ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i] for i in [calculer_decalage_propre(bout) for bout in code_fractionne]])
    code_fractionne_decode = [decaler(bout, calculer_decalage_propre(bout)) for bout in code_fractionne]
    return recoller (code_fractionne_decode)
txt = "Le but de ce projet est de programmer des algorithmes de chiffrements utilisés avant l’utilisation d’algorithmes modernes, mais surtout de programmer des algorithmes capables de casser ces chiffrements anciens. Dans un premier temps, il faudra programmer en python le code de césar, le chiffre de Vigenère ainsi que la scytale, et une substitution monoalphabétique générale. Toutes les descriptions peuvent être trouvés sur internet facilement."
#txt = 'IX C LDEIF IY EISFTSIPIQ, HLVW LQ GSIXEMY OM QOZWTMYR XI MIVOZ HP BLUZHPZ-XEZ-XCWRCWL, FV NEGRP OEROSY I UUU PL VETGVP IZAUX OWRNQ PPA QOQYCA PEE TWCW DAYNMW'
txt = ''.join([lettre for lettre in txt if lettre.isalpha()])
print(decrypter(txt, 0.065))