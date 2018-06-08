import logging
import logging.handlers
import riot_request
import db_request
# import os
import json

configFile = 'config.json'
configData = json.load(open(configFile))

apiEndpoint = configData["api"]["endpoint"]
apiKey = configData["api"]["key"]

db = configData["mysql"]["db"]
dbUsername = configData["mysql"]["user"]
dbPassword = configData["mysql"]["password"]


def main():
    # initialize logger and logger config
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler("logs/riot_app.log")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info('Completed logger setup')

    logger.info('initializing riot_request.riotconnector')
    rc = riot_request.RiotConnector(apiEndpoint, apiKey)

    dr = db_request.DBConnector(dbUsername, dbPassword, db)

    dr.close()


if __name__ == '__main__':
    main()
