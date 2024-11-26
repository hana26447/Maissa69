from token import voyelle, cond, m, extract

def filter(mot):
    if len(mot)>3:
        if cond(mot, "ies"):
            mot = extract(mot, "ies")
        elif cond(mot, "s"):
            mot = extract(mot, "s")
        elif (cond(mot, "ed") and voyelle(extract(mot, "ed"))):
            mot = extract(mot, "ed")
        elif (cond(mot, "y")):
            mot = extract(mot, "y") +"i"
        elif len(mot) >6:
            if (cond(mot, "ation")and m(mot)>2):
                mot = extract(mot, "ation") + "ate"
        elif (cond(mot, "ant") and m(mot)>1):
            mot = extract(mot, "ant")
        elif (cond(mot,"ss") and m(mot)>1):
            mot = extract(mot, "ss")
        elif (cond(mot, "al") and m(mot)>1):
            mot = extract(mot, "al")
        elif (cond(mot, "e") and m(mot)>1):
            mot = extract(mot, "e")
        elif (cond(mot, "t") and m(extract(mot, "t"))):
            mot = extract(mot, "t")
    
    return mot
        

import os

# Chemin du répertoire contenant les fichiers .txt
repertoire = "./Doc"

# Parcourir les fichiers dans le répertoire
for nom_fichier in os.listdir(repertoire):
    # Vérifier si le fichier a l'extension .txt
    if nom_fichier.endswith("*.txt"):
        chemin_complet = os.path.join(repertoire, nom_fichier)
        print(f"Lecture du fichier : {chemin_complet}")
        
        # Lire le contenu du fichier
        with open(chemin_complet, 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()
            print(contenu)
            print("-" * 50)  # Séparateur entre les fichiers



