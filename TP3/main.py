from TP3.search_engine import *

synonym_country= open_json("TP3/origin_synonyms.json")
token_exemple =tokenize_without_stopwords_punctuation("La france est en europe alors que les usa en amérique")
expand_query(tokens=token_exemple, synonyms_dict=synonym_country)