import json
import logging
import uuid

from base.model import BaseClass, BaseModel, Entity
from repository.mongodb import MongoDb

from openapi_server.models.base_model_ import Model

ID_ATTRIBUTE = 'id'
ID_ATTRIBUTE_MONGO = '_id'

class MongoDbCollection(BaseClass):

    def __init__(self, name, clazz):
        super().__init__()

        self.collection_name = name
        self.clazz = None

        if issubclass(type(clazz), Model) or issubclass(type(clazz), Entity) or issubclass(type(clazz), BaseModel):
            self.clazz = clazz
        else:
            logging.error("collection class must inherit from {} or {}. provided class {} does not comply.".format(Model, BaseModel, clazz))

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return { 'name': self.collection_name, 'clazz': str(self.object_type()) }

    def object_type(self):
        return type(self.clazz)

    def find(self, mongodb):
        collection = self._get_collection(mongodb)

        if not collection:
            logging.warning("no collection '{}' found".format(self.collection_name))
            return []

        objects = []
        for obj in collection.find():
            objects.append(self.clazz.from_dict(obj))
    
        return objects
    
    def find_one(self, mongodb, id):
        return self.find_one_for_attribute(mongodb, ID_ATTRIBUTE, id)

    def find_one_for_attribute(self, mongodb, attribute, id):
        collection = self._get_collection(mongodb)

        if not collection:
            logging.warning("no collection '{}' found".format(self.collection_name))
            return []
        
        obj = collection.find_one({attribute : id})

        if obj:
            return self.clazz.from_dict(obj)
        
        return None

    def find_for_attributes(self, mongodb, attributes):
        collection = self._get_collection(mongodb)

        if not collection:
            logging.warning("no collection '{}' found. returing None".format(self.collection_name))
            return []

        entities = []
        for obj in collection.find(attributes):
            entities.append(self.clazz.from_dict(obj))

        return entities
    
    def delete_one(self, mongodb, id):
        collection = self._get_collection(mongodb)

        if not collection:
            logging.warning("no collection '{}' found".format(self.collection_name))
            return []
        
        collection.delete_one({ID_ATTRIBUTE : id})

    def insert_one(self, mongodb, objekt):
        collection = self._get_collection(mongodb)

        if not collection:
            logging.warning("no collection '{}' found".format(self.collection_name))
            return []
        
        if not objekt:
            logging.error("object of type 'Model' expected. provided object is None")
            return None

        if not isinstance(objekt, type(self.clazz)):
            logging.error("object of type '{}' expected. provided type {} is not supported".format(type(self.clazz), type(object)))
            return None
        
        objekt_dict = objekt.to_dict()

        if ID_ATTRIBUTE in objekt_dict and objekt_dict[ID_ATTRIBUTE]:
            logging.error("attribute {} must not be provided when inserting a new object. not inserting object {}".format(ID_ATTRIBUTE, objekt_dict))
            return None

        id = _create_id()
        objekt_dict[ID_ATTRIBUTE] = id
        objekt_dict[ID_ATTRIBUTE_MONGO] = id
        
        collection.insert_one(objekt_dict)

        return id
      
    def insert_one_with_id(self, mongodb, objekt):
        collection = self._get_collection(mongodb)

        if not collection:
            logging.warning("no collection '{}' found".format(self.collection_name))
            return []
        
        if not objekt:
            logging.error("object of type 'Model' expected. provided object is None")
            return None

        if not isinstance(objekt, type(self.clazz)):
            logging.error("object of type '{}' expected. provided type {} is not supported".format(type(self.clazz), type(object)))
            return None

        objekt_dict = objekt.to_dict()
        objekt_dict[ID_ATTRIBUTE_MONGO] = _create_id()
        
        collection.insert_one(objekt_dict)

    def save(self, mongodb, objekt, mongodb_id=None):
        collection = self._get_collection(mongodb)

        if not collection:
            logging.warning("no collection '{}' found".format(self.collection_name))
            return []
        
        if not objekt:
            logging.error("object of type 'Model' expected. provided object is None")
            return None

        if not isinstance(objekt, type(self.clazz)):
            logging.error("object of type '{}' expected. provided type {} is not supported".format(type(self.clazz), type(object)))
            return None

        objekt_dict = objekt.to_dict()

        if mongodb_id:
            objekt_dict['_id'] = mongodb_id
        
        logging.debug("COLLECTION SAVE objekt.to_dict() {}".format(objekt.to_dict()))

        collection.save(objekt_dict)

    def _get_collection(self, mongodb):
        if mongodb:
            if isinstance(mongodb, MongoDb):
                db = mongodb.get_db()
                return db[self.collection_name]
            else:
                logging.error("provided mongodb reference not matching expected type {}. actual type: {}".format(MongoDb, str(type(MongoDbCollection))))
        else:
            logging.error("provided mongodb reference is None")

        return None

def _create_id():
    return str(uuid.uuid4())