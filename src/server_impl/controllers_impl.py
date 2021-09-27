import datetime
import logging
import sys

from pathlib import Path

from base.model import BaseClass, BaseModel, Entity, MongoDbEntityCollection

from openapi.model_store import OpenApiModelStore
from openapi.request import get_api_version
from openapi.response import Response, HTTP_GET_OK, HTTP_POST_CREATED

from engine.policy_application import PolicyApplicationProcess
from process.business_log import BusinessTransactionLogHandler

from entity.constants import CROPS
from entity.application import Application
from entity.policy import Policy
from entity.policy_template import GroupPolicyTemplate

from tenant.tenant_manager import TenantManager
from util.timestamp import LocalDate, LocalizedTimeStamp
from util.geo import latitude_longitude_to_pixel

from objectstore.bucket import Bucket
from repository.mongodb_collection import MongoDbCollection

import openapi_server.models

from openapi_server.models.activation import Activation
from openapi_server.models.component import Component
from openapi_server.models.config import Config
from openapi_server.models.payment import Payment
from openapi_server.models.planting_window import PlantingWindow

from openapi_server.models.arc2_cache import Arc2Cache
from openapi_server.models.arc2_rainfall import Arc2Rainfall

COLLECTION_ACTIVATIONS = "activations"
COLLECTION_PAYMENTS = "payments"
COLLECTION_POLICIES = "policies"

COLLECTION_PRODUCT_CONFIGS = "group_policy_templates"

STATUS_PROCESSING = "PROCESSING"

