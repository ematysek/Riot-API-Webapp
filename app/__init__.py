from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from app.default_conf import Config, init_env
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(default_configs=Config):
    init_env()
    new_app = Flask(__name__)

    # Load configs
    new_app.config.from_object(default_configs)

    # Init flask extensions
    db.init_app(new_app)
    migrate.init_app(new_app, db)

    return new_app


# Import down here to avoid circular dependency
# import app.flask_models
