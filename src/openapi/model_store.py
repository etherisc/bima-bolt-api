import datetime
import logging

from base.model import BaseClass

from openapi.request import validate_request_host
from openapi.response import Response

from openapi_server.models.not_found_response import NotFoundResponse

class OpenApiModelStore(BaseClass):

    @staticmethod
    def get_id(db, collection, id):
        validate_request_host()

        if OpenApiModelStore._is_invalid(db, collection):
            return Response.http_get_bad_request("invalid db or collection, see log", collection.object_type())

        obj = collection.find_one(db, id)

        if obj:
            return Response.http_get_ok(obj)
            
        return Response.http_get_not_found("no object found for provided id", id, collection.object_type())

    @staticmethod
    def get(db, collection):
        validate_request_host()

        if OpenApiModelStore._is_invalid(db, collection):
            return Response.http_get_bad_request("invalid db or collection, see log", collection.object_type())
        
        return Response.http_get_ok(collection.find(db))

    @staticmethod
    def post(db, collection, obj):
        validate_request_host()

        if OpenApiModelStore._is_invalid(db, collection):
            return Response.http_post_bad_request("invalid db or collection, see log", collection.object_type())
        
        logging.info("attempting insert in collection {} obj {}".format(collection.collection_name, obj))
        inserted_id = collection.insert_one(db, obj)

        if inserted_id:
            return Response.http_post_created(inserted_id)
            
        return Response.http_post_bad_request("failed to add object, see log", collection.object_type())

    @staticmethod
    def _is_invalid(db, collection):
        if not db:
            logging.error("provided mongodb is None")
            return True
    
        if not collection:
            logging.error("provided collection is None")
            return True
    
        return False
