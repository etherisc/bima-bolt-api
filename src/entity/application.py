import logging
import uuid

from openapi_server.models.activation import Activation

from base.model import Entity, MongoDbEntityCollection
from repository.mongodb import MongoDb

from entity.constants import CROPS, APPLICATION_STATUS_UNDERWRITTEN, APPLICATION_STATUS_DECLINED
from entity.policy_template import GroupPolicyTemplate, ActivationWindow
from entity.schema.application_schema import ApplicationSchema
from entity.schema.schemas import validate_object

from util.geo import latitude_longitude_to_pixel
from util.timestamp import LocalizedTimeStamp

class Application(Entity):

    def __init__(self, business_tx_id, task_id, activation, is_valid, validation_message, product):
        super().__init__()

        logging.debug("creating application form activation {}".format(activation))
        logging.debug("is_valid {} validation_message {}".format(is_valid, validation_message))

        self['id'] = str(uuid.uuid4())
        self['activation_id'] = activation.id
        self['order_no'] = activation.order_number
        self['phone_no'] = activation.mobile_num
        self['timestamp'] = LocalizedTimeStamp.local_to_utc(activation.call_time).isoformat()

        self['season'] = Application.get_season(activation)
        self['crop'] = Application.get_crop(activation)
        self['location'] = Application.get_location(activation)
        self['amount'] = activation.amount_premium

        self['product_config_id'] = None

        if is_valid and product:
            self['product_config_id'] = product['id']
            self.update_meta(business_tx_id, task_id, APPLICATION_STATUS_UNDERWRITTEN, validation_message)
        else:
            self.update_meta(business_tx_id, task_id, APPLICATION_STATUS_DECLINED, validation_message)


    def update_meta(self, business_tx_id, task_id, status, comment):
        self['meta'] = {
            'business_tx_id': business_tx_id,
            'task_id': task_id,
            'status': status,
            'comment': comment,
            'created_at': LocalizedTimeStamp.now_utc().isoformat()
        }


    def to_schema(self):
        return validate_object(self, ApplicationSchema)


    @staticmethod
    def validate(mongodb: MongoDb, activation: Activation) -> (bool, str, GroupPolicyTemplate):

        # successful validation results in matching product_config
        product_config = None

        # make sure that for the order_no of this activation no application in state underwritten exists already
        application = Application.get_application(mongodb, activation)
        if application:
            return (False, "for order {} an underwritten application already exists with id {}".format(activation.order_number, application['id']), product_config)

        # reject activation with invalid/empty crop
        crop = Application.get_crop(activation)
        if not crop:
            return (False, "unsupported crop {}. valid crop list {}".format(activation.value_chain, CROPS), product_config)

        # reject activation with invalid/empty location
        location = Application.get_location(activation)
        if not location:
            return (False, "invalid location {}/{}".format(activation.latitude, activation.longitude), product_config)

        # reject activation without matching activation window
        timestamp = activation.call_time
        activation_window_id = Application.get_activation_window(mongodb, timestamp, crop)
        if not activation_window_id:
            return (False, "no matching activation window for timestamp {}, crop {}".format(timestamp, crop), product_config)

        # reject activation without matching product config
        product_config = Application.get_product_config(mongodb, activation_window_id, location)
        if not product_config:
            return (False, "no matching product config for crop {} activation window {} location {}".format(crop, activation_window_id, location), product_config)
        
        return (True, "validation successful", product_config)        


    @staticmethod
    def get_application(mongodb, activation):
        collection = MongoDbEntityCollection('applications', Application)
        query = {
            'order_no': activation.order_number,
            'meta.status': APPLICATION_STATUS_UNDERWRITTEN,
        }

        return collection.find_one(mongodb, query)


    @staticmethod
    def get_season(activation):
        call_time = activation.call_time
        if not call_time:
            return None

        if call_time.month < 6:
            return "LR{}".format(call_time.year)
        else:
            return "SR{}".format(call_time.year)


    @staticmethod
    def get_crop(activation):
        crop = activation.value_chain

        if crop not in CROPS:
            logging.warning("unsupported crop '{}' for activation {}".format(crop, activation))
            return None

        return crop


    @staticmethod
    def get_location(activation):
        try:
            return latitude_longitude_to_pixel(
                activation.latitude, 
                activation.longitude)
        except:
            logging.warning("invalid coordinates '{}/{}' for activation {}".format(activation.latitude, activation.longitude, activation))
            return None


    # TODO refactor when sales window processing is here (activation_window its own module? then move this there or to sales_window module)
    @staticmethod
    def get_activation_window(mongodb, timestamp, crop):
        activation_date = timestamp.date()
        window_2nd_prio = None

        collection = MongoDbEntityCollection('activation_windows', ActivationWindow)
        activation_windows = collection.find(mongodb)

        for window in activation_windows:
            logging.debug("checking window {} for a match".format(window))

            if window['crop'] != crop:
                continue
        
            activation_window_id = window['id']
            match = ActivationWindow.compare_date_with_window(activation_date, window)
            logging.debug("date {}, match typye {}".format(activation_date, match))

            if match == 1:
                logging.info('matching activation window found for {}/{}: {}'.format(activation_date, crop, activation_window_id))
                return activation_window_id

            elif match == 2:
                window_2nd_prio = activation_window_id

        if window_2nd_prio:
            logging.warning('fallback activation window found for {}/{}: {}'.format(activation_date, crop, window_2nd_prio))
        else:
            logging.error('failed to find activation window for {}/{}'.format(activation_date, crop))
        
        return window_2nd_prio

        return None


    @staticmethod
    def get_product_config(mongodb, activation_window_id, location):

        # create product_config key
        product, season, crop, activation_window = activation_window_id.split('.')
        product_config_key = '.'.join([product, season, crop, activation_window, location])

        logging.info("key parts {} {} {} {} {}".format(product, season, crop, activation_window, location))
        logging.info("checking activation_window_id {} product_config_key {}".format(activation_window_id, product_config_key))

        collection = MongoDbEntityCollection('group_policy_templates', GroupPolicyTemplate)

        return collection.find_one_for_id(mongodb, product_config_key)

