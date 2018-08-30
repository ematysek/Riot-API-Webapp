import json
import os

DEFAULT_LOGGER_CONFIG_LOCATION = "conf/logger.json"


def load_logger_config(logger_conf_loc=None):
    logger_conf_location = logger_conf_loc or DEFAULT_LOGGER_CONFIG_LOCATION
    if not os.path.isfile(logger_conf_location):
        print("Could not find logger config file in {}".format(logger_conf_location))
        exit()
    with open(logger_conf_location, 'r') as logger_conf_file:
        return json.load(logger_conf_file)
