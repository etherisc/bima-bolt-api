import configparser
import pymongo

# https://docs.python.org/3/library/configparser.html
config = configparser.ConfigParser()
config.read('config.readonly.ini')

mongodb_host = config['mongodb']['host']
mongodb_port = config['mongodb']['port']
mongodb_timeout = int(config['mongodb']['timeout_ms'])
mongodb_uri = '%s:%s' % (mongodb_host, mongodb_port)

client = pymongo.MongoClient(host = mongodb_uri, serverSelectionTimeoutMS = mongodb_timeout)
print("connected to mongodb. uri='%s' with timeout [ms] %i" % (mongodb_uri, mongodb_timeout))
# print(client.server_info())

dbs = client.list_database_names()
print ("mongo databases: %s" % dbs)

if 'ussd_events' in dbs:
    db  = client['ussd_events']
    collections = db.list_collection_names()
    print ("collections for databases 'ussd_events': %s" % collections)
