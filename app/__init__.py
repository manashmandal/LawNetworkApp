from flask import Flask, render_template
from config import config
from flask_pymongo import PyMongo
from flask_login import LoginManager


mongo = PyMongo()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initializing the addons
    mongo.init_app(app, config_prefix='MONGO')
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .viz import viz as viz_blueprint
    app.register_blueprint(viz_blueprint)

    return app