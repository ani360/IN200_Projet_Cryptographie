#je définis ici un programme qui permettra pour les différents programmes de cryptage/décryptage de prendre en entrée des fichier .txt et de rendre des fichiers.txt en output

#cette fonction permet d'extraire le texte contenu dans un fichier en paramètre, 
#elle permet donc de prendre un fichier de l'ordinateur en paramèrtre dans vos fonctions à la place d'un string ou autre

def conversion_texte(path_fichier_entrée):
    fichier_entrée = open(path_fichier_entrée, 'r')
    texte = ""
    ligne = fichier_entrée.readline()
    while ligne != '': 
        texte += ligne
        ligne = fichier_entrée.readline()
    fichier_entrée.close()
    return texte

#cette fonction permet quand a elle de prendre le texte rendu par une fonction de cryptage/décryptage
#et d'en faire une fichier .txt une entête pourra être écrite au dessus du texte


def écriture_fichier_sortie(path_fichier_output, texte_output, entête): 
    fichier_output = open(path_fichier_output, 'w')
    longueur_texte = len(texte_output)
    if longueur_texte <= 100 :
        fichier_output.write('\n' + entête + ":" + '\n' + '\n' + texte_output + '\n')
    else : 
        fichier_output.write('\n' + entête + ":" + '\n' + '\n')
        for n in range((longueur_texte//100)):
            fichier_output.write(texte_output[(n*100):((n+1)*100)] + '\n')
        fichier_output.write(texte_output[(longueur_texte//100)*100:] + '\n')
    fichier_output.close()


écriture_fichier_sortie("C:/Users/Utilisateur/Desktop/IN200/Test.txt", conversion_texte("C:/Users/Utilisateur/Desktop/IN200/Test.txt"), "premier test")







