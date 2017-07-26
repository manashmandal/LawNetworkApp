from flask import Blueprint
from app import mongo

INNER_LAW_NETWORK = mongo.db.network # This network collection contains the relationship between named entities and sections
LAW_NETWORK = "" # Outer law network, which cites which one
LAWS = mongo.db.laws # Containes the law texts

api = Blueprint('api', __name__)



from . import routes