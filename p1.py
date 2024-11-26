import json
from pymongo import MongoClient
from math import log, sqrt
from token_utils import Tokeniser, get_doc

# Définir la stop list
stoplist = ['the', 'of', 'in', 'on', 'to', 'a', 'has', 'been', 'most', 'around', 'due', 'are', 'that', 'can', 'lot']

# Connexion à MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/")
    client.admin.command('ping')  # Vérification de la connexion
    print("Connexion à MongoDB réussie.")
except Exception as e:
    print(f"Erreur de connexion à MongoDB : {e}")
    exit(1)

# Sélection de la base de données et de la collection
db = client["RI"]
collection = db["tfidf_index"]

# Chargement des documents
try:
    docs = get_doc()
    if not docs:
        print("Aucun document trouvé. Vérifiez le répertoire './Doc'.")
        exit(1)
except Exception as e:
    print(f"Erreur lors du chargement des documents : {e}")
    exit(1)

# Indexation avec calcul TF-IDF
print("Début de l'indexation avec TF-IDF...")
from collections import defaultdict

index = defaultdict(lambda: {"doc_ids": {}, "df": 0})
N = len(docs)  # Nombre total de documents

# Calcul de TF et DF
for doc_id, doc in enumerate(docs):
    tokens = Tokeniser([doc])
    term_counts = defaultdict(int)  # Compter les termes dans un document
    for token_list in tokens:
        for token in token_list:
            if token.lower() not in stoplist:
                term_counts[token] += 1

    # Mise à jour de l'index avec les TF et DF
    for term, count in term_counts.items():
        index[term]["doc_ids"][str(doc_id)] = count  # Utiliser des chaînes pour les clés de `doc_ids`
        index[term]["df"] += 1  # Document Frequency

# Calcul de TF-IDF
for term, data in index.items():
    for doc_id, tf in data["doc_ids"].items():
        # TF normalisé : fréquence brute divisée par le nombre total de termes dans le document
        tf_normalized = tf / sum(data["doc_ids"].values())
        # IDF : log(N / (1 + DF))
        idf = log(N / (1 + data["df"]))
        # TF-IDF
        data["doc_ids"][doc_id] = tf_normalized * idf

# Insertion dans MongoDB
print("Insertion des données dans MongoDB...")
collection.drop()  # Nettoyer l'ancienne collection
for term, data in index.items():
    collection.insert_one({"term": term, "doc_ids": data["doc_ids"], "df": data["df"]})
print("Indexation avec TF-IDF terminée et insérée dans MongoDB.")

# Exportation de l'index vers un fichier JSON
def export_index_to_json(file_path="tfidf_index.json"):
    try:
        documents = collection.find()
        index_data = []
        for doc in documents:
            doc["_id"] = str(doc["_id"])  # Convertir ObjectId en string
            index_data.append(doc)
        # Trier les termes pour une meilleure lisibilité
        index_data = sorted(index_data, key=lambda x: x["term"])
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(index_data, f, indent=4, ensure_ascii=False)
        print(f"Index TF-IDF exporté avec succès dans le fichier : {file_path}")
    except Exception as e:
        print(f"Erreur lors de l'exportation de l'index : {e}")

export_index_to_json()

# Recherche avec similarité cosinus
def search_query(query):
    try:
        tokens = Tokeniser([query])
        query_vector = defaultdict(float)
        results = defaultdict(float)

        # Calcul du vecteur de la requête
        for token_list in tokens:
            for token in token_list:
                if token.lower() not in stoplist:
                    result = collection.find_one({"term": token})
                    if result:
                        idf = log(N / (1 + result["df"]))
                        query_vector[token] += idf  # Ajout du poids IDF du terme

        # Calcul de la similarité cosinus
        for token, query_weight in query_vector.items():
            result = collection.find_one({"term": token})
            if result:
                for doc_id, tfidf in result["doc_ids"].items():
                    results[doc_id] += query_weight * tfidf  # Produit scalaire

        # Normalisation des scores
        for doc_id in results:
            doc_vector_length = sqrt(sum([tfidf ** 2 for tfidf in result["doc_ids"].values()]))
            query_vector_length = sqrt(sum([weight ** 2 for weight in query_vector.values()]))
            if doc_vector_length > 0 and query_vector_length > 0:
                results[doc_id] /= (doc_vector_length * query_vector_length)

        # Tri des résultats par score décroissant
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        return sorted_results
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
        return {}

# Entrer une requête pour tester la recherche
query = input("Entrez une requête pour rechercher : ")
results = search_query(query)
print("Résultats de la recherche :")
for doc_id, score in results:
    print(f"Document {doc_id} : score = {score:.4f}")
