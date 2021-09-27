import logging
import log4mongo

from logging.config import dictConfig
from log4mongo.handlers import MongoHandler

from base.env import ENV_DB_HOST,ENV_DB_PORT, ENV_DB_TIMEOUT, ENV_DB_NAME,ENV_DB_ACCESS_KEY, ENV_DB_ACCESS_SECRET
from base.env import env, env_int

# logging basiscs from https://towardsdatascience.com/logging-basics-in-python-d0db13e538f9
# logging config from https://flask.palletsprojects.com/en/2.0.x/logging/
# mongodb logging from https://github.com/log4mongo/log4mongo-python

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s %(module)s: %(message)s',
    }},
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'mongo': {
            'class': 'log4mongo.handlers.MongoHandler',
            'host': env(ENV_DB_HOST), 
            'port': env_int(ENV_DB_PORT, 3101), 
            'database_name': 'policy_engine_logs',
            'capped': True,
            'capped_size': 83886080, 
            'capped_max': 50000,
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'mongo']
    }
}

def configure_logging():
    dictConfig(LOGGING_CONFIG)
    logging.info("logging config: {}".format(LOGGING_CONFIG))
