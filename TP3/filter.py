from query_tokens import *

def verify_any_token(index, tokens_query, document): # Verify if any token is linked to a document
    for token in tokens_query: # For each token in the query
        if token in index: # if it exists in the index
            if document in index[token]: # If the document has this token (given by the index)
                return True
    return False

#The following function returns all the documents that match all the tokens of the query
#So it verifies for each document if it has all the tokens and add it to a list if it does.
# This will also serves as the exact match for scoring later
def filter_by_all_tokens(tokens_query, index, synonym_dict):
    for i in range(len(tokens_query)): # For every token in the query
        documents = []
        token = tokens_query[i] # Every token
        token_ex = expand_token_with_synonym(token=token, synonyms_dict=synonym_dict) # Add alll the synonyms of the given token
        for synonym in token_ex: # For every synonym (or the token alone if it didn't have any synonym)
            if synonym in index: # If it exits in the index
                for doc in index[synonym]: # for every document listed for this token
                    documents.append(doc) # Get all the documents linked to this token

        if i == 0: # Initialiaze
            all_tokens = documents # all_tokens is a list of every document url that has all the tokens
        
        # Intersect of the remaining documents that still have all the tokens for now and the documents that match the imminant token
        all_tokens = [doc for doc in all_tokens if doc in documents] 


        if not all_tokens: # If at any point, all_token is empty, then no documents match all the tokens of the query
            return False
        
    return all_tokens # If the loop ended, then all_tokens is not empty so documents match all the tokens of the query


# Filter the documents url by the tokens of the query
def filter_all_documents(query, title, description, brand, origin, synonyms, documents):
    all_tokens_documents = [] # The documents that match all the tokens
    filtered_documents = [] # The documents that match any of the tokens

    # Verify if documents match every token
    all_title = filter_by_all_tokens(tokens_query=query, index=title, synonym_dict=synonyms) # In their title
    all_description = filter_by_all_tokens(tokens_query=query, index=description, synonym_dict=synonyms) # In their description

    if all_title: # If any of their field match all the tokens, then add it
        all_tokens_documents += all_title
    
    if all_description:
        all_tokens_documents += all_description

    expanded_query = expand_query_with_synonym(tokens_query=query, synonyms_dict=synonyms) # Add the synonyms for any tokens
    #If any synonym match the token, then the whole document is added

    for doc in documents: # For every document
        doc = doc["url"] 
        if doc not in all_tokens_documents: # If their url is not already in all_tokens_documents
            if verify_any_token(index=title, tokens_query=expanded_query, document=doc): # Verify if the title match any token
                if doc not in filtered_documents: # And if the document was not already added
                    filtered_documents.append(doc)

            if verify_any_token(index=description, tokens_query=expanded_query, document=doc): # the description
                if doc not in filtered_documents:
                    filtered_documents.append(doc)

            if verify_any_token(index=brand, tokens_query=expanded_query, document=doc): # The brand
                if doc not in filtered_documents:
                    filtered_documents.append(doc)

            if verify_any_token(index=origin, tokens_query=expanded_query, document=doc): # The origin
                if doc not in filtered_documents:
                    filtered_documents.append(doc)

    return all_tokens_documents, filtered_documents

def associate_document_to_given_url(urls, documents): # For a list of urls, associate the whole document to it (the jsonl)
    associated_documents = []
    for doc in documents: # For every documents
        for url in urls: # for every url
            if doc["url"] ==url: # If any url of the documents match any url of the list, then add it
                associated_documents.append(doc)
    return associated_documents