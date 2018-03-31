from app import mongo
from flask import jsonify, request
from . import api


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
