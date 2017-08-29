from pymongo import MongoClient
import os


class Config:
    WTF_CSRF_ENABLED = True
    SECRET_KEY = "hello"

    MONGO_DBNAME = "law"
    MONGO_HOST = "localhost"
    MONGO_PORT = 27017
    MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')

    TEMPLATES_AUTO_RELOAD = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    MONGO_DBNAME = "law"
    MONGO_HOST = "ds123311.mlab.com"
    MONGO_PORT = 23311
    # Load from environment variable
    MONGO_USERNAME = "manash"
    MONGO_PASSWORD = "manash"


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
