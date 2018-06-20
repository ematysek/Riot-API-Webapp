import logging
import logging.config
import os

from conf.config import load_config, get_logger_config
from ui.webui import launch
from util.request_handler import RequestHandler


def main():
    # Create logs dir if it doesn't exist
    if not os.path.exists('logs/'):
        os.mkdir('logs/')
    # TODO Create init_configs function
    # TODO Create config files for loggers
    load_config()

    logging.config.dictConfig(get_logger_config())

    # initialize logger
    logger = logging.getLogger(__name__)

    logger.info('Initializing RequestHandler')
    rh = RequestHandler()

    # Proof of concept
    rh.insert_or_update_summoner('wellthisisawkwrd')
    accid = rh.get_accountid_by_name('wellthisisawkwrd')
    rh.update_recent_usermatches(accid)

    launch()


if __name__ == '__main__':
    main()
