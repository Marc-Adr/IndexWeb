import json
import string
from spacy.lang.en import stop_words
from datetime import datetime

# Fonction pour ouvrir un fichier JSONL et charger son contenu sous forme de liste de dictionnaires
def open_jsonl(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))  # Conversion de chaque ligne en dictionnaire JSON
    return data

# Fonction pour sauvegarder les index
def save_index(index, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=4)
        
# Fonction pour extraire l'ID du produit et les variantes à partir d'une URL donnée
def get_url_info(url):
    splitted_url = url.split("/")
    variant = None
    product_id = None
    url_id = None
    
    for i in range(len(splitted_url)):
        if splitted_url[i] == "product":  # Recherche du segment "product" dans l'URL
            if i + 1 == len(splitted_url):  # Vérifie s'il y a un ID après "product" (si l'url continue après)
                return product_id, variant
            else:
                url_id = splitted_url[i + 1]
    
    if url_id:
        if "?" in url_id:  # Gestion des paramètres dans l'URL
            split_id = url_id.split("?")
            product_id = int(split_id[0])  # Extraction de l'ID du produit
            if "variant" in url_id:
                variant = split_id[1]  # Extraction de la variante si elle est présente
        else:
            product_id = int(url_id)
    
    return product_id, variant


# Fonction pour tokeniser un texte tout en supprimant la ponctuation et les stopwords
def tokenize_without_stopwords_punctuation(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))  # Suppression de la ponctuation
    tokens = [word for word in text.split() if word not in stop_words.STOP_WORDS]  # Suppression des stopwords
    return tokens

# Création d'un index inversé pour un champ donné (titre ou description)
def create_inverted_index_title_description(products, field): # field étant "title" ou "description"
    inverted_index = {}
    for product in products: # Pour chaque produit dans products
        id = product["url"]  # Utilisation de l'URL comme identifiant du produit
        tokens = tokenize_without_stopwords_punctuation(product.get(field, "")) # tokeniser
        for token in tokens:
            if token not in inverted_index:
                inverted_index[token] = []
            if id not in inverted_index[token]:
                inverted_index[token].append(id)  # Association des tokens aux produits correspondants
    return inverted_index

# Création d'un index basé sur les avis des produits
def create_index_reviews(products):
    index_review = {}
    for product in products:
        nb_reviews = 0 # Nombre d'avis
        avg_rating = None # Moyenne des avis
        last_rating = None # Dernier avi
        id = product["url"]
        
        if "product_reviews" in product and len(product["product_reviews"]) >= 1: # S'il y des reviews pour un produit
            sum_ratings = 0
            product_reviews = product["product_reviews"] 
            nb_reviews = len(product_reviews) # On compte le nombre d'avis
            
            for review in product_reviews:
                if "rating" in review: # S'il y a des notes dans les reviews
                    sum_ratings += review["rating"]  # Calcul de la somme des notes
            
            if nb_reviews != 0:
                avg_rating = sum_ratings / nb_reviews  # Calcul de la moyenne des notes
            
            # Recherche de l'avis le plus récent
            latest_date = max(range(len(product_reviews)), 
                              key=lambda i: datetime.strptime(product_reviews[i]["date"], "%Y-%m-%d")) #Recherche de l'index de l'avis pour lequel la date est la plus grande
            last_rating = product_reviews[latest_date]["rating"] # Note du dernier avis
        
        index_review[id] = {"number_reviews": nb_reviews, "average_rating": avg_rating, "latest_rating": last_rating}
    return index_review

# Création d'un index inversé basé sur les caractéristiques des produits
def create_inverted_index_features(products, field): #field pouvant être "brand" ou "made in"
    inverted_index_features = {}
    for product in products:
        id = product["url"] #id du produit étant l'url
        if "product_features" in product: # S'il y a des features dans le produit
            product_features = product["product_features"]
            if field in product_features: # S'il y a ce que l'on cherche (origine ou marque) dans les features
                token = product_features[field].lower() #tokenize le feature
                if token not in inverted_index_features:
                    inverted_index_features[token] = []
                if id not in inverted_index_features[token]:
                    inverted_index_features[token].append(id) # Association des tokens aux produits correspondants
    return inverted_index_features

# Création d'un index positionnel pour un champ donné (titre ou description)
def create_positional_index(products, field):
    positional_index = {}
    for product in products:
        id = product["url"]
        tokens = tokenize_without_stopwords_punctuation(product.get(field, "")) #tokenize le champ
        for pos, token in enumerate(tokens):
            if token not in positional_index: #Si le token n'est dans dans l'index
                positional_index[token] = {}
            if id not in positional_index[token]:
                positional_index[token][id] = []
            positional_index[token][id].append(pos)  # Stocke les positions des tokens
    return positional_index
