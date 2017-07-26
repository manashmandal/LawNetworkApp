from . import *
from app import mongo

def get_edge_detail(source_id, destination_id):
    # Edge data
    edge_data = []

    # Getting law dictionary
    source = mongo.db.laws.find_one({'law_id': source_id})
    destination = mongo.db.laws.find_one({'law_id': destination_id})

    # This title will be searched through the law doc
    try:
        destination_title = destination['title'].lower()
    except:
        return []

    source_sections = source['section_details']

    for key in source_sections:
        if destination_title in source_sections[key].lower():
            edge_data.append(
                {
                    'section_title': key,
                    'section_detail': source_sections[key]
                }
            )
    return edge_data