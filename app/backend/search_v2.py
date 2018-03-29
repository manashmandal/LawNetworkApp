"""
Instructions:

1. Process input query, tokenize it and prepare bigram for it
2. Run the input query through the database and fine the related laws
3. Prepare a dynamic graph using citation details

"""
from . import Bigram, tfidf_model, tfidf_bigram_model, index_bigram_dense, index_dense, vocabulary_bigram, vocabulary, LAW_SECTION_ID_LIST
import numpy as np
from app import mongo

# Process using this sfunction when someone enters query
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

        # Prepare the law related section map
        law_related_sections = { str(law_id) : [] for law_id in law_ids  }

        # Sorted law section 
        searched_laws_sections = sorted(np.array(LAW_SECTION_ID_LIST)[indices].tolist(), key= lambda x : x[0])

        
        for law in law_ids:
            for section in  searched_laws_sections:
                if law == section[0]:
                    law_related_sections[str(law)].append(section[1])

        # Remove and insert
        mongo.db.temp_search.remove()
        mongo.db.temp_search.insert_one({ 'search_result' : 
            {
            'unique_law_ids' : law_ids,
            'search_indices' : indices.tolist(), 
            'law_section_id' : np.array(LAW_SECTION_ID_LIST)[indices].tolist(),
            'law_related_section_map' : law_related_sections
            }
        })

        return law_ids




