import json
import numpy as np
import string
from datetime import datetime
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
STOPWORDS = stopwords.words("english")

# Fonction pour ouvrir un fichier JSONL et charger son contenu sous forme de liste de dictionnaires
def open_jsonl(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))  # Conversion de chaque ligne en dictionnaire JSON
    return data

def open_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    return data

# Fonction pour sauvegarder les index
def save_data(index, file_path):
    with open("TP3/"+file_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=4)

# Fonction pour tokeniser un texte tout en supprimant la ponctuation et les stopwords
def tokenize_without_stopwords_punctuation(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))  # Suppression de la ponctuation
    tokens = [word for word in text.split() if word not in STOPWORDS]  # Suppression des stopwords
    return tokens

def tokenize_space(text):
     text = text.lower()
     token = text.split()
     return token

def expand_query(tokens, synonyms_dict):
    expended_tokens = tokens
    for tok in tokens:
        if tok in synonyms_dict:
            for syn in synonyms_dict[tok]:
                expended_tokens.append(syn)
    return expended_tokens

def verify_any_token(document, tokens):
    return any(token in document for token in tokens)

def verify_all_token(document, tokens):
    return all(token in document for token in tokens)

def bm25(field, doc, documents,tokens_query, k1=1.2, b=0.75): # field = title ou description
    doc_token = tokenize_without_stopwords_punctuation(doc.get(field, ""))
    fieldLen = len(doc_token)
    doclen = 0
    for d in documents:
        d_token = tokenize_without_stopwords_punctuation(d.get(field, ""))
        doclen += len(d_token)
    avgFieldLen = doclen/len(documents)
    score_bm25 =0
    for token in tokens_query:
        freq_token = doc_token.count(token)
        freq_doc = 0
        for d in documents:
            d_token = tokenize_without_stopwords_punctuation(d.get(field, ""))
            if token in d_token:
                freq_doc += 1
        IDF = np.log(1 + (len(documents) + freq_doc + 0.5)/(freq_doc + 0.5))
        score_bm25 += IDF * (freq_token*(k1 + 1))/(freq_token + k1*(1-b +b*(fieldLen/avgFieldLen)))
    return score_bm25

def exact_match(document, tokens_query):
    return set(tokens_query).issubset(set(document))


def score_idea(document, weight_title, weight_description, weight_title_and_description, weight_nb_reviews, weight_avg_reviews):
    a=2


