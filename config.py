from pymongo import MongoClient



class Config:
    WTF_CSRF_ENABLED = True
    SECRET_KEY = "hello"
    DB_NAME = "lawviz"
    PORT = 27017
    HOST = 'localhost'
    DATABASE = MongoClient(HOST, PORT)[DB_NAME]
    USERS_COLLECTION = DATABASE.users

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development' : DevelopmentConfig
}
