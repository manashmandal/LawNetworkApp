from app import mongo
# from . import api, AVAILABLE_LAW_KEYS, LAW_COUNT
from . import api
from flask_login import (login_required, current_user)
from flask import request
from ..backend.search import (_search, build_main_network_connection, make_section_entity_network, calc_amendment)
from ..backend.search_v2 import search_laws
import json
from flask import jsonify
from flask_api import status
import time
from ..models import UserStatSchema
#from spacy.lang.en.stop_words import STOP_WORDS


# INNER_LAW_NETWORK = mongo.db.network # This network collection contains the relationship between named entities and sections
# LAW_NETWORK = "" # Outer law network, which cites which one
# LAWS = mongo.db.laws # Containes the law texts
# USERS = mongo.db.users

LAW_COUNT = 705

AVAILABLE_LAW_KEYS = {
        "amendments" : 1,
        "subtitle" : 2,
        "title" : 3,
        "chapters" : 4,
        "volume" : 5,
        "section_details" : 6,
        "date" : 7,
        "preamble" : 8 
} 


# Returns the connection [Main Connection]
@api.route('/api/connection', methods=['GET'])
# @login_required
def get_law_connection():
    law_id = request.args.get('id')
    return "Connnection %s" % str(mongo.db.users.find_one({'username' : 'manash'}))


# Amendment data
@api.route('/api/amendments', methods=['GET'])
def get_amendment_detail():
    _id = int(request.args.get('id', 1))

    if (_id > 704):
        _id = 1

    amendments, title = calc_amendment(_id)
    return jsonify({
        'id' : _id,
        'amendments' : amendments,
        'title' : title
    })


# Law Inner Details
"""
Types: 
1. Phrase <-> Section : ps/sp
2. Phrase <-> Entity : pe/ep
3. Entity <-> Section : es/se
"""
@api.route('/api/law_inner_detail/phrase_entity', methods=['GET'])
def get_phrase_entity_network():
    _id = int(request.args.get('id', 344))
    nodes, edges, _map = make_section_entity_network(_id)

    return jsonify({
        'id' : _id,
        'nodes' : nodes,
        'edges' : edges,
        'map' : _map
    })


@api.route('/api/law_inner_detail', methods=['GET'])
def get_law_inner_detail():
    _id = int(request.args.get('id', 344))
    _type = str(request.args.get('type', 'ps'))

    # If Phrase <-> Section Network is needed
    if _type == 'ps' or _type == 'sp':
        pass

    # If Entity <-> Section Network is Needed
    elif _type == 'pe' or _type == 'ep':
        details = mongo.db.network.find_one({'law_id' : _id})

        edges = []
        nodes = []
        # edges = [
        #     {'from' : e['from'], 'to' : e['to'] } for e in details['edges'] if e['title'] == 'Organization'  
        # ]
        from_nodes = []
        to_nodes = []

        for d in details['edges']:
            if (len(d['title']) < 15):
                # print(d['title'])
                edges.append({'from' : d['from'], 'to' : d['to']})
                from_nodes.append(d['from'])
                to_nodes.append(d['to'])
                nodes.append(d['from'])
                nodes.append(d['to'])


        print("NODE COUNT : {}".format(len(list(set(nodes)))))

        return jsonify({
            'connection-type' : 'phrase-entity',
            'edges' : edges,
            'nodes' : details['nodes']
        })


        print(edges)
    
    # ends_to = len([e['to'] for e in edges])
    # begins_from = len([e['from'] for e in edges])

    # print("CONNECTIONS BEGINS FROM {} NODES AND ENDS TO {} AND TOTAL CONNECTION {}".format(begins_from, ends_to, len(edges)))

    inner_details = mongo.db.network.find_one({'law_id' : _id})
    return jsonify({
        'nodes' : inner_details['nodes'],
        'edges' : inner_details['edges'],
        'id' : _id
    })


