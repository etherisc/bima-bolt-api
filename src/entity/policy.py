import datetime
import json
import logging
import uuid

from base.model import BaseClass, Entity
from entity.schema.policy_schema import PolicySchema
from entity.schema.schemas import validate_object

from entity.constants import POLICY_STATUS_PENDING
from entity.constants import POSITION_STATUS_PENDING, POSITION_NO, POSITION_DEDUCTIBLE, POSITION_GERMINATION_DRY, POSITION_VEGETATION, POSITION_FLOWERING, POSITION_EXCESS_RAIN

from util.json_encoder import DateTimeEncoder
from util.geo import pixel_to_latitude_longitude
from util.timestamp import LocalizedTimeStamp

DATE_FORMAT = '{0:%Y-%m-%d}'

class Policy(Entity):

    # TODO needs to be fixed, value should come from voucher not from constant factor
    MAX_PAYOUT_FACTOR = 10.0

    # TODO needs to be fixed, value should come from site table not from constant factor
    HURDLE_MAX_VALUE = 0.15

    # TODO refactor to replace activation related data with application data (ie get rid of params phone_no, voucher_no, crop, location and make application mandatory)
    def __init__(self, *args):
        super().__init__()

        # default
        if len(args) in [5,7]:
            business_tx_id = args[0]
            task_id = args[1]
            phone_no = args[2]
            voucher_no = args[3]
            crop = args[4]
            application = None
            group_policy = None

            if len(args) == 7:
                application = args[5]
                group_policy = args[6]
        
        # should only be called by method from_dict
        elif len(args) == 0:
            return

        # should never happen
        else:
            logging.error("unsupported list for Policy constructor {}".format(args))
            return
    
    # def __init__(self, business_tx_id, task_id, phone_no, voucher_no, crop, application=None, group_policy=None):
    #     super().__init__()

        self['order_no'] = voucher_no
        self['phone_no'] = phone_no
        self['premium_amount'] = 0.0
        self['group_policy'] = group_policy
        self['payments'] = []
        self['claims'] = self._get_pending_claim_positions(business_tx_id)
        self['review_check'] = None

        if application:
            logging.info("add application data {}".format(application))
            self['application_id'] = application['id']
            self['order_no'] = application['order_no']
            self['phone_no'] = application['phone_no']
            self['season'] = application['season']
            self['crop'] = application['crop']

            self.add_payment(Payment(
                business_tx_id, 
                application['phone_no'], 
                application['order_no'], 
                None, 
                application['timestamp'], 
                application['amount']))
        else:
            # TODO this is a hack and needs to be removed
            self['application_id'] = "fa8e0ff5-ca2f-40fa-89f3-3d68e03d8121"
            self['season'] = "LR2021"
            self['crop'] = crop


        # TODO get rid of this additional state
        self['status'] = 'created'

        self.update_meta(business_tx_id, task_id, POLICY_STATUS_PENDING)

    def update_meta(self, business_tx_id, task_id, status):
        self['meta'] = {
            'business_tx_id': business_tx_id,
            'task_id': task_id,
            'status': status,
            'created_at': LocalizedTimeStamp.now_utc().isoformat()
        }

    def to_schema(self):

        group_policy = self['group_policy']
        group_policy_id = None
        begin_date = None
        end_date = None
        activation_window = None
        location = None

        if group_policy:
            group_policy_id = group_policy['id']
            begin_date = group_policy['begin_date']
            end_date = group_policy['end_date']
            activation_window = group_policy['activation_window']
            location = group_policy['location']

        obj = {
            Entity.MONGODB_ID: self[Entity.MONGODB_ID],
            'id': self.get_id(),
            'application_id': self['application_id'],
            'group_policy_id': group_policy_id,
            'phone_no': self['phone_no'],
            'order_no': self['order_no'],
            'season': self['season'],
            'crop': self['crop'],
            'activation_window':activation_window,
            'location': location,
            'begin_date': begin_date,
            'end_date': end_date,
            'premium_amount': self['premium_amount'],
            'sum_insured_amount': self.get_sum_insured(),
            'payments': self['payments'],
            'claims': self['claims'],
            'review_check': self['review_check'],
            'meta': self['meta'],
        }

        return validate_object(obj, PolicySchema)

    def get_id(self):
        id_full = "{}-{}-{}".format(self['phone_no'], self['season'], self['order_no'])
        id_cropped = id_full[:64]
        return id_cropped

    def get_sum_insured(self):
        return Policy.MAX_PAYOUT_FACTOR * self['premium_amount']
    
    def get_crop(self):
        if self['group_policy']:
            return self['group_policy']['crop']

        return None
    
    def get_activation_window(self):
        if self['group_policy']:
            return self['group_policy']['activation_window']
             
        return None
    
    def get_location(self):
        if self['group_policy']:
            return self['group_policy']['location']

        return None
    
    def get_activation_date(self):
        if self['activation']:
            return self['activation']['timestamp']
        else:
            return None
    
    def get_activation_date_formatted(self):
        return DATE_FORMAT.format(self.get_activation_date())
    
    def get_begin(self):
        if self['group_policy']:
            return datetime.datetime.fromordinal(self['group_policy']['begin_date'])
        else:
            return None
    
    def get_end(self):
        if self['group_policy']:
            return datetime.datetime.fromordinal(self['group_policy']['policy_end'])
        else:
            return None

    def _get_pending_claim_positions(self, business_tx_id):
        positions = []

        positions.append(ClaimPosition(POSITION_DEDUCTIBLE, business_tx_id))
        positions.append(ClaimPosition(POSITION_GERMINATION_DRY, business_tx_id))
        positions.append(ClaimPosition(POSITION_VEGETATION, business_tx_id))
        positions.append(ClaimPosition(POSITION_FLOWERING, business_tx_id))
        positions.append(ClaimPosition(POSITION_EXCESS_RAIN, business_tx_id))

        return positions

    def add_payment(self, payment):
        self['payments'].append(payment)
        self['premium_amount'] += payment['amount']

    def _phone_no_formatted(self):
        pn = self['phone_no']

        if not pn:
            return ''
        if len(pn) != 12:
            return pn
        
        return "'+{} {} {}'".format(pn[:3], pn[3:6], pn[6:])


class Activation(Entity):

    def __init__(self, job_id, phone_no, voucher_no, crop, location, timestamp):
        self['phone_no'] = phone_no
        self['voucher_no'] = voucher_no
        self['crop'] = crop
        self['location'] = location
        self['timestamp'] = timestamp
        (self['latitude'], self['longitude']) = pixel_to_latitude_longitude(location)

        self['job_id'] = job_id
        self['created_at'] = LocalizedTimeStamp.now_utc().isoformat()

class Payment(Entity):

    def __init__(self, business_tx_id, phone_no, order_no, transaction_no, timestamp, amount):
        self['phone_no'] = phone_no
        self['order_no'] = order_no
        self['transaction_no'] = transaction_no
        self['timestamp'] = timestamp
        self['amount'] = amount

        self['business_tx_id'] = business_tx_id
        self['created_at'] = LocalizedTimeStamp.now_utc().isoformat()

class ClaimPosition(Entity):

    def __init__(self, name, job_id):
        # super().__init__()

        self['no'] = POSITION_NO[name]
        self['name'] = name
        self['status'] = POSITION_STATUS_PENDING

        self['weight'] = None
        self['amount'] = None
        self['mpesa_tx'] = None
        self['blockchain_tx'] = None

        self['job_id'] = job_id
        self['created_at'] = LocalizedTimeStamp.now_utc().isoformat()
