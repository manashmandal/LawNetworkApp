from pymongo import MongoClient



class Config:
    WTF_CSRF_ENABLED = True
    SECRET_KEY = "hello"

    MONGO_DBNAME = "law"
    MONGO_HOST = "localhost"
    MONGO_PORT = 27017


    TEMPLATES_AUTO_RELOAD = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development' : DevelopmentConfig
}
