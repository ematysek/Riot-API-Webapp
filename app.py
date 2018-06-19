import logging
import os
from logging.handlers import TimedRotatingFileHandler

from conf.config import load_config
from ui.webui import launch
from util.request_handler import RequestHandler


def main():
    # Create logs dir if it doesn't exist
    if not os.path.exists('logs/'):
        os.mkdir('logs/')
    # TODO Create init_configs function
    # TODO Create config files for loggers
    load_config()

    # initialize logger and logger config
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler("logs/riot_app.log", when='midnight', backupCount=7, utc=True)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info('Completed logger setup')

    # Set up sqlAlchemy logger
    sql_logger = logging.getLogger('sqlalchemy.engine')
    sql_logger.setLevel(logging.INFO)
    sql_logger.addHandler(handler)

    # Set up Flask access logger
    wsgi_logger = logging.getLogger('werkzeug')
    wsgi_logger.addHandler(handler)

    logger.info('Initializing RequestHandler')
    rh = RequestHandler()

    # Proof of concept
    rh.insert_or_update_summoner('wellthisisawkwrd')
    accid = rh.get_accountid_by_name('wellthisisawkwrd')
    rh.update_recent_usermatches(accid)

    launch(handler)


if __name__ == '__main__':
    main()
