from app import mongo
from flask import jsonify, request
from . import api


@api.route('/api/routes_v2_test', methods=['GET'])
def routes_v2_testing():
    return jsonify({
        'success' : 'jsonify done'
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
                    'detail' : item['detail']
                })
            else:
                sections.append({
                    'title' : item['title'],
                    'detail' : item['detail']
                })

    # sections = [ {item['title'] : item['detail']} for item in all_sections if item['id'] in section_ids ]


    return jsonify({
        'related_sections' : sections
    })
