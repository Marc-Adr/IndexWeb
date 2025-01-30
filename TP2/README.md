Ce dossier comprend les codes pour créer plusieurs index sur le fichier jsonl "products.jsonl"
Avant de lancer le code du main, il faut avoir les packages du requirements.txt
# pip install -r requirements.txt
Le début du main présente des fonctions intermédiaires
Ensuite, si on lance le if __name__="__main__", alors plusieurs json se créent selon l'index créé


Les différents fonctions sont:
## get_url_info
Cette fonction prend en entrée une url d'un produit de product et renvoie un couple (id, variant) selon ce qui est présent dans l'url

## create_inverted_index_title_description (Index inversé par titre ou description):

    But : Associe chaque token extrait des champs "title" ou "description" de chaque produit à une liste d'IDs de produits contenant ce token.
    Type : Index inversé (chaque mot dans le texte indexe les IDs des produits où il apparaît).

## create_index_reviews (Index basé sur les avis produits):

    But : Crée un index contenant des informations sur les avis des produits : nombre d'avis, note moyenne et dernière note.
    Contenu :
        number_reviews : Le nombre total d'avis pour un produit.
        average_rating : La moyenne des notes des avis.
        latest_rating : La dernière note donnée à un produit.

## create_inverted_index_features (Index inversé basé sur les caractéristiques des produits) :

    But : Crée un index inversé basé sur les caractéristiques des produits, comme la marque ou l'origine.
    Type : Index inversé des tokens extraits des "product_features".

## create_positional_index (Index positionnel):

    But : Crée un index positionnel pour chaque champ spécifié (ex : titre ou description), en enregistrant les positions des tokens dans chaque produit.
    Type : Index positionnel où chaque token est associé aux positions dans lesquelles il apparaît dans chaque produit.