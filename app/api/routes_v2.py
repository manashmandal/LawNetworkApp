from app import mongo
from flask import jsonify
from . import api


@api.route('/api/routes_v2_test', methods=['GET'])
def routes_v2_testing():
    return jsonify({
        'success' : 'jsonify done'
    })
