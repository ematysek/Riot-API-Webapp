import os
import logging
from flask.cli import load_dotenv

logger = logging.getLogger(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))


# load_dotenv(os.path.join(basedir, '.env'))
def init_env():
    if load_dotenv():
        logger.info("env files loaded")
        if logger.level == logging.DEBUG:
            for k, v in os.environ.items():
                logger.debug("{}: {}".format(k, v))
    else:
        logger.warning("env files NOT loaded")


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '9867eea89c294b9162dba0890b7dfb98'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
