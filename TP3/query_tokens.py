import string
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
STOPWORDS = stopwords.words("english")

def tokenize_without_stopwords_punctuation(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))  # Supress the punctuation 
    tokens = [word for word in text.split() if word not in STOPWORDS]  # remove the stopwords
    return tokens

def tokenize_space(text): # Space tokenization
     text = text.lower()
     token = text.split()
     return token

def expand_token_with_synonym(token, synonyms_dict): # Add every synonyms to the given token
    synonyms_token = [token]
    if token in synonyms_dict: # If the token has synonyms
        for syn in synonyms_dict[token]: # Add every synonym
            synonyms_token.append(syn)
    return synonyms_token

def expand_query_with_synonym(tokens_query, synonyms_dict): # Add every synonyms to the whole query
    expended_tokens = tokens_query
    for tok in tokens_query: # for every token of the query
        if tok in synonyms_dict: # If any has synonyms
            for syn in synonyms_dict[tok]:
                expended_tokens.append(syn) # add all the synonyms to the query
    return expended_tokens

def unify_query(tokens_query): # Delete every token that appears more than once in a query
    tokens = []
    for token in tokens_query:
        if token not in tokens: # Add every token only once in a new list
            tokens.append(token)
    return tokens # If we started with ["kids", "kids", "chocolate"], the result will be : ["kids", "chocolate"] 