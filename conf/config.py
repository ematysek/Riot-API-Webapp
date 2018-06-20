import json
import os

DEFAULT_CONFIG_LOCATION = "conf/config.json"
global_conf = None
DEFAULT_LOGGER_CONFIG_LOCATION = "conf/logger.json"
logger_conf = None


def load_config(config_location=None):
    # TODO add support for env variables
    # Base Config
    conf_location = config_location or DEFAULT_CONFIG_LOCATION
    if not os.path.isfile(conf_location):
        print("Could not find config file in {}".format(conf_location))
        exit()
    with open(conf_location, 'r') as conf_file:
        j = json.load(conf_file)
        global global_conf
        global_conf = j

    # Logger Config
    logger_conf_location = DEFAULT_LOGGER_CONFIG_LOCATION
    if not os.path.isfile(logger_conf_location):
        print("Could not find logger config file in {}".format(logger_conf_location))
        exit()
    with open(logger_conf_location, 'r') as logger_conf_file:
        k = json.load(logger_conf_file)
        global logger_conf
        logger_conf = k


def get_logger_config():
    return logger_conf


class Config:

    def __init__(self):
        self.__conf = global_conf

    def get_property(self, property_name):
        return self.__conf.get(property_name)


class APIConfig(Config):

    @property
    def api_endpoint(self):
        return self.get_api_conf().get('endpoint')

    @property
    def api_key(self):
        return self.get_api_conf().get('key')

    def get_api_conf(self):
        return self.get_property('api')


class DBConfig(Config):

    def get_db_conf(self):
        return self.get_property('db')

    @property
    def db_file(self):
        return self.get_db_conf().get('db_file')
