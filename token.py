import re
import glob
import os

def Tokeniser(lst): 
    #  Tokeniser par rapport aux blancs et tous les caractères spéciaux 
    return [re.findall(r'[a-zA-Z0-9]+', l) for l in lst]


def get_requet(path='requet.txt'):
    # Lire le contenu du fichier de requete
    d =[]
    filename = glob.glob(path)
    for file in filename:
        with open(file , 'r') as f:
            d.extend(line.lower() for line in f.read().splitlines()) 
    return d


def get_doc(repertoire="./Doc"):
    # Lire tous les documents dans le répertoire
    try:
        if not os.path.exists(repertoire):
            raise FileNotFoundError(f"Le répertoire {repertoire} n'existe pas.")
        
        fichiers = os.listdir(repertoire)
        data = []
        if not fichiers:
            print(f"Aucun fichier trouvé dans le répertoire {repertoire}.")
        else:
            for nom_fichier in fichiers:
                if nom_fichier.endswith(".txt"):
                    chemin_fichier = os.path.join(repertoire, nom_fichier)
                    try:
                        with open(chemin_fichier, "r", encoding="utf-8") as fichier:
                            data.extend(line.lower() for line in fichier.read().splitlines())
                    except Exception as e:
                        print(f"Erreur lors de la lecture du fichier {nom_fichier} : {e}")
        return data
    except FileNotFoundError as e:
        print(f"Erreur : {e}")
        return []
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
        return []
    
def voyelle(mot):   
    v = "aouei"  
    return any(char in v for char in mot[:-2])

def extract(mot, l):
    return mot[:-len(l)]

def cond(mot, t):
    # verrifier si un mot ce termine avec une sequence 
    return mot.endswith(t)

def m(M):
    vowels = "aeiou" 
    count = 0
    
    for i in range(len(M) - 1):  
        if M[i].isalpha() and M[i+1].isalpha():  
            if M[i] not in vowels and M[i+1] in vowels:  
                count += 1
                
    return count




