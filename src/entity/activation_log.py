from base.model import Entity
from util.timestamp import LocalizedTimeStamp

class ActivationLog(Entity):

    def __init__(self, job_id, process_id, voucher, phone, crop, timestamp, pixel, latitude, longitude):
        super().__init__()
        
        self['voucher_no'] = voucher
        self['phone_no'] = phone

        self['crop'] = crop
        self['timestamp'] = timestamp
        self['pixel'] = pixel
        self['latitude'] = latitude
        self['longitude'] = longitude

        self['job_id'] = job_id
        self['process_id'] = process_id
        self['status'] = 'created'
        self['message'] = None
        self['created_at'] = LocalizedTimeStamp.now_utc().isoformat()