class ActivationsController_impl(OpenApiModelStore):

    collection = MongoDbCollection(COLLECTION_ACTIVATIONS, Activation())

    @staticmethod
    def activations_get(tenant, env):
        logging.info("tenant: {}, environment: {}, api version: {}".format(
            tenant, env, 
            get_api_version()))
        
        return OpenApiModelStore.get(
            TenantManager.get_mongodb(tenant, env), 
            ActivationsController_impl.collection)

    @staticmethod
    def activations_event_id_get(tenant, event_id, env):
        return OpenApiModelStore.get_id(
            TenantManager.get_mongodb(tenant, env), 
            ActivationsController_impl.collection, 
            event_id)

    @staticmethod
    def activations_planting_window_get(tenant, env, reference_date, crop, latitude, longitude):
        logging.info("tenant: {}, environment: {}, api version: {}".format(
            tenant, env, 
            get_api_version()))

        pixel = latitude_longitude_to_pixel(latitude, longitude)
        attributes = { 
                'crop': crop, 
                'location': pixel,
            }
        
        date_ref = LocalDate.from_compact(reference_date).toordinal()

        logging.info("query attributes {}".format(attributes))
        logging.info("query date {}, lat/lng {}/{}".format(reference_date, latitude, longitude))

        # check aginst actuarial ground truth (site table derived info)
        # group_policy_templates {crop:"Maize", location: "Pixel405559"}
        mongodb = TenantManager.get_mongodb(tenant, env)
        product_configs_collection = MongoDbEntityCollection(COLLECTION_PRODUCT_CONFIGS, GroupPolicyTemplate)
        product_configs = product_configs_collection.find_for_attributes(mongodb, attributes)        

        logging.info("product configs. count {}, data {}".format(len(product_configs), '<lots of data>'))

        # TODO date_tolerance: grace period for activations needs to be globally configurable and not buried in some arbitrary class ...
        date_tolerance = 14
        init_min = LocalDate.from_compact('30000101').toordinal()
        init_max = LocalDate.from_compact('19000101').toordinal()

        date_min = init_min
        date_max = init_max

        backup_min = init_min
        backup_max = init_max

        global_min = init_min
        global_max = init_max

        for product_config in product_configs:
            swc = product_config['sow_window_configuration']
            date_from = LocalDate.from_custom(swc['start_date'], '%d.%m.%Y').toordinal()
            date_to = LocalDate.from_custom(swc['end_date'], '%d.%m.%Y').toordinal()

            global_min = min(date_from, global_min)
            global_max = max(date_to, global_max)

            # exact match with activation window
            if date_ref >= date_from and date_ref <= date_to:
                date_min = min(date_from, date_min)
                date_max = max(date_to, date_max)
            
            # upcoming activation window
            elif date_ref <= date_to:
                date_max = max(date_to, date_max)

            # special case if too early inside tolerance
            if date_ref + date_tolerance >= date_from and date_ref <= date_to:
                backup_min = min(date_from, backup_min)
            
            # special case if too late inside tolerance
            if date_ref - date_tolerance <= date_to and date_ref >= date_from:
                backup_min = min(date_from, backup_min)
                backup_max = max(date_to, backup_max)

        # clean case, inside activation windows
        if date_min < init_min and date_max > init_max:
            return PlantingWindow(
                crop, pixel, 
                LocalDate.to_compact(LocalDate.from_ordinal(date_min)), 
                LocalDate.to_compact(LocalDate.from_ordinal(date_max)))

        # special case too early but inside tolerance
        if backup_min < init_min and backup_max == init_max:
            return PlantingWindow(
                crop, pixel, 
                LocalDate.to_compact(LocalDate.from_ordinal(backup_min)), 
                LocalDate.to_compact(LocalDate.from_ordinal(global_max)))

        # special case too late but inside tolerance
        if backup_min < init_min and backup_max > init_max:
            return PlantingWindow(
                crop, pixel, 
                LocalDate.to_compact(LocalDate.from_ordinal(backup_min)), 
                LocalDate.to_compact(LocalDate.from_ordinal(backup_max)))

        # error case too early/too late
        if date_ref < global_min:
            return Response.http_get_bad_request('{} {} activation too early'.format(
                LocalDate.to_compact(LocalDate.from_ordinal(global_min)), 
                LocalDate.to_compact(LocalDate.from_ordinal(global_max))),
                None)

        else:
            return Response.http_get_bad_request('{} {} activation too late'.format(
                LocalDate.to_compact(LocalDate.from_ordinal(global_min)), 
                LocalDate.to_compact(LocalDate.from_ordinal(global_max))),
                None)


    @staticmethod
    def activations_post(tenant, env, activation):
        mongodb = TenantManager.get_mongodb(tenant, env)

        # TODO try to find a reason why storing the activation cannot be done in the policy application process
        # in case no such reason pops up move it there (activation id might be precomputed and returned if is_valid == True)
        # store activation
        activation_id, http_status = OpenApiModelStore.post(
            mongodb, 
            ActivationsController_impl.collection, 
            activation)

        # reject activation if persisting fails
        if http_status != HTTP_POST_CREATED:
            validation_message = "failed to store activation, see log"
            logging.warning(validation_message)
            return Response.http_get_bad_request(validation_message, Activation)

        # validate activation data to find matching product config
        activation.id = activation_id
        is_valid, validation_message, product_config = Application.validate(mongodb, activation)

        # create business process
        application_process = PolicyApplicationProcess(
            PolicyApplicationProcess.create_tx_id(), 
            BusinessTransactionLogHandler(mongodb), 
            mongodb, 
            activation,
            is_valid,
            validation_message,
            product_config,
            raise_exception = True)

        # asynchronous start of process
        application_process.start()        

        if not is_valid:
            logging.warning(validation_message)
            return Response.http_get_bad_request(validation_message, Activation)

        return Response.http_post_created(activation.id)


class PaymentsController_impl(OpenApiModelStore):

    collection = MongoDbCollection(COLLECTION_PAYMENTS, Payment())

    @staticmethod
    def payments_get(tenant, env):
        return OpenApiModelStore.get(
            TenantManager.get_mongodb(tenant, env), 
            PaymentsController_impl.collection)

    @staticmethod
    def payments_event_id_get(tenant, event_id, env):
        return OpenApiModelStore.get_id(
            TenantManager.get_mongodb(tenant, env), 
            PaymentsController_impl.collection, 
            event_id)

    @staticmethod
    def payments_post(tenant, env, obj):
        return OpenApiModelStore.post(
            TenantManager.get_mongodb(tenant, env), 
            PaymentsController_impl.collection, 
            obj)