# Inner law details, connection between entities and sections 
"""
Available Keys:
    1. amendments
    2. subtitle
    3. title
    4. chapters
    5. volume
    6. section_details
    7. date
    8. preamble
"""
@api.route('/api/law_detail', methods=['GET'])
def get_law_detail():
    law_id = int(request.args.get('id'))
    key = str(request.args.get('key', default="title"))

    # Checking key validity
    try:
        idx = AVAILABLE_LAW_KEYS[key]
    except KeyError:
        return {"error" : "you entered an invalid key", "valid_keys" : list(AVAILABLE_LAW_KEYS.keys()) }

    if law_id > 0 and law_id < LAW_COUNT:
        detail = mongo.db.laws.find_one({'law_id' : law_id })
        return jsonify({
            key : detail[key],
            'law_id' : law_id
        })
    
    else:
        return {"error" : "the law doesn't exist currently"}


# Get all detail 
@api.route('/api/law_detail/all', methods=['GET'])
def get_all_law_detail():
    law_id = int(request.args.get('id'))

    # Checking key validity
    if law_id > 0 and law_id < LAW_COUNT:
        detail = mongo.db.laws.find_one({'law_id' : law_id })
        detail['_id'] = law_id
        return jsonify({
            'detail' : detail,
            'law_id' : law_id
        })
    
    else:
        return {"error" : "the law doesn't exist currently"}



# Returns the connected nodes
@api.route('/api/connected_laws', methods=['GET']) 
def get_connected_laws():
    law_id = int(request.args.get('id'))

    connections = mongo.db.citations.find_one({'node' : law_id})['links']

    print("COnnection type : {}".format(type(connections)))

    return jsonify({
        'source' : law_id,
        'connections' : connections
    })


# Returns law text in a formatted manner 
@api.route('/api/law_text', methods=['GET'])
def get_law_text():
    pass

@api.route('/api/edge_detail', methods=['GET'])
def get_connection_detail():
    source_id = int(request.args.get('s'))
    destination_id = int(request.args.get('d'))
    # detail = mongo.db.edge_detail.find_one({'source' : source_id, 'destination' : destination_id})
    # detail = mongo.db.citation_details_v2.find_one({'source' : source_id, 'destination' : destination_id})
    # Upgrade with citation keywords
    detail = mongo.db.citation_details_with_keywords.find_one({ 'source' : source_id, 'destination' : destination_id })

    if detail != None:
        return jsonify({
            'source' : source_id,
            'destination' : destination_id,
            'detail' : detail['details']
        })

    error = {"error" : "connection does not exist"}

    return jsonify(error), status.HTTP_404_NOT_FOUND


# API Route for Searching laws
@api.route('/api/search_law', methods=['GET'])
def search_law():
    import codecs
    query = str(request.args.get('q'))

    #print("Type : {} - LENGTH : {}".format(type(query) , len(query) ))

    ngram = bool(int(request.args.get('ngram', default=False)))
    exclude_unigram = bool(int(request.args.get('exclude_unigram', default=True)))
    max_result = int(request.args.get('max', 30))

    print(max_result)

    # laws = _search(str(query), only_ngram_search=ngram, exclude_unigram=exclude_unigram)
    laws = search_laws(str(query), max_result=max_result)

    # Filtering size
    # TODO: REMOVE THIS WHEN WE CAN GET ALL LAWS FROM DATABASE
    # laws = [law for law in laws if law < 700]

    # print(laws)

    outer_network = build_main_network_connection(laws)

    id_title_map = { id : mongo.db.laws_v2.find_one({'law_id' : id})['title'] for id in laws }

    # Add coordinates 
    all_coordinates = mongo.db.law_embeddings.find_one()

    # print(all_coordinates)
    coords = []

    for law in laws:
        coords.append({'x' : all_coordinates[str(law)]['x'], 'y' : all_coordinates[str(law)]['y'], 'law_id' : str(law) })

    if (len(laws) == 0):
        return {"error" : "Nothing found"}, status.HTTP_404_NOT_FOUND

    return jsonify({
        'laws' : laws,
        'network' : outer_network,
        'id_title_map' : id_title_map,
        'coords' : coords
    })



# API for Saving User stat

## Single click data
@api.route('/api/userstat/law_single_click', methods=['GET'])
def law_single_click():
    if request.method == 'GET':
        username = request.args.get('user')
        node = int(request.args.get('node'))
        res = UserStatSchema.insert_law_node_single_click(username, node)

        if (res.acknowledged == True):
            return jsonify({"success" : "updated"})

    return jsonify({"error" : "update failed"}), status.HTTP_400_BAD_REQUEST

