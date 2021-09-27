from base.model import Entity
from util.timestamp import LocalizedTimeStamp

class EntitySchema(Entity):

    def __init__(self, job_id, name, schema, sample):
        super().__init__()
        
        self['id'] = name
        self['schema'] = schema
        self['sample'] = sample
        self['job_id'] = job_id
        self['status'] = 'created'
        self['created_at'] = LocalizedTimeStamp.now_utc().isoformat()
