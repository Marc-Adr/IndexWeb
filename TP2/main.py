from indexing import *
import json

#Importation du jsonl
produits = open_jsonl("products.jsonl")

#Regerder le détaille d'une url d'un produit (son id et ses variants)
url = produits[0]["url"] #Récupération de l'url de la page principal
get_url_info(url) #Retourne ses informations ((None, None) car ce n'est pas un produit)

url = produits[5]["url"] #Récupération de l'url d'un produit dans la liste
get_url_info(url) #Retourne ses informations (id, variant)

titre = produits[1]["title"] #Récupération du titre du premier produit
tokenize_without_stopwords_punctuation(titre) #Tokeniser sans stopword et ponctuation
tokenize_without_stopwords_punctuation(produits[1]["description"]) #Même chose avec la description

if __name__== "__main__":
    inverted_index_title=create_inverted_index_title_description(products=produits, field="title")
    inverted_index_description=create_inverted_index_title_description(products=produits, field="description")

    index_reviews=create_index_reviews(products=produits)

    index_features_brand=create_inverted_index_features(produits, field="brand")
    index_features_origin=create_inverted_index_features(produits, field="made in")


    inverted_index_title_position=create_positional_index(produits, "title")
    inverted_index_description_position=create_positional_index(produits, "description")

    save_index(inverted_index_title, "index_titre.json")
    save_index(inverted_index_description, "index_description.json")
    save_index(index_reviews, "index_reviews.json")
    save_index(index_features_origin, "index_origine.json")
    save_index(index_features_brand, "index_marque.json")
    save_index(inverted_index_title_position, "index_position_titre.json")
    save_index(inverted_index_description_position, "index_position_description.json")