class PoliciesController_impl(BaseClass):

    collection = MongoDbCollection(COLLECTION_POLICIES, Policy())

    @staticmethod
    def policies_get(tenant, env, phone_no, status):
        logging.info("tenant: {}, environment: {}, api version: {}".format(
            tenant, env, 
            get_api_version()))

        mongodb = TenantManager.get_mongodb(tenant, env)

        attributes = {}

        if phone_no:
            attributes['phone_no'] = phone_no

        if status:
            attributes['meta.status'] = status
                
        policies = PoliciesController_impl.collection.find_for_attributes(mongodb, attributes)
        
        logging.info("query attributes {}".format(attributes))
        logging.info("resulting policies {}".format(policies))

        result = []

        for policy in policies:
            order_no = policy['order_no']
            phone_no = policy['phone_no']
            status = policy['meta']['status']

            result.append(openapi_server.models.policy.Policy(
                order_no, phone_no, status))

        return result

    @staticmethod
    def policies_order_no_get(tenant, order_no, env):
        logging.info("tenant: {}, environment: {}, api version: {}".format(
            tenant, env, 
            get_api_version()))

        mongodb = TenantManager.get_mongodb(tenant, env)
        attributes = { 
                'order_no': order_no
            }
                
        policies = PoliciesController_impl.collection.find_for_attributes(mongodb, attributes)
        
        logging.debug("query attributes {}".format(attributes))
        logging.debug("resulting policies {}".format(policies))

        if len(policies) == 0:
            return Response.http_get_not_found('no policy found for ther order number provided', order_no, None)

        if len(policies) > 1:
            return Response.http_get_bad_request('multiple policies found for order number {}'.format(order_no), None)

        policy = policies[0]
        order_no = policy['order_no']
        phone_no = policy['phone_no']
        funding_end_date = None
        status = policy['meta']['status']
        crop = policy['crop']
        location = policy['location']['name']
        sum_insured = Policy.MAX_PAYOUT_FACTOR * policy['premium_amount']
        begin_date = policy['begin_date']
        end_date = policy['end_date']

        return openapi_server.models.policy_info.PolicyInfo(
            order_no, phone_no, funding_end_date, status,
            crop, location, sum_insured, begin_date, end_date
        )


    @staticmethod
    def policies_order_no_claims_get(tenant, order_no, env):
        logging.info("tenant: {}, environment: {}, api version: {}".format(
            tenant, env, 
            get_api_version()))

        mongodb = TenantManager.get_mongodb(tenant, env)
        attributes = { 
                'order_no': order_no
            }
                
        policies = PoliciesController_impl.collection.find_for_attributes(mongodb, attributes)
        
        logging.info("query attributes {}".format(attributes))

        if len(policies) == 0:
            return Response.http_get_not_found('no policy found for ther order number provided', order_no, None)

        if len(policies) > 1:
            return Response.http_get_bad_request('multiple policies found for order number {}'.format(order_no), None)

        policy = policies[0]
        claims = []
        for claim in policy['claims']:
            claims.append(openapi_server.models.Claim(
                sequence_no=claim['no'], 
                name=claim['name'], 
                amount=claim['amount'], 
                status=claim['status']))
        
        return claims


class Arc2Controller_impl(BaseClass):

    @staticmethod
    def arc2_rainfall_get(tenant, location, date_begin_str, days, env):
        arc2 = TenantManager.get_arc2(tenant, env)
        date_begin = LocalDate.from_compact(date_begin_str)
        date_begin_ordinal = date_begin.toordinal()
        days = int(days)

        date_end_str = LocalDate.to_compact(date_begin + datetime.timedelta(days=int(days - 1)))
        status_code, url, encoding, rainfall = arc2.rainfall(location, date_begin_ordinal, days)
        
        return {
            'status': status_code,
            'url': url,
            'date_begin': date_begin_str,
            'date_end': date_end_str,
            'days': days,
            'data': Arc2Controller_impl._text_to_list(rainfall)
        }

    @staticmethod
    def arc2_cache_get(tenant, date_begin_str, days, env):
        arc2 = TenantManager.get_arc2(tenant, env)
        date_begin = LocalDate.from_compact(date_begin_str)
        days = int(days)

        date_end_str = LocalDate.to_compact(date_begin + datetime.timedelta(days=int(days - 1)))
        status_code, url, encoding, cache, ftp = arc2.cache(date_begin, days)
        
        return {
            'status': status_code,
            'url': url,
            'date_begin': date_begin_str,
            'date_end': date_end_str,
            'days': days,
            'cache': Arc2Controller_impl._text_to_list(cache),
            'source': ftp
        }

    @staticmethod
    def _text_to_list(text):
        if text.endswith('\n'):
            text = text[:-1]

        return text.split('\n')



class AdminController_impl(BaseClass):

    @staticmethod
    def config_get(tenant, env):
        return TenantManager.get_config(tenant, env)

    @staticmethod
    def config_post(tenant, env, config):
        return TenantManager.set_config(tenant, env, config)

