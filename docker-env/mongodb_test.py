import pymongo

host = 'localhost'
port = 3101
client = pymongo.MongoClient(host, port)
print("connected to mongodb at '%s' on port '%s'" % (host, port))

db = client.my_test
print("database '%s' created (or assigned)" % db.name)

collection = db.my_collection
print("collection '%s' created (or assigned)" % collection.name)
print("elements in collection: %i" % collection.count_documents({}))

print("inserting 3 items with attibute 'x'")
collection.insert_one({"x": 10})
collection.insert_one({"x": 8})
collection.insert_one({"x": 11})

print("items in collection: %i" % collection.count_documents({}))
print("sorted items on attribute 'x' in ascencing order")

for item in collection.find().sort('x', pymongo.ASCENDING):
    print(item)
