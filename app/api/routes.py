from app import mongo
# from . import api, AVAILABLE_LAW_KEYS, LAW_COUNT
from . import api
from flask_login import login_required
from flask import request
from ..backend.search import _search, build_main_network_connection
import json
from flask import jsonify
from flask_api import status

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
    pass



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
        return {"error" : "you entered an invalid key", "valid_keys" : AVAILABLE_LAW_KEYS.keys() }

    if law_id > 0 and law_id < LAW_COUNT:
        detail = mongo.db.laws.find_one({'law_id' : law_id })
        return jsonify({
            key : detail[key]
        })
    
    else:
        return {"error" : "the law doesn't exist currently"}



# Returns law text in a formatted manner 
@api.route('/api/law_text', methods=['GET'])
def get_law_text():
    pass

@api.route('/api/edge_detail', methods=['GET'])
def get_connection_detail():
    source_id = int(request.args.get('s'))
    destination_id = int(request.args.get('d'))
    detail = mongo.db.edge_detail.find_one({'source' : source_id, 'destination' : destination_id})

    if detail != None:
        return jsonify({
            'detail' : detail['details']
        })

    error = {"error" : "connection does not exist"}

    return jsonify(error), status.HTTP_404_NOT_FOUND


@api.route('/api/search_law', methods=['GET'])
def search_law():
    query = request.args.get('q')
    ngram = bool(int(request.args.get('ngram', default=False)))
    exclude_unigram = bool(int(request.args.get('exclude_unigram', default=True)))

    laws = _search(str(query), only_ngram_search=ngram, exclude_unigram=exclude_unigram)
    outer_network = build_main_network_connection(laws)

    return jsonify({
        'laws' : laws,
        'network' : outer_network
    })





