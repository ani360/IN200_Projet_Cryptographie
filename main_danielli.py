import unicodedata
import json

def sanitize(input_str: str) -> str:
    normalized = unicodedata.normalize('NFD', input_str)
    result = "".join(char for char in normalized if unicodedata.category(char) != 'Mn')
    final_list_char = []
    for char in result:
        if char.isalpha() or char.isspace():
            final_list_char.append(char.upper())
    return "".join(final_list_char)

def caesar(message, cle, alphabet):
    message_chiffre = ""
    taille = len(alphabet)
    for letter in message:
        if letter in alphabet:
            index = alphabet.find(letter)
            nouvel_index = (index + cle) % taille
            message_chiffre += alphabet[nouvel_index]
        else:
            message_chiffre += letter
    return message_chiffre

def main():
    f_input = open("LangDict.json", "r")
    langues = json.load(f_input)
    f_input.close()
    
    for nom_langue in langues.keys():
        print("- " + nom_langue)
        
    choix = input("Langue ???? : ").lower()
    alphabet = langues[choix]["alphabet"]
    texte = "BRAVO" ##########c'est un test pour que le prog puisse fonctionner
    mode = input("1.Chiffrer | 2.Déchiffrer | 3.Brute Force : ")
    message_propre = sanitize(texte)
    
    if mode == "1":
        cle = int(input("Clé : "))
        print("Résultat :", caesar(message_propre, cle, alphabet))

    elif mode == "2":
        cle = int(input("Clé : "))
        print("Résultat :", caesar(message_propre, -cle, alphabet))

    elif mode == "3":
        print("\nBRUTEFORCEEEEEEEEEEE")
        for k in range(len(alphabet)):
            tentative_de_bruteforce = caesar(message_propre, -k, alphabet)
            print("Clé " + str(k) + " : " + tentative_de_bruteforce)

######## Remy comment ca marche l'analyse de frequence si j'ai bien compris je dois trouver la lettre la plus fréquente dans le texte puis je regarde dans  JSON quelle est la lettre la plus fréquente pour la langue choisie pour ensuite calculer la distance entre les deux pour en deduire la clé c'et bien ca ?

