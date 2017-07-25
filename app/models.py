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
    print("CALLED USERLOADER")
    user_record = mongo.db.users.find_one({'username' : username})
    if user_record is not None:
        user = User(username)
        user.username = user_record['username']
        user.password = user_record['password']
        return user
    return None

