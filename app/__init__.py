from flask import Flask, render_template
from config import config
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_api import FlaskAPI


mongo = PyMongo()
login_manager = LoginManager()
# flask_api = FlaskAPI()

def create_app(config_name):
    app = FlaskAPI(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.jinja_env.auto_reload = True

    # Initializing the addons
    mongo.init_app(app)
    login_manager.init_app(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .viz import viz as viz_blueprint
    app.register_blueprint(viz_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app