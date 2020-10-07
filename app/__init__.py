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

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from .api.resource_routes import register_resource_routes
    register_resource_routes(app)

    from .middleware import Middleware
    app.wsgi_app = Middleware(app.wsgi_app)

    return app
