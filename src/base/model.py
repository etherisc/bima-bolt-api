import datetime
import json
import logging
import uuid

from base.config import configure_logging
from repository.mongodb import MongoDb


class BaseClass(object):

    # set up logging
    logging.getLogger(__name__).addHandler(logging.NullHandler())
    configure_logging()

# inspired by
# https://stackoverflow.com/questions/2390827/how-to-properly-subclass-dict-and-override-getitem-setitem
class Entity(dict):

    MONGODB_ID = '_id'
    ID = 'id'

    DATE_POSTFIX = '_date'
    DATE_FORMAT = '%d.%m.%Y'
    
    def __init__(self, *args, **kwargs):

        id = str(uuid.uuid4())
        self[Entity.MONGODB_ID] = id

        if not Entity.ID in kwargs:
            self[Entity.ID] = id
        
        self.update(*args, **kwargs)

    def __getitem__(self, key):

        if not key in self:
            logging.warning("unknown attribute '{}'. returning None".format(key))
            return None
        
        return dict.__getitem__(self, key)

    def __setitem__(self, key, val):
        val_adapted = Entity.from_date(val, key)
        return dict.__setitem__(self, key, val_adapted)

    def __repr__(self):
        return json.dumps(self, cls=DateTimeEncoder)

    @property
    def id(self):
        return self[Entity.ID]

        
    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def to_dict(self):
        return self

    # helper method to compensate for not storing date values (mongodb does not work with dates, only datetimes)
    @staticmethod   
    def to_date(date_string):
        if not isinstance(date_string, str):
            logging.warning("helper method only supports conversion from str using format '{}'. returning None".format(Entity.DATE_FORMAT))
            return None
        else:
            return datetime.datetime.strptime(date_string, Entity.DATE_FORMAT).date()
    
    # helper method to compensate for not storing date values (mongodb does not work with dates, only datetimes)
    @staticmethod   
    def from_date(val, key=None):
        # mongodb does not work with dates 
        # -> 'hack': convert date to str and log a warning if attribute name does not end with '_date'
        if isinstance(val, datetime.date):
            if not isinstance(val, datetime.datetime):
                if key and not key.endswith(Entity.DATE_POSTFIX):
                    logging.warning("attribute names for dates should end with '{}'. attribute name '{}' does not comply".format(Entity.DATE_POSTFIX, key))
            
                return val.strftime(Entity.DATE_FORMAT)
            
        return val

    @staticmethod   
    def from_dict(new_data):

        entity = Entity()

        for k, v in new_data.items():
            entity[k] = v
        
        return entity


class MongoDbEntityCollection(object):

    def __init__(self, name, clazz):
        super().__init__()

        self.name = name
        self.clazz = None
        
        if issubclass(clazz, Entity):
            self.clazz = clazz
        else:
            logging.error("collection class must inherit from Entity. provided class {} does not comply".format(clazz))

        logging.debug("entity collection created. name {} clazz {}".format(self.name, self.clazz.__name__))

    def entity_type(self):
        self.clazz

    def find(self, mongodb):
        collection = self._get_collection(mongodb)

        if not collection:
            return []

        objects = []
        for obj in collection.find():
            obj_target = self.clazz.from_dict(obj)
            logging.debug("source type {} target type {} object {}".format(type(obj), type(obj_target), obj_target))
            objects.append(obj_target)
    
        return objects
    
    def find_one_for_id(self, mongodb, id):
        return self.find_one(mongodb, {Entity.ID: id})

    def find_one(self, mongodb, query):
        collection = self._get_collection(mongodb)

        if not collection:
            return None
        
        obj = collection.find_one(query)

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
      
    def insert_one(self, mongodb, objekt, to_schema=True):
        collection = self._get_collection(mongodb)

        if not collection:
            return None
        
        if not objekt:
            logging.error("object of type '{}' expected. provided object is None".format(self.clazz))
            return None

        if not isinstance(objekt, self.clazz):
            logging.error("object of type '{}'. provided type {} is not supported".format(self.clazz, type(objekt)))
            return None
        
        clazz = objekt.__class__
        if to_schema and hasattr(clazz, 'to_schema') and callable(getattr(clazz, 'to_schema')):
            collection.insert_one(objekt.to_schema())
        else:
            collection.insert_one(objekt)

        return objekt.id
      
    def replace_one_for_id(self, mongodb, id, objekt, to_schema=True):
        collection = self._get_collection(mongodb)

        if not collection:
            return None
        
        if not objekt:
            logging.error("object of type '{}' expected. provided object is None".format(self.clazz))
            return None

        if not isinstance(objekt, self.clazz):
            logging.error("object of type '{}'. provided type {} is not supported".format(self.clazz, type(objekt)))
            return None
        
        clazz = objekt.__class__
        if to_schema and hasattr(clazz, 'to_schema') and callable(getattr(clazz, 'to_schema')):
            logging.debug("replace one {}".format(objekt))
            collection.replace_one({Entity.ID: id}, objekt.to_schema())
        else:
            collection.replace_one({Entity.ID: id}, objekt)

        return objekt.id

    def _get_collection(self, mongodb):
        if mongodb:
            if isinstance(mongodb, MongoDb):
                db = mongodb.get_db()
                return db[self.name]
            else:
                logging.error("provided mongodb reference not matching expected type {}. actual type: {}".format(MongoDb, str(type(MongoDbEntityCollection))))
        else:
            logging.error("provided mongodb reference is None")

        return None


class BaseModel(BaseClass):

    MONGODB_ID = '_id'

    def __init__(self, model_id=None):
        super().__init__()

        id = str(uuid.uuid4())
        self.id = id
        self.data = {}
        self.data[BaseModel.MONGODB_ID] = id

        if model_id:
            self.id = model_id

    def __repr__(self):
        return json.dumps(self.to_dict(), cls=DateTimeEncoder)

    def assign(self, attribute, value):
        self.data[attribute] = value
    
    def value(self, attribute):
        if attribute in self.data:
            return self.data[attribute]
        else:
            return None
    
    def from_dict(self, data, model_id=None):
        if model_id:
            self.id= model_id
        
        if data:
            self.data = data

        return self
        
    def to_dict(self):
        return self.data


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime)or isinstance(z, datetime.date):
            return (str(z))
        else:
            try:
                return super().default(z)
            except Exception:
                logging.debug('failed to encode using "super().default(z)". using fallback to str(z). z: {} type: {}'.format(z, type(z)))
                return (str(z))