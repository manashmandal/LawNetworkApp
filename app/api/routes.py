from app import mongo
from . import (api, LAW_NETWORK, INNER_LAW_NETWORK, LAWS)
from flask_login import login_required
from flask import request

# Returns the connection [Main Connection]
@api.route('/api/connection', methods=['GET'])
# @login_required
def get_law_connection():
    law_id = request.args.get('id')
    return "Connnection %s" % str(law_id)


# Amendment data
@api.route('/api/amendments', methods=['GET'])
def get_amendment_detail():
    pass



# Inner law details, connection between entities and sections 
@api.route('/api/law_detail', methods=['GET'])
def get_law_detial():
    pass


# Returns law text in a formatted manner 
@api.route('/api/law_text', methods=['GET'])
def get_law_text():
    pass

