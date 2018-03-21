"""
Instructions:

1. Process input query, tokenize it and prepare bigram for it
2. Run the input query through the database and fine the related laws
3. Prepare a dynamic graph using citation details

"""
from . import Bigram, tfidf_model, tfidf_bigram_model, index_bigram_dense, index_dense, vocabulary_bigram, vocabulary, LAW_SECTION_ID_LIST
import numpy as np

# Process using this function when someone enters query
# Process text v2
def process_text_v2(input_text, tokenize=False):
    valid_list = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎংঅআইঈউঊঋএঐওঔৌোৈেৃূুীিা")
    filter_text = [l for l in input_text if l in valid_list]
    if tokenize == True:
        return "".join(filter_text).lower().split()
    else:
        return "".join(filter_text).lower()

    return filter_text


# Search using bigram
def search_laws(query, max_result=10, use_bigram=False):

    query = process_text_v2(query, tokenize=True)

    if use_bigram == True:
        query = Bigram[query]

        query_tfidf = tfidf_bigram_model[vocabulary_bigram.doc2bow(query)]
        indices = index_bigram_dense[query_tfidf]
        # If no indices nothing found
        if (len(indices) == 0):
            return -1
        # Clipping the result
        indices = np.argsort(-indices)[:max_result]
        
        # Returning the laws only 
        law_ids = np.unique(np.array(LAW_SECTION_ID_LIST)[indices][:, 0]).tolist()

        return law_ids

    else:
        query_tfidf = tfidf_model[vocabulary.doc2bow(query)]
        indices = index_dense[query_tfidf]
        if (len(indices) == 0):
            return -1
        indices = np.argsort(-indices)[:max_result]

        # Returning the laws only 
        law_ids = np.unique(np.array(LAW_SECTION_ID_LIST)[indices][:, 0]).tolist()

        return law_ids




