from app import mongo
from flask import jsonify, request
from . import api
from ..backend.search_v2 import search_laws
from ..backend.search import build_main_network_connection
import numpy as np

@api.route('/api/related_edges', methods=['GET', 'POST'])
def get_related_edges():
    # Get query
    query = str(request.args.get('q'))
    
    # Max result 
    max_result = int(request.args.get('max', 30))
    
    # Get the keyword
    keyword = str(request.args.get('keyword'))
    
    # Find out the laws 
    laws = search_laws(str(query), max_result=max_result)

    # Build the network
    network = build_main_network_connection(laws)

    # Replace the key
    network = [ {'source' : n['from'], 'destination' : n['to']} for n in network ]

    # Search through the database
    citation_keywords = mongo.db.citation_details_with_keywords.aggregate([
        {"$match" :  { "$or" : network } },
        {"$project" : { "keywords" : "$details.section_keywords", "source" : "$source", "destination" : "$destination", "_id" : 0 }}
    ])

    citation_keywords = list(citation_keywords)

    # Get keyword array
    keywords = [ck['keywords'][0] for ck in citation_keywords]

    # Find the indices to get the relevant laws
    in_key = np.array([ np.any(np.isin(key, [keyword])) for key in keywords ])

    data = [
        {'from' : d['source'], 'to' : d['destination'] } for d in np.array(citation_keywords)[in_key].tolist()
    ]

    return {
        'data' : data
    } 


@api.route('/api/routes_v2_test', methods=['GET'])
def routes_v2_testing():
    return jsonify({
        'success' : 'jsonify done'
    })

# Get a specific section based on law and section key
@api.route('/api/section_by_key', methods=['GET'])
def get_section_by_key():
    lawid = int(request.args.get('id'))
    sectionid = int(request.args.get('section'))

    law = mongo.db.law_details.find_one({'id' : str(lawid)})

    for section in law['sections']:
        if section['id'] == sectionid:
            return section
    
    return jsonify({
        "error" : "Section Key Does Not Exist"
    })


@api.route('/api/temp_search', methods=['GET'])
def temp_search():
    lawid = request.args.get('id')

    section_ids = mongo.db.temp_search.find_one()['search_result']['law_related_section_map'][str(lawid)]

    all_sections = mongo.db.law_details.find_one({'id' : str(lawid)})['sections']

    sections = []

    for item in all_sections:
        if item['id'] in section_ids:
            if item['title'] == "":
                sections.append({
                    'title' : "TITLE NOT FOUND",
                    'detail' : item['detail'],
                    'section_id' :  item['id']
                })
            else:
                sections.append({
                    'title' : item['title'],
                    'detail' : item['detail'],
                    'section_id' :  item['id']
                })

    # sections = [ {item['title'] : item['detail']} for item in all_sections if item['id'] in section_ids ]


    return jsonify({
        'related_sections' : sections
    })
