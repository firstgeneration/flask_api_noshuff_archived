from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_name):
    config_object = config[config_name]
    app = Flask(__name__)
    app.config.from_object(config_object)
    config_object.init_app(app)
    db.init_app(app)

    if config_name in ['development']:
        CORS(app)

    from .api import api, authentication as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')
    api.init_app(app)

    from app.api.permissions import permission_manager
    api.permission_manager(permission_manager)

    return app
