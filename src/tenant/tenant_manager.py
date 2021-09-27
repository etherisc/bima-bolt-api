import datetime
import logging
import os

from openapi_server.models.config import Config

from base.env import ENV_DB_HOST,ENV_DB_PORT, ENV_DB_TIMEOUT, ENV_DB_NAME,ENV_DB_ACCESS_KEY, ENV_DB_ACCESS_SECRET
from base.env import env, env_int

from base.model import BaseClass, BaseModel

from openapi.model_store import OpenApiModelStore
from openapi.request import get_tenant, get_environment
from openapi.response import Response, HTTP_GET_OK

from objectstore.bucket import Bucket
from repository.mongodb import MongoDb
from repository.mongodb_collection import MongoDbCollection
from entity.arc2 import Arc2

from util.timestamp import LocalizedTimeStamp


TENANT_S3 = "s3"
TENANT_MONGO = "mongo"
TENANT_ARC2 = "arc2"

TENANT_CONFIGS = "configs"
TENANTS = "tenants"

# setup up logging handler


def get_tenant_key(tenant, env):
    if env:
        return "{}-{}".format(tenant, env)    
    return tenant

def get_mongo_key(tenant, env):
    key = get_tenant_key(tenant, env)
    return "{}.{}".format(key, TENANT_MONGO)

def get_s3_key(tenant, env):
    key = get_tenant_key(tenant, env)
    return "{}.{}".format(key, TENANT_S3)

def get_arc2_key(tenant, env):
    key = get_tenant_key(tenant, env)
    return "{}.{}".format(key, TENANT_ARC2)


class Tenant(BaseModel):

    def __init__(self, tenant_key=None, config_id=None): 
        super().__init__()

        self.assign("id", tenant_key)
        self.assign("config_id", config_id)
        self.assign("created_at", datetime.datetime.now())
        self.assign("modified_at", self.value("created_at"))


class TenantManager(BaseClass):

    # tenant manager persistence setup
    host = env(ENV_DB_HOST)
    port = env_int(ENV_DB_PORT, 27017)
    timeout = env_int(ENV_DB_TIMEOUT, 1000)
    db_name = env(ENV_DB_NAME)
    access_key = env(ENV_DB_ACCESS_KEY, "")
    secret_key = env(ENV_DB_ACCESS_SECRET, "")
    engine_db = MongoDb(host, port, timeout, db_name, access_key, secret_key)

    tenants_collection = MongoDbCollection(TENANTS, Tenant())
    configs_collection = MongoDbCollection(TENANT_CONFIGS, Config())

    cache = {}

    @staticmethod
    def set_db(host, port, timeout, db_name, access_key, secret_key):
        TenantManager.engine_db = MongoDb(host, port, timeout, db_name, access_key, secret_key)
    
    @staticmethod
    def set_config(tenant, env, config):
        key = get_tenant_key(tenant, env)
        db = TenantManager.engine_db

        timestamp = LocalizedTimeStamp.now_utc().isoformat()
        config.created_at = timestamp
        (config_id, status_code) = OpenApiModelStore.post(
            db, TenantManager.configs_collection, config)

        if status_code == 201:
            tenant_existing = TenantManager.tenants_collection.find_one(db, key)

            if not tenant_existing:
                tenant_new = Tenant(key, config_id)
                logging.info("set new tenant {} to {}".format(key, tenant_new))
                TenantManager.tenants_collection.insert_one_with_id(db, tenant_new)
            else:
                tenant_existing.assign("config_id", config_id)
                tenant_existing.assign("modified_at", timestamp)
                logging.info("update tenant {} to {}".format(key, tenant_existing))
                TenantManager.tenants_collection.save(db, tenant_existing)
            
            # remove cache entries to make sure that next request uses new/updated config
            mongo_key = get_mongo_key(tenant, env)
            if mongo_key in TenantManager.cache:
                del TenantManager.cache[mongo_key]

            s3_key = get_s3_key(tenant, env)
            if s3_key in TenantManager.cache:            
                del TenantManager.cache[s3_key]

            arc2_key = get_arc2_key(tenant, env)
            if arc2_key in TenantManager.cache:            
                del TenantManager.cache[arc2_key]

            return Response.http_post_created(key)

        return Response.http_post_bad_request("failed to set config for tenant key {}. see log".format(key), type(config))

    @staticmethod
    def get_config(tenant, env):
        key = get_tenant_key(tenant, env)
        return TenantManager.get_tenant_config(key)


    @staticmethod
    def get_tenant_config(key):
        db = TenantManager.engine_db
        logging.info("TENANT MANAGER DEBUG engine db {}".format(db))
        tenant = TenantManager.tenants_collection.find_one(db, key)

        if tenant:
            config_id = tenant.value("config_id")

            if config_id:
                return OpenApiModelStore.get_id(
                    db, TenantManager.configs_collection, config_id)
        
        return Response.http_get_not_found("no config stored for tenant key. provide a config first", key, Config)


    @staticmethod
    def get_host():
        return TenantManager.host


    @staticmethod
    def get_mongodb(tenant, env):
        key = get_tenant_key(tenant, env)
        mongokey = get_mongo_key(tenant, env)

        if mongokey in TenantManager.cache:
            return TenantManager.cache[mongokey]

        # create and cache mongodb from config
        (config, status) = TenantManager.get_config(tenant, env)

        if status != HTTP_GET_OK:
            return None
        
        if not config:
            return None
        
        logging.debug("CONFIG {}".format(config))
        m = config.mongo
        mongodb = MongoDb(m.host, m.port, m.timeout, m.resource, m.access_id, m.access_secret)
        TenantManager.cache[mongokey] = mongodb

        return mongodb


    @staticmethod
    def get_bucket(tenant, env):
        key = get_tenant_key(tenant, env)
        s3key = get_s3_key(tenant, env)

        if s3key in TenantManager.cache:
            return TenantManager.cache[s3key]

        # create and cache mongodb from config
        (config, status) = TenantManager.get_config(tenant, env)

        if status != HTTP_GET_OK:
            return None

        if not config:
            return None

        b = config.s3
        bucket = Bucket(b.host, b.port, b.resource, b.access_id, b.access_secret)
        TenantManager.cache[s3key] = bucket

        return bucket


    @staticmethod
    def get_arc2(tenant, env):
        key = get_tenant_key(tenant, env)
        arc2key = get_arc2_key(tenant, env)

        if arc2key in TenantManager.cache:
            return TenantManager.cache[arc2key]

        # create and cache mongodb from config
        (config, status) = TenantManager.get_config(tenant, env)

        if status != HTTP_GET_OK:
            return None
        
        if not config:
            return None
        
        logging.debug("CONFIG {}".format(config))
        m = config.arc2
        timeout_s = int(m.timeout/1000) 
        arc2 = Arc2(m.host, m.port, m.resource, timeout_s)
        TenantManager.cache[arc2key] = arc2

        return arc2