## Double click data 
@api.route('/api/userstat/law_double_click', methods=['GET'])
def law_double_click():
    if request.method == 'GET':
        node = int(request.args.get('node'))
        res = UserStatSchema.insert_law_node_double_click(node)

        if (res.acknowledged == True):
            return jsonify({"success" : "updated"})

    return jsonify({"error" : "update failed"}), status.HTTP_400_BAD_REQUEST

## Entered search term
@api.route('/api/userstat/law_search_term', methods=['GET'])
def law_search_term():
    if request.method == 'GET':
        term = request.args.get('term')
        res = UserStatSchema.insert_search_terms(term)

        if (res.acknowledged == True):
            return jsonify({"success" : "updated" })

    return jsonify({"error" : "update failed"}), status.HTTP_400_BAD_REQUEST


## Law Edge click term
@api.route('/api/userstat/law_edge_click', methods=['GET'])
def law_edge_click():
    if request.method == 'GET':
        _from = int(request.args.get('f'))
        _to = int(request.args.get('t'))
        res = UserStatSchema.insert_edge_click({'from' : _from, 'to' : _to})
        if (res.acknowledged == True):
            return jsonify({"success" : "updated" })

    return jsonify({"error" : "update failed"}), status.HTTP_400_BAD_REQUEST

## Inner node click term
@api.route('/api/userstat/inner_node_click', methods=['GET'])
def law_inner_node_click():
    if request.method == 'GET':
        title = request.args.get('title')
        law_id = int(request.args.get('law'))
        res = UserStatSchema.insert_inner_node_click({'title' : title, 'law_id' : law_id})
        if (res.acknowledged == True):
            return jsonify({"success" : "updated" })

    return jsonify({"error" : "update failed"}), status.HTTP_400_BAD_REQUEST





# API for test purpose
@api.route('/api/test', methods=['GET'])
def testapi():
    count = int(request.args.get('count', 5))
    begin_time = time.time()
    for i in range(1, count +1):
        id = i % 704 + 1
        
        print(id)
        q = mongo.db.laws.find_one({'law_id' : id})
        # print(q['title'])
    end_time = time.time()

    return {
        "time_taken" : end_time - begin_time
    }



# WordCloud API
@api.route('/api/wordcloud', methods=['GET'])
def get_word_cloud():
    section_key = str(request.args.get('key'))
    law_id = str(request.args.get('id', '1'))

    try:
        cld = mongo.db.wordcloud.find_one({'law_id' : law_id })[law_id][section_key]
    except:
        cld = None
    print(cld)

    # Clean up the data [removing stop words]
    for word_dict in cld['words']:
        if word_dict['word'] in STOP_WORDS:
            cld['words'].remove(word_dict)

    # print(len(cld))

    return {
        "info" : cld
    }

# Get list of sections
@api.route('/api/section_titles', methods=['GET'])
def get_section_keys():
    _id = int(request.args.get('id', 1))
    section_keys = [key for key in mongo.db.laws.find_one({'law_id' : _id})['section_details']]
    return {
        'section_keys' : section_keys
    }
    

# Returns entity group of a given law id 
@api.route('/api/entity', methods=['GET'])
def get_entity():
    _id = int(request.args.get('id', 1))

    if (_id > 704):
        _id = 1

    entity_group = mongo.db.entities.find_one({'law_id' : _id})['entity_group']

    entity_token_group_dict = {}

    for ent in entity_group:
        entity_token_group_dict[ent[0]] = ent[1]

    organizations = list(set([ent[0] for ent in entity_group if ent[1] == 'ORGANIZATION']))
    locations = list(set([ent[0] for ent in entity_group if ent[1] == 'LOCATION']))
    dates = list(set([ent[0] for ent in entity_group if ent[1] == 'DATE']))
    persons = list(set([ent[0] for ent in entity_group if ent[1] == 'PERSON']))
    
    print(entity_token_group_dict)

    return {
        "organizations" : organizations,
        "locations" : locations,
        "dates" : dates,
        "persons" : persons
    }
    # return {
    #     'entities' : entity_token_group_dict
    # }