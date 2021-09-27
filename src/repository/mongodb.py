import json
import logging

from pymongo import MongoClient

class MongoDb(object):

    def __init__(self, host, port, timeout, db_name, access_key, secret_key):
        super().__init__()

        self.host = host
        self.port = port
        self.timeout = timeout

        self.db_name = db_name
        self.access_key = access_key
        self.secret_key = secret_key

        self.client = MongoClient(host = "{0}:{1:.0f}".format(host, port), serverSelectionTimeoutMS = timeout)
        self.db = self.client[db_name]
    
    def __repr__(self):
        return json.dumps(self.to_dict())
    
    def to_dict(self):
        return {
            "host": self.host,
            "port": self.port,
            "db": self.db_name
        }

    def value(self, attribute):
        if attribute == 'host':
            return self.host
        elif attribute == 'port':
            return self.port
        elif attribute == 'timeout':
            return self.timeout
        elif attribute == 'db_name':
            return self.db_name
        elif attribute == 'access_key':
            return self.access_key
        elif attribute == 'secret_key':
            return self.secret_key
        
    def get_db(self):
        return self.db
    
    def get_client(self):
        return self.client

    def drop_collection(self, collection_name):
        logging.info("dropping collection {} from db {}".format(collection_name, self.db_name))
        self.db.drop_collection(collection_name)
