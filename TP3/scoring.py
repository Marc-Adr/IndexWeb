import numpy as np
from filter import *
from query_tokens import *



    
# Compute the bm25
def bm25(field, doc, documents,tokens_query, k1=1.2, b=0.75): # field = title or description
    doc_token = tokenize_without_stopwords_punctuation(doc.get(field, "")) # For every token of the given field (title or description) of the given document
    fieldLen = len(doc_token) # Store the number of tokens
    doclen = 0
    for d in documents: # For every documents
        d_token = tokenize_without_stopwords_punctuation(d.get(field, "")) # Of the matching field
        doclen += len(d_token)
    avgFieldLen = doclen/len(documents) # Average their number of tokens
    score_bm25 =0
    for token in tokens_query: #For every token of the query
        freq_token = doc_token.count(token) # Count the number of times it appears in the given document at the beginning
        freq_doc = 0
        for d in documents:
            d_token = tokenize_without_stopwords_punctuation(d.get(field, ""))
            if token in d_token: # for every  documents the token appears in
                freq_doc += 1 # Store the frequency of occurences in every documents
        IDF = np.log(1 + (len(documents) + freq_doc + 0.5)/(freq_doc + 0.5)) # Compute the IDF
        score_bm25 += IDF * (freq_token*(k1 + 1))/(freq_token + k1*(1-b +b*(fieldLen/avgFieldLen))) # sum the bm25
    return score_bm25


# Original score idea I created
def calculate_score_idea(document, tokens_query, weight_title, weight_description, weight_reviews, weight_origin, weight_brand, index_reviews, synonyms):
    expanded_query = expand_query_with_synonym(tokens_query=tokens_query, synonyms_dict=synonyms)
    title = tokenize_without_stopwords_punctuation(document.get("title", "")) # Tokenize the title of the document
    description = tokenize_without_stopwords_punctuation(document.get("description", "")) # and the description of the document
    nb_reviews = 0
    avg_reviews = 0
    origin = []
    brand = []
    if document["url"] in index_reviews: # If the document has reviews
        nb_reviews = index_reviews[document["url"]]["total_reviews"] # Get the number of reviews
        avg_reviews = index_reviews[document["url"]]["mean_mark"] # And the mean mark
    
    if "product_reviews" in document and len(document["product_reviews"]) >= 1:
        if "made in" in document["product_features"]:  
            origin = tokenize_space(document["product_features"]["made in"]) # Get the origin 
        
        if "brand" in document["product_features"]:
            brand = tokenize_space(document["product_features"]["brand"]) # And the brand

    score_idea = 0
    for token in expanded_query:
        title_freq = 0 # Calculate every frequency of the token occuring in each field
        description_freq = 0
        origin_freq = 0
        brand_freq = 0

        for title_token in title: # For every token of the title
            if title_token == token: # if the token of the title matches the token of the query
                title_freq +=1
        
        for description_token in description: # Same thing for every other fields
            if description_token == token:
                description_freq +=1
        
        for origin_token in origin:
            if origin_token == token:
                origin_freq +=1

        for brand_token in brand:
            if brand_token == token:
                brand_freq +=1

        # Then sum the score by multiplying every frequency to the wieght you give for the field (linear scoring)
        score_idea += title_freq*weight_title + description_freq*weight_description + origin_freq*weight_origin + brand_freq*weight_brand + nb_reviews*avg_reviews*weight_reviews
    
    return score_idea