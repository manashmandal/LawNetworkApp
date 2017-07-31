from . import *
from app import mongo
from bisect import bisect
from textblob import TextBlob
from bson.objectid import ObjectId


def _search(text, only_ngram_search=True, exclude_unigram=True):
    # Ids
    _ids = []

    # Final search text
    ngram_search = ""

    # stemmed text
    text = nlp(u'' + text)

    # Only alphabet is real
    filtered_text = " ".join([stemmer.stem(t.lower_) for t in text if t.is_alpha])


    # print(filtered_text)

    # Make a spacy doc
    text_doc = nlp(u'' + filtered_text)

    # Take word count
    word_count = text_doc.__len__()

    # DEBUG_MSG
    # print("WORD COUNT : {}".format(word_count))

    # If strict ngram is turned on, exclude unigrams
    if exclude_unigram == True:

        sw = filtered_text.lower().split(' ')

        search_combinations = ["_".join([word for word in combination]) for combination in
                               itertools.permutations(sw, len(sw))]

        for search_words in search_combinations:
            for _id in range(1, LAW_COUNT):
                bigram_text = mongo.db.bigrams.find_one({'law_id' : _id })['text']
                trigram_text = mongo.db.trigrams.find_one({'law_id' : _id})['text']

                for btoken, ttoken in zip(bigram_text.split(' '), trigram_text.split(' ')):
                    if '_' in btoken or '_' in ttoken:
                        if search_words == btoken or search_words == ttoken:
                            _ids.append(_id)
        return list(set(_ids))


    else:

        # Make ngram then search
        if (word_count > 1 and word_count < 4):
            # Splitting the keywords into separate words
            search_words = filtered_text.lower().split(' ')

            # DEBUG_MSG
            # print("SEARCH WORDS ", search_words)

            # Creating combination of n-grams
            search_combinations = ["_".join([word for word in combination]) for combination in itertools.permutations(search_words, len(search_words))]

            for combination in search_combinations:
                _ids.append(search_database(combination, ngram_search=True))


            _ids = list(set(sum(_ids, [])))

            # print("NGRAM _ ")


        if only_ngram_search == False or word_count > 3:
            all_key_search = search_database(filtered_text, ngram_search=False, delimiter=" ")

            # Concatening the list
            _ids = _ids + all_key_search

            # DEBUG_MSG
            # print("ALL KEY SEARCH: {}".format(all_key_search))

    return sorted(list(set(_ids)))



def search_database(text, ngram_search=True, delimiter='_'):
    _ids = []

    if ngram_search == True:
        for _id in range(1, LAW_COUNT):
            law_bigram = mongo.db.bigrams.find_one({'law_id' : _id})['text']
            law_trigram = mongo.db.trigrams.find_one({'law_id' : _id})['text']
            if text in law_bigram or text in law_trigram:
                _ids.append(_id)
    else:
        keywords = [stemmer.stem(key) for key in text.split(delimiter)]

        for _id in range(1, LAW_COUNT):
            law_bigram = mongo.db.bigrams.find_one({'law_id' : _id})['text']
            found_all = []
            for key in keywords:
                if key in law_bigram.split():
                    found_all.append(1)
            if sum(found_all) == len(keywords):
                _ids.append(_id)

    return _ids


# Input list of laws [See the implementation in optimized network builder ipynb]
# TODO: add an option to remove self citation [option : exclude_self_cite]
# TODO: if details don't exist remove the connection [option : exclude_non_detail]
def build_main_network_connection(search_result, exclude_self_cite=False, exclude_non_detail=False):
    list_connections = []
    for sr in search_result:
        law = mongo.db.citations.find_one({'node' : sr})
        connection = list(set.intersection(set(search_result), set(law['links'])))
        for c in connection:
            list_connections.append(
                {'from' : law['node'], 'to' : c}
            )
    return list_connections


"""
Network Builder Functions
"""
# Filter outs entites given law id
def filter_entity(_id, entity_type='ORGANIZATION'):
    entities = mongo.db.entities.find_one({'law_id' : _id})[
        'entity_group'
    ]
    
    filtered_entities = [
        item[0].replace('[', '').replace(']', '').strip().lower() for item in entities if item[1] == entity_type
    ]
    
    return filtered_entities




