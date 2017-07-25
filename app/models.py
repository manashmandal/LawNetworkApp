from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager



class User():
    def __init__(self, username):
        self.username = username


    def get_username(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)