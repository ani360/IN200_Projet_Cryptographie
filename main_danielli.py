#GEMINI/GPT/CLAUDE + Lis pas le objectif.md ; Pas très sérieux tt ça !

# 1. LES LANGUES
langues = {
    "english": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "french": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "german": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "spanish": "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ",
    "italian": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "portuguese": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "russian": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
}

# 2. LES FONCTIONS
def nettoyer(texte_du_fichier, alphabet, supprimer_espaces=False):
    message = ""
    accents = {
        'é':'e', 'è':'e', 'ê':'e', 'ë':'e', 'à':'a', 
        'â':'a', 'î':'i', 'ï':'i', 'ô':'o', 'ù':'u', 
        'û':'u', 'ç':'c'
    }

    for caractere in texte_du_fichier.upper():       
        if caractere.lower() in accents:
            caractere = accents[caractere.lower()].upper()

        if caractere == " " and supprimer_espaces == True:
            continue 

        if caractere in alphabet:
            message = message + caractere
            
    return message 

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

# 3. LE MAIN
def main():
    # Choix de la langue
    print("Langues disponibles :")
    for langue in langues.keys():
        print("- " + langue)
    
    choix_langue = input("Quelle langue choisir ? ").lower()
    alphabet = langues.get(choix_langue, langues["english"])
    
    print("Taille de l'alphabet :", len(alphabet))

    # CHOIX DU FICHIER
    chemin = input("Entrez l'adresse du fichier .txt : ")
    
    # ENCODAGE OU DECODAGE
    mode = input("Voulez-vous (1) Chiffrer ou (2) Déchiffrer ? ")
    cle = int(input("Clé de décalage : "))
    
    if mode == "2":
        cle = -cle
    # AJOUT OU SUPRESSION DES ESPACES

    reponse = input("Voulez-vous supprimer les espaces ? (o/n) : ")
    supprimer_espaces = (reponse.lower() == "o")

    # LECTURE DU FICHIER
    f_input = open(chemin, "r")
    texte_du_fichier = "" 
    ligne = f_input.readline() 
    while ligne != "":
        texte_du_fichier = texte_du_fichier + ligne 
        ligne = f_input.readline() 
    f_input.close()

    # ON TRAITE LE FICHIER
    message_propre = nettoyer(texte_du_fichier, alphabet, supprimer_espaces)
    resultat = caesar(message_propre, cle, alphabet)

    # RESULTATS
    print("\nTexte d'origine :")
    print(texte_du_fichier)
    print("\nRésultat :")
    print(resultat)

if __name__ == "__main__":
    main()