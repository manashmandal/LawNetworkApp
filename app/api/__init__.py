from flask import Blueprint

api = Blueprint('api', __name__)

from . import routes
from . import routes_v2