# Returns entity to section map
def entity_to_section_map(_id, verbose=False):
    # Load Stopwords
    _stopwords = mongo.db.stopwords.find_one({"_id" : ObjectId("5970d42eed9d820af407f0d5")})['stopwords']

    # Get sections
    sections = mongo.db.laws.find_one({'law_id' : _id})['section_details']
    # Get entities
    entities = list(set(filter_entity(_id)))
    
    entity_section_map = []
    
    for entity in entities:
        # Lower the entity
        entity = entity.lower()
   
        # Search through the sections
        for section_key in sections:
        
            if entity in sections[section_key].lower():
                
                # Filter unicode characters
                filter_section = ''.join([i if ord(i) < 128 else ' ' for i in sections[section_key].lower()])
            
                # Get the ngram 
                section_blob = TextBlob(filter_section)
                
                section_blob_gram = [list(text) for text in section_blob.ngrams(n=2)]
                
                idx = 0
                bigrams = []
                bigram_track = []
                for item in section_blob_gram:
                    count = section_blob_gram.count(item)
                    if ( count > 1) and item not in bigrams:
                        stopword_alert = False
                        for _item in item:
                            if _item in _stopwords:
                                stopword_alert = True
                #                 print("FOUND STOP WORD: {}".format(_item))
                                # Uncomment the below lines for some extra bigrams [warning]
                #             else:
                #                 stopword_alert = not stopword_alert
                        if stopword_alert == False:
                            if item not in bigram_track:
                                bigrams.append({'gram' : item, 'count' : count, 'phrase' : " ".join(i for i in item)})
                                bigram_track.append(item)
                    idx += 1
                
                entity_section_map.append({
                    'law_id' : _id,
                    'entity' : entity,
                    'section_key' : section_key,
                    'section_text' : sections[section_key],
                    'bigrams' : bigrams
                })
                
    return entity_section_map



# Makes Section <-> Entity Network
def make_section_entity_network(_id):
    # Get map list
    _map_list = entity_to_section_map(_id)
    
    _from_nodes = []
    _to_nodes = []
    tracker = []
    node_to_id = {}
    id_to_node = {}
    
    # Nodes 
    nodes = []
    
    last_idx = 0
    idx = 0
    # Connection begin from 
    for item in _map_list:
        if item['entity'] not in tracker:
            tracker.append(item['entity'])
            _from_nodes.append({'id': idx + 1, 'value' : 5, 'label' : item['entity'], 'type':'entity'})
            nodes.append({'id' : idx + 1, 'value' : 5, 'label' : item['entity'], 'type' : 'entity'})
            node_to_id[item['entity']] = idx + 1
            id_to_node[idx + 1] = item['entity']
            idx += 1
    last_idx = idx
                
                
    # Connection to [section keys]
    for item in _map_list:
        if item['section_key'] not in tracker:
            tracker.append(item['section_key'])
            last_idx += 1
            _to_nodes.append({'id' : last_idx, 'value' : 3, 'label' : item['section_key']})
            nodes.append({'id' : last_idx, 'value' : 3, 'label' : item['section_key'], 'type' : 'section_key'})
            node_to_id[item['section_key']] = last_idx
            id_to_node[last_idx] = item['section_key']
    
    # Edges
    edges = []
            
    # Make connection
    for item in _map_list:
        # Add key section
        edges.append(
            {'from' : node_to_id[item['entity']], 'to' : node_to_id[item['section_key']], 'value' : 1, 'title' : item['section_text']}
        )
    
    return (nodes, edges)




# Calculates amendments
def calc_amendment(_id):
    the_law = mongo.db.laws.find_one({'law_id' : _id})
    amendments = the_law['amendments']
    count_dict = {}
    for amendment in amendments:
        for token in amendment.split():
            if token.isnumeric() and len(token) > 3:
                if token not in count_dict.keys():
                    count_dict[token] = 1
                else:
                    count_dict[token] += 1
    if count_dict == None:
        return None
    else:
        return count_dict, the_law['title']