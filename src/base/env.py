import logging
import os

ENV_DB_HOST = "DB_HOST"
ENV_DB_PORT = "DB_PORT"
ENV_DB_NAME = "DB_NAME"
ENV_DB_ACCESS_KEY = "DB_ACCESS_KEY"
ENV_DB_ACCESS_SECRET = "DB_ACCESS_SECRET"
ENV_DB_TIMEOUT = "DB_TIMEOUT"

logging.getLogger(__name__).addHandler(logging.NullHandler())


def env(variable, default_value=None):
    if variable in os.environ:
        return os.environ[variable]
    elif default_value != None:
        logging.warning("environment variable {} not defined. using default value: '{}'".format(variable, default_value))
        return default_value
    
    logging.error("environment variable {} not defined and no default defined".format(variable))
    raise EnvError("required environment variable {} not set. restart server with variable set".format(variable))


def env_int(variable, default_value):
    val = env(variable, default_value)

    if val:
        try:
            return int(val)
        except:
            logging.warning("failed to convert '{}' for variable {} to int value. using default value: {}".format(val, variable, default_value))
            return default_value

    logging.warning("environment variable {} not defined. using default value: {}".format(variable, default_value))
    return default_value


class EnvError(Exception):

    def __init__(self, value): 
        self.value = value
    
    def __str__(self): 
        return "Error: {}".format(self.value)
