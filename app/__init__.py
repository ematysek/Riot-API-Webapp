from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from app.default_conf import Config
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(default_configs=Config):
    app = Flask(__name__)

    # Load configs
    app.config.from_object(default_configs)

    # Init flask extensions
    db.init_app(app)
    migrate.init_app(app, db)

    return app


import app.flask_models
