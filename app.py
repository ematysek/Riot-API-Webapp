import logging
import logging.handlers
import json
from request_handler import RequestHandler


def main():
    # TODO Create init_configs function
    # TODO Create config files for loggers
    configFile = 'config.json'
    configData = json.load(open(configFile))

    apiEndpoint = configData["api"]["endpoint"]
    apiKey = configData["api"]["key"]

    # initialize logger and logger config
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler("logs/riot_app.log")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info('Completed logger setup')

    sql_logger = logging.getLogger('sqlalchemy.engine')
    sql_logger.setLevel(logging.INFO)
    sql_logger.addHandler(handler)

    logger.info('Initializing RequestHandler')
    rh = RequestHandler(apiEndpoint, apiKey, 'riot.db')

    # Proof of concept
    rh.insert_or_update_summoner('chowdog')
    accid = rh.get_accountid_by_name('chowdog')
    rh.update_recent_usermatches(accid)


if __name__ == '__main__':
    main()
