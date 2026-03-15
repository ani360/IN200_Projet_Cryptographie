#classes (objet final) :
class caesar :
    def __init__ (self, input : str,):
        self.input = input
        if type(input) != str :
            ("Input must be a string")
        self.dict_freq : dict = {
    "francais": [
        7.636, 0.901, 3.260, 3.669, 14.715, 1.066, 0.866, 0.737, 7.529, 0.613,
        0.074, 5.456, 2.968, 7.095, 5.796, 2.521, 1.362, 6.693, 7.948, 7.244,
        6.311, 1.838, 0.049, 0.427, 0.128, 0.326
    ],
    "anglais": [
        8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153,
        0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056,
        2.758, 0.978, 2.360, 0.150, 1.974, 0.074
    ],
    "espagnol": [
        11.525, 2.215, 4.019, 5.010, 12.181, 0.692, 1.768, 0.703, 6.247, 0.443,
        0.011, 4.967, 3.157, 6.712, 8.683, 2.510, 0.877, 6.871, 7.977, 4.632,
        2.927, 1.138, 0.017, 0.215, 1.008, 0.467
    ],
    "italien": [
        11.745, 0.927, 4.501, 3.736, 11.792, 1.113, 0.473, 0.640, 10.143, 0.011,
        0.009, 6.510, 2.512, 6.883, 9.832, 3.056, 0.505, 6.367, 4.981, 5.623,
        3.011, 2.097, 0.033, 0.003, 0.020, 1.181
    ],
    "allemand": [
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
    "russe": [ # Alphabet cyrillique (33 lettres)
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

class vigenere :
    def __init__(self, input : str) :
        self.vigenere_table : dict = {
        'A': {'A':'A','B':'B','C':'C','D':'D','E':'E','F':'F','G':'G','H':'H','I':'I','J':'J','K':'K','L':'L','M':'M','N':'N','O':'O','P':'P','Q':'Q','R':'R','S':'S','T':'T','U':'U','V':'V','W':'W','X':'X','Y':'Y','Z':'Z'},
        'B': {'A':'B','B':'C','C':'D','D':'E','E':'F','F':'G','G':'H','H':'I','I':'J','J':'K','K':'L','L':'M','M':'N','N':'O','O':'P','P':'Q','Q':'R','R':'S','S':'T','T':'U','U':'V','V':'W','W':'X','X':'Y','Y':'Z','Z':'A'},
        'C': {'A':'C','B':'D','C':'E','D':'F','E':'G','F':'H','G':'I','H':'J','I':'K','J':'L','K':'M','L':'N','M':'O','N':'P','O':'Q','P':'R','Q':'S','R':'T','S':'U','T':'V','U':'W','V':'X','W':'Y','X':'Z','Y':'A','Z':'B'},
        'D': {'A':'D','B':'E','C':'F','D':'G','E':'H','F':'I','G':'J','H':'K','I':'L','J':'M','K':'N','L':'O','M':'P','N':'Q','O':'R','P':'S','Q':'T','R':'U','S':'V','T':'W','U':'X','V':'Y','W':'Z','X':'A','Y':'B','Z':'C'},
        'E': {'A':'E','B':'F','C':'G','D':'H','E':'I','F':'J','G':'K','H':'L','I':'M','J':'N','K':'O','L':'P','M':'Q','N':'R','O':'S','P':'T','Q':'U','R':'V','S':'W','T':'X','U':'Y','V':'Z','W':'A','X':'B','Y':'C','Z':'D'},
        'F': {'A':'F','B':'G','C':'H','D':'I','E':'J','F':'K','G':'L','H':'M','I':'N','J':'O','K':'P','L':'Q','M':'R','N':'S','O':'T','P':'U','Q':'V','R':'W','S':'X','T':'Y','U':'Z','V':'A','W':'B','X':'C','Y':'D','Z':'E'},
        'G': {'A':'G','B':'H','C':'I','D':'J','E':'K','F':'L','G':'M','H':'N','I':'O','J':'P','K':'Q','L':'R','M':'S','N':'T','O':'U','P':'V','Q':'W','R':'X','S':'Y','T':'Z','U':'A','V':'B','W':'C','X':'D','Y':'E','Z':'F'},
        'H': {'A':'H','B':'I','C':'J','D':'K','E':'L','F':'M','G':'N','H':'O','I':'P','J':'Q','K':'R','L':'S','M':'T','N':'U','O':'V','P':'W','Q':'X','R':'Y','S':'Z','T':'A','U':'B','V':'C','W':'D','X':'E','Y':'F','Z':'G'},
        'I': {'A':'I','B':'J','C':'K','D':'L','E':'M','F':'N','G':'O','H':'P','I':'Q','J':'R','K':'S','L':'T','M':'U','N':'V','O':'W','P':'X','Q':'Y','R':'Z','S':'A','T':'B','U':'C','V':'D','W':'E','X':'F','Y':'G','Z':'H'},
        'J': {'A':'J','B':'K','C':'L','D':'M','E':'N','F':'O','G':'P','H':'Q','I':'R','J':'S','K':'T','L':'U','M':'V','N':'W','O':'X','P':'Y','Q':'Z','R':'A','S':'B','T':'C','U':'D','V':'E','W':'F','X':'G','Y':'H','Z':'I'},
        'K': {'A':'K','B':'L','C':'M','D':'N','E':'O','F':'P','G':'Q','H':'R','I':'S','J':'T','K':'U','L':'V','M':'W','N':'X','O':'Y','P':'Z','Q':'A','R':'B','S':'C','T':'D','U':'E','V':'F','W':'G','X':'H','Y':'I','Z':'J'},
        'L': {'A':'L','B':'M','C':'N','D':'O','E':'P','F':'Q','G':'R','H':'S','I':'T','J':'U','K':'V','L':'W','M':'X','N':'Y','O':'Z','P':'A','Q':'B','R':'C','S':'D','T':'E','U':'F','V':'G','W':'H','X':'I','Y':'J','Z':'K'},
        'M': {'A':'M','B':'N','C':'O','D':'P','E':'Q','F':'R','G':'S','H':'T','I':'U','J':'V','K':'W','L':'X','M':'Y','N':'Z','O':'A','P':'B','Q':'C','R':'D','S':'E','T':'F','U':'G','V':'H','W':'I','X':'J','Y':'K','Z':'L'},
        'N': {'A':'N','B':'O','C':'P','D':'Q','E':'R','F':'S','G':'T','H':'U','I':'V','J':'W','K':'X','L':'Y','M':'Z','N':'A','O':'B','P':'C','Q':'D','R':'E','S':'F','T':'G','U':'H','V':'I','W':'J','X':'K','Y':'L','Z':'M'},
        'O': {'A':'O','B':'P','C':'Q','D':'R','E':'S','F':'T','G':'U','H':'V','I':'W','J':'X','K':'Y','L':'Z','M':'A','N':'B','O':'C','P':'D','Q':'E','R':'F','S':'G','T':'H','U':'I','V':'J','W':'K','X':'L','Y':'M','Z':'N'},
        'P': {'A':'P','B':'Q','C':'R','D':'S','E':'T','F':'U','G':'V','H':'W','I':'X','J':'Y','K':'Z','L':'A','M':'B','N':'C','O':'D','P':'E','Q':'F','R':'G','S':'H','T':'I','U':'J','V':'K','W':'L','X':'M','Y':'N','Z':'O'},
        'Q': {'A':'Q','B':'R','C':'S','D':'T','E':'U','F':'V','G':'W','H':'X','I':'Y','J':'Z','K':'A','L':'B','M':'C','N':'D','O':'E','P':'F','Q':'G','R':'H','S':'I','T':'J','U':'K','V':'L','W':'M','X':'N','Y':'O','Z':'P'},
        'R': {'A':'R','B':'S','C':'T','D':'U','E':'V','F':'W','G':'X','H':'Y','I':'Z','J':'A','K':'B','L':'C','M':'D','N':'E','O':'F','P':'G','Q':'H','R':'I','S':'J','T':'K','U':'L','V':'M','W':'N','X':'O','Y':'P','Z':'Q'},
        'S': {'A':'S','B':'T','C':'U','D':'V','E':'W','F':'X','G':'Y','H':'Z','I':'A','J':'B','K':'C','L':'D','M':'E','N':'F','O':'G','P':'H','Q':'I','R':'J','S':'K','T':'L','U':'M','V':'N','W':'O','X':'P','Y':'Q','Z':'R'},
        'T': {'A':'T','B':'U','C':'V','D':'W','E':'X','F':'Y','G':'Z','H':'A','I':'B','J':'C','K':'D','L':'E','M':'F','N':'G','O':'H','P':'I','Q':'J','R':'K','S':'L','T':'M','U':'N','V':'O','W':'P','X':'Q','Y':'R','Z':'S'},
        'U': {'A':'U','B':'V','C':'W','D':'X','E':'Y','F':'Z','G':'A','H':'B','I':'C','J':'D','K':'E','L':'F','M':'G','N':'H','O':'I','P':'J','Q':'K','R':'L','S':'M','T':'N','U':'O','V':'P','W':'Q','X':'R','Y':'S','Z':'T'},
        'V': {'A':'V','B':'W','C':'X','D':'Y','E':'Z','F':'A','G':'B','H':'C','I':'D','J':'E','K':'F','L':'G','M':'H','N':'I','O':'J','P':'K','Q':'L','R':'M','S':'N','T':'O','U':'P','V':'Q','W':'R','X':'S','Y':'T','Z':'U'},
        'W': {'A':'W','B':'X','C':'Y','D':'Z','E':'A','F':'B','G':'C','H':'D','I':'E','J':'F','K':'G','L':'H','M':'I','N':'J','O':'K','P':'L','Q':'M','R':'N','S':'O','T':'P','U':'Q','V':'R','W':'S','X':'T','Y':'U','Z':'V'},
        'X': {'A':'X','B':'Y','C':'Z','D':'A','E':'B','F':'C','G':'D','H':'E','I':'F','J':'G','K':'H','L':'I','M':'J','N':'K','O':'L','P':'M','Q':'N','R':'O','S':'P','T':'Q','U':'R','V':'S','W':'T','X':'U','Y':'V','Z':'W'},
        'Y': {'A':'Y','B':'Z','C':'A','D':'B','E':'C','F':'D','G':'E','H':'F','I':'G','J':'H','K':'I','L':'J','M':'K','N':'L','O':'M','P':'N','Q':'O','R':'P','S':'Q','T':'R','U':'S','V':'T','W':'U','X':'V','Y':'W','Z':'X'},
        'Z': {'A':'Z','B':'A','C':'B','D':'C','E':'D','F':'E','G':'F','H':'G','I':'H','J':'I','K':'J','L':'K','M':'L','N':'M','O':'N','P':'O','Q':'P','R':'Q','S':'R','T':'S','U':'T','V':'U','W':'V','X':'W','Y':'X','Z':'Y'}
    } #example : cipher_letter = vigenere_table[key_letter][plain_letter]
        #On hardcode la table de vigenere car ca prendrait plus de temps et d'énergie de  la générer.
        self.vigenere_inverse : dict = {
    'A': {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'},
    'B': {'B': 'A', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E', 'G': 'F', 'H': 'G', 'I': 'H', 'J': 'I', 'K': 'J', 'L': 'K', 'M': 'L', 'N': 'M', 'O': 'N', 'P': 'O', 'Q': 'P', 'R': 'Q', 'S': 'R', 'T': 'S', 'U': 'T', 'V': 'U', 'W': 'V', 'X': 'W', 'Y': 'X', 'Z': 'Y', 'A': 'Z'},
    'C': {'C': 'A', 'D': 'B', 'E': 'C', 'F': 'D', 'G': 'E', 'H': 'F', 'I': 'G', 'J': 'H', 'K': 'I', 'L': 'J', 'M': 'K', 'N': 'L', 'O': 'M', 'P': 'N', 'Q': 'O', 'R': 'P', 'S': 'Q', 'T': 'R', 'U': 'S', 'V': 'T', 'W': 'U', 'X': 'V', 'Y': 'W', 'Z': 'X', 'A': 'Y', 'B': 'Z'},
    'D': {'D': 'A', 'E': 'B', 'F': 'C', 'G': 'D', 'H': 'E', 'I': 'F', 'J': 'G', 'K': 'H', 'L': 'I', 'M': 'J', 'N': 'K', 'O': 'L', 'P': 'M', 'Q': 'N', 'R': 'O', 'S': 'P', 'T': 'Q', 'U': 'R', 'V': 'S', 'W': 'T', 'X': 'U', 'Y': 'V', 'Z': 'W', 'A': 'X', 'B': 'Y', 'C': 'Z'},
    'E': {'E': 'A', 'F': 'B', 'G': 'C', 'H': 'D', 'I': 'E', 'J': 'F', 'K': 'G', 'L': 'H', 'M': 'I', 'N': 'J', 'O': 'K', 'P': 'L', 'Q': 'M', 'R': 'N', 'S': 'O', 'T': 'P', 'U': 'Q', 'V': 'R', 'W': 'S', 'X': 'T', 'Y': 'U', 'Z': 'V', 'A': 'W', 'B': 'X', 'C': 'Y', 'D': 'Z'},
    'F': {'F': 'A', 'G': 'B', 'H': 'C', 'I': 'D', 'J': 'E', 'K': 'F', 'L': 'G', 'M': 'H', 'N': 'I', 'O': 'J', 'P': 'K', 'Q': 'L', 'R': 'M', 'S': 'N', 'T': 'O', 'U': 'P', 'V': 'Q', 'W': 'R', 'X': 'S', 'Y': 'T', 'Z': 'U', 'A': 'V', 'B': 'W', 'C': 'X', 'D': 'Y', 'E': 'Z'},
    'G': {'G': 'A', 'H': 'B', 'I': 'C', 'J': 'D', 'K': 'E', 'L': 'F', 'M': 'G', 'N': 'H', 'O': 'I', 'P': 'J', 'Q': 'K', 'R': 'L', 'S': 'M', 'T': 'N', 'U': 'O', 'V': 'P', 'W': 'Q', 'X': 'R', 'Y': 'S', 'Z': 'T', 'A': 'U', 'B': 'V', 'C': 'W', 'D': 'X', 'E': 'Y', 'F': 'Z'},
    'H': {'H': 'A', 'I': 'B', 'J': 'C', 'K': 'D', 'L': 'E', 'M': 'F', 'N': 'G', 'O': 'H', 'P': 'I', 'Q': 'J', 'R': 'K', 'S': 'L', 'T': 'M', 'U': 'N', 'V': 'O', 'W': 'P', 'X': 'Q', 'Y': 'R', 'Z': 'S', 'A': 'T', 'B': 'U', 'C': 'V', 'D': 'W', 'E': 'X', 'F': 'Y', 'G': 'Z'},
    'I': {'I': 'A', 'J': 'B', 'K': 'C', 'L': 'D', 'M': 'E', 'N': 'F', 'O': 'G', 'P': 'H', 'Q': 'I', 'R': 'J', 'S': 'K', 'T': 'L', 'U': 'M', 'V': 'N', 'W': 'O', 'X': 'P', 'Y': 'Q', 'Z': 'R', 'A': 'S', 'B': 'T', 'C': 'U', 'D': 'V', 'E': 'W', 'F': 'X', 'G': 'Y', 'H': 'Z'},
    'J': {'J': 'A', 'K': 'B', 'L': 'C', 'M': 'D', 'N': 'E', 'O': 'F', 'P': 'G', 'Q': 'H', 'R': 'I', 'S': 'J', 'T': 'K', 'U': 'L', 'V': 'M', 'W': 'N', 'X': 'O', 'Y': 'P', 'Z': 'Q', 'A': 'R', 'B': 'S', 'C': 'T', 'D': 'U', 'E': 'V', 'F': 'W', 'G': 'X', 'H': 'Y', 'I': 'Z'},
    'K': {'K': 'A', 'L': 'B', 'M': 'C', 'N': 'D', 'O': 'E', 'P': 'F', 'Q': 'G', 'R': 'H', 'S': 'I', 'T': 'J', 'U': 'K', 'V': 'L', 'W': 'M', 'X': 'N', 'Y': 'O', 'Z': 'P', 'A': 'Q', 'B': 'R', 'C': 'S', 'D': 'T', 'E': 'U', 'F': 'V', 'G': 'W', 'H': 'X', 'I': 'Y', 'J': 'Z'},
    'L': {'L': 'A', 'M': 'B', 'N': 'C', 'O': 'D', 'P': 'E', 'Q': 'F', 'R': 'G', 'S': 'H', 'T': 'I', 'U': 'J', 'V': 'K', 'W': 'L', 'X': 'M', 'Y': 'N', 'Z': 'O', 'A': 'P', 'B': 'Q', 'C': 'R', 'D': 'S', 'E': 'T', 'F': 'U', 'G': 'V', 'H': 'W', 'I': 'X', 'J': 'Y', 'K': 'Z'},
    'M': {'M': 'A', 'N': 'B', 'O': 'C', 'P': 'D', 'Q': 'E', 'R': 'F', 'S': 'G', 'T': 'H', 'U': 'I', 'V': 'J', 'W': 'K', 'X': 'L', 'Y': 'M', 'Z': 'N', 'A': 'O', 'B': 'P', 'C': 'Q', 'D': 'R', 'E': 'S', 'F': 'T', 'G': 'U', 'H': 'V', 'I': 'W', 'J': 'X', 'K': 'Y', 'L': 'Z'},
    'N': {'N': 'A', 'O': 'B', 'P': 'C', 'Q': 'D', 'R': 'E', 'S': 'F', 'T': 'G', 'U': 'H', 'V': 'I', 'W': 'J', 'X': 'K', 'Y': 'L', 'Z': 'M', 'A': 'N', 'B': 'O', 'C': 'P', 'D': 'Q', 'E': 'R', 'F': 'S', 'G': 'T', 'H': 'U', 'I': 'V', 'J': 'W', 'K': 'X', 'L': 'Y', 'M': 'Z'},
    'O': {'O': 'A', 'P': 'B', 'Q': 'C', 'R': 'D', 'S': 'E', 'T': 'F', 'U': 'G', 'V': 'H', 'W': 'I', 'X': 'J', 'Y': 'K', 'Z': 'L', 'A': 'M', 'B': 'N', 'C': 'O', 'D': 'P', 'E': 'Q', 'F': 'R', 'G': 'S', 'H': 'T', 'I': 'U', 'J': 'V', 'K': 'W', 'L': 'X', 'M': 'Y', 'N': 'Z'},
    'P': {'P': 'A', 'Q': 'B', 'R': 'C', 'S': 'D', 'T': 'E', 'U': 'F', 'V': 'G', 'W': 'H', 'X': 'I', 'Y': 'J', 'Z': 'K', 'A': 'L', 'B': 'M', 'C': 'N', 'D': 'O', 'E': 'P', 'F': 'Q', 'G': 'R', 'H': 'S', 'I': 'T', 'J': 'U', 'K': 'V', 'L': 'W', 'M': 'X', 'N': 'Y', 'O': 'Z'},
    'Q': {'Q': 'A', 'R': 'B', 'S': 'C', 'T': 'D', 'U': 'E', 'V': 'F', 'W': 'G', 'X': 'H', 'Y': 'I', 'Z': 'J', 'A': 'K', 'B': 'L', 'C': 'M', 'D': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'}, # Note: Q est souvent son propre pivot selon la table
    'R': {'R': 'A', 'S': 'B', 'T': 'C', 'U': 'D', 'V': 'E', 'W': 'F', 'X': 'G', 'Y': 'H', 'Z': 'I', 'A': 'J', 'B': 'K', 'C': 'L', 'D': 'M', 'E': 'N', 'F': 'O', 'G': 'P', 'H': 'Q', 'I': 'R', 'J': 'S', 'K': 'T', 'L': 'U', 'M': 'V', 'N': 'W', 'O': 'X', 'P': 'Y', 'Q': 'Z'},
    'S': {'S': 'A', 'T': 'B', 'U': 'C', 'V': 'D', 'W': 'E', 'X': 'F', 'Y': 'G', 'Z': 'H', 'A': 'I', 'B': 'J', 'C': 'K', 'D': 'L', 'E': 'M', 'F': 'N', 'G': 'O', 'H': 'P', 'I': 'Q', 'J': 'R', 'K': 'S', 'L': 'T', 'M': 'U', 'N': 'V', 'O': 'W', 'P': 'X', 'Q': 'Y', 'R': 'Z'},
    'T': {'T': 'A', 'U': 'B', 'V': 'C', 'W': 'D', 'X': 'E', 'Y': 'F', 'Z': 'G', 'A': 'H', 'B': 'I', 'C': 'J', 'D': 'K', 'E': 'L', 'F': 'M', 'G': 'N', 'H': 'O', 'I': 'P', 'J': 'Q', 'K': 'R', 'L': 'S', 'M': 'T', 'N': 'U', 'O': 'V', 'P': 'W', 'Q': 'X', 'R': 'Y', 'S': 'Z'},
    'U': {'U': 'A', 'V': 'B', 'W': 'C', 'X': 'D', 'Y': 'E', 'Z': 'F', 'A': 'G', 'B': 'H', 'C': 'I', 'D': 'J', 'E': 'K', 'F': 'L', 'G': 'M', 'H': 'N', 'I': 'O', 'J': 'P', 'K': 'Q', 'L': 'R', 'M': 'S', 'N': 'T', 'O': 'U', 'P': 'V', 'Q': 'W', 'R': 'X', 'S': 'Y', 'T': 'Z'},
    'V': {'V': 'A', 'W': 'B', 'X': 'C', 'Y': 'D', 'Z': 'E', 'A': 'F', 'B': 'G', 'C': 'H', 'D': 'I', 'E': 'J', 'F': 'K', 'G': 'L', 'H': 'M', 'I': 'N', 'J': 'O', 'K': 'P', 'L': 'Q', 'M': 'R', 'N': 'S', 'O': 'T', 'P': 'U', 'Q': 'V', 'R': 'W', 'S': 'X', 'T': 'Y', 'U': 'Z'},
    'W': {'W': 'A', 'X': 'B', 'Y': 'C', 'Z': 'D', 'A': 'E', 'B': 'F', 'C': 'G', 'D': 'H', 'E': 'I', 'F': 'J', 'G': 'K', 'H': 'L', 'I': 'M', 'J': 'N', 'K': 'O', 'L': 'P', 'M': 'Q', 'N': 'R', 'O': 'S', 'P': 'T', 'Q': 'U', 'R': 'V', 'S': 'W', 'T': 'X', 'U': 'Y', 'V': 'Z'},
    'X': {'X': 'A', 'Y': 'B', 'Z': 'C', 'A': 'D', 'B': 'E', 'C': 'F', 'D': 'G', 'E': 'H', 'F': 'I', 'G': 'J', 'H': 'K', 'I': 'L', 'J': 'M', 'K': 'N', 'L': 'O', 'M': 'P', 'N': 'Q', 'O': 'R', 'P': 'S', 'Q': 'T', 'R': 'U', 'S': 'V', 'T': 'W', 'U': 'X', 'V': 'Y', 'W': 'Z'},
    'Y': {'Y': 'A', 'Z': 'B', 'A': 'C', 'B': 'D', 'C': 'E', 'D': 'F', 'E': 'G', 'F': 'H', 'G': 'I', 'H': 'J', 'I': 'K', 'J': 'L', 'K': 'M', 'L': 'N', 'M': 'O', 'N': 'P', 'O': 'Q', 'P': 'R', 'Q': 'S', 'R': 'T', 'S': 'U', 'T': 'V', 'U': 'W', 'V': 'X', 'W': 'Y', 'X': 'Z'},
    'Z': {'Z': 'A', 'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': 'G', 'G': 'H', 'H': 'I', 'I': 'J', 'J': 'K', 'K': 'L', 'L': 'M', 'M': 'N', 'N': 'O', 'O': 'P', 'P': 'Q', 'Q': 'R', 'R': 'S', 'S': 'T', 'T': 'U', 'U': 'V', 'V': 'W', 'W': 'X', 'X': 'Y', 'Y': 'Z'}
}
        self.original : str = input
        self.input : str = ''.join([lettre for lettre in input if lettre.isalpha()])
    
    def encode(self, key : str) -> str:
        #example : cipher_letter = vigenere_table[key_letter][plain_letter]
        encoded : str = ""
        key : str = "".join(char for char in key.upper() if char.isalpha())
        i :int = 0
        plaintext = self.original.upper()
        for char in plaintext :
            if char.isalpha():
                encoded += self.vigenere_table[key[i%(len(key))]][char]
                i+=1
            else :
                encoded += char
        return(encoded)
    
    def decode(self, key : str) -> str:
        decoded : str = ""
        key : str = "".join(char for char in key.upper() if char.isalpha())
        plaintext : str = self.original
        i : int = 0
        for char in plaintext :
            if char.isalpha() :
                decoded += self.vigenere_inverse[key[i%(len(key))]][char]
                i+=1
            else :
                decoded += char
        return(decoded)

    def decrypt(self, min : int, langue : str) -> str:
        input : str = self.input.upper()
        pas = 1
        while Calcul_IC(input, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', pas) < min :
            pas+=1
        fractionne = [input[start::pas] for start in range(pas)]
        indices_cles = [caesar(bout).decrypt_freq(langue) for bout in fractionne]
        key = (['ABCDEFGHIJKLMNOPQRSTUVWXYZ'[(26 - i) % 26] for i in indices_cles])

        return(''.join(key), self.decode(''.join(key)))


#Cette fonction peut être utile dans tout le projet donc je la laisse en dehors de tout objet :
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

#test vigenere
#txt = 'Il y avait en Westphalie, dans le chateau de monsieur le baron de Thunder-ten-tronckh, un jeune garcon a qui la nature avait donne les moeurs les plus douces'
txt = "Le but de ce projet est de programmer des algorithmes de chiffrements utilises avant l’utilisation d’algorithmes modernes, mais surtout de programmer des algorithmes capables de casser ces chiffrements anciens. Dans un premier temps, il faudra programmer en python le code de cesar, le chiffre de Vigenere ainsi que la scytale, et une substitution monoalphabetique generale. Toutes les descriptions peuvent etre trouves sur internet facilement."
encoded = (vigenere(txt).encode('AMELIE'))
decoded = (vigenere(encoded.upper()).decrypt(0.065, 'francais'))
print(encoded)
print(decoded)

#test césar :
"""encoded = (caesar(txt).encode(5))
decoded = (caesar(encoded).decode_freq('francais'))
print(encoded)
print(decoded)"""