from scoring import *
from query_tokens import *
from filter import *
from save_open_data import *

title_index = open_json("TP3/title_index.json")
description_index = open_json("TP3/description_index.json")
origin_index = open_json("TP3/origin_index.json")
brand_index = open_json("TP3/brand_index.json")
reviews_index = open_json("TP3/reviews_index.json")
synonym_country= open_json("TP3/origin_synonyms.json")
all_documents = open_jsonl("TP3/rearranged_products.jsonl")

query = "sneakers leather for kids" # Set the query you want to search the documents and rank them by scores
query_tokens = tokenize_without_stopwords_punctuation(query) # Tokenize the query

if __name__ == "__main__":
    
    # Filter the documents by the token of the query.
    #  all_match_url is the list of the documents that match all the tokens of the query either in description or in title
    # any_match_url are other documents that match any token but not all
    all_match_url, any_match_url = filter_all_documents(
        query=query_tokens, 
        title=title_index, 
        description=description_index,
        brand=brand_index, 
        origin=origin_index, 
        synonyms=synonym_country, 
        documents=all_documents
    )
    

    every_match_url = all_match_url + any_match_url # every_match_url regroups all the document that AT LEAST match any token of the query
    print("The number of filtered documents is " + str(len(every_match_url)))
    print("Starting from a number of original documents being " + str(len(all_documents)))

    every_match_document = associate_document_to_given_url( # Recreate the whole document by regrouping the url (id of the document) with all its features
        urls=every_match_url, 
        documents=all_documents
    )

    list_bm25 = [] # The result of bm25 scoring
    list_score_idea = [] # The result of the score I created
    for doc in every_match_document:
        score_bm25_title = bm25(field="title", doc=doc, documents=all_documents, tokens_query=query_tokens) # Get the bm25 score of the title of the document
        score_bm25_description = bm25(field="description", doc=doc, documents=all_documents, tokens_query=query_tokens) # bm25 of the description
        score_bm25 = 2 * score_bm25_title + score_bm25_description # Make the bm25 of the title more relevent than the description (personnal choice)
        list_bm25.append({"title": doc["title"], "description": doc["description"], "url": doc["url"], "score": score_bm25}) # Create the list of all the filtered docs that will be sorted by bm25 scores

        score_idea = calculate_score_idea(document=doc, tokens_query=query_tokens, weight_title=3, weight_description=1, # Calculte my original score
                                           weight_brand=2, weight_origin=2, weight_reviews=0.1, synonyms=synonym_country, index_reviews=reviews_index)
        if doc["url"] in all_match_url: # Add an exact match score (multiply the score or add to it)
            score_idea * 1.3 # I chose multiply 
        list_score_idea.append({"title": doc["title"], "description": doc["description"], "url": doc["url"], "score": score_idea}) # Create the list of the scores i created


    sorted_bm25 = sorted(list_bm25, key=lambda x: x["score"], reverse=True) # Rank the documents by decreasing bm25 scores
    save_data(index=sorted_bm25, file_path="TP3/result_bm25.json") # Save in a json

    sorted_idea = sorted(list_score_idea, key=lambda x: x["score"], reverse=True) # Rank the documents by decreasing scores of my own
    save_data(index=sorted_idea, file_path="TP3/result_score_idea.json") # Save in a json
