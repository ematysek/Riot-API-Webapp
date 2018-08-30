import logging.config
import os

from app import create_app
from conf.config import load_logger_config

# Create logs dir if it doesn't exist
if not os.path.exists('logs/'):
    os.mkdir('logs/')

logging.config.dictConfig(load_logger_config())

app = create_app()

app.logger.info("app created")
app.logger.info("debug: {}".format(app.debug))
app.logger.debug("secret key: {}".format(app.secret_key))

if __name__ == '__main__':
    app.run()
