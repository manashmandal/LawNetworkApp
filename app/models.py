from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from . import mongo
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def is_active(self):
        return True

    @property
    def password(self):
        raise AttributeError("password is not readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_username(self):
        return self.username

    def get_id(self):
        return self.username

    def is_anonymous(self):
        return False

    @staticmethod
    def validate_login(password_hash, password):
        # return check_password_hash(password_hash, password)
        return password_hash == password

@login_manager.user_loader
def load_user(username):
    user_record = mongo.db.users.find_one({'username' : username})
    if user_record is not None:
        user = User(username)
        user.username = user_record['username']
        user.password = user_record['password']
        return user
    return None


# Schema
class UserStatSchema(object):
    Schema = {
        "username" : "",
        "law_node_single_click" : [],
        "law_node_double_click" : [],
        "search_terms" : [],
        "edge_click" : [],
        "inner_node_click" : [],
        "inner_edge_click" : []
    }

    @staticmethod
    def insert_law_node_single_click(username, data):
        mongo.db.userstat.update_one({'username' : username}, {'$push' : {'law_node_single_click' : data } })

    @staticmethod
    def insert_law_node_double_click(username, data):
        mongo.db.userstat.update_one({'username' : username}, {'$push' : {'law_node_double_click' : data }})
    
    @staticmethod
    def insert_search_terms(username, data):
        mongo.db.userstat.update_one({'username' : username}, {'$push' : {'search_terms' : data }})

    @staticmethod
    def insert_edge_click(username, data):
        mongo.db.userstat.update_one({'username' : username}, {'$push' : {'edge_click' : data}})

    @staticmethod
    def insert_inner_node_click(username, data):
        mongo.db.userstat.update_one({'username' : username}, {'$push' : {'inner_node_click' : data}})
    
    @staticmethod
    def insert_inner_edge_click(username, data):
        mongo.db.userstat.update_one({'username' : username}, {'$push' : {'inner_edge_click' : data }})

