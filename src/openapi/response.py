from openapi_server.models.not_found_response import NotFoundResponse
from openapi_server.models.bad_request_response import BadRequestResponse

HTTP_GET_OK = 200
HTTP_GET_BAD_REQUEST = 400
HTTP_GET_NOT_FOUND = 404

HTTP_POST_OK = 200
HTTP_POST_CREATED = 201
HTTP_POST_BAD_REQUEST = 400

# PATCH: 200 OK
# DELETE: 204 No Content

class Response:

    @staticmethod
    def http_get_ok(element):
        return element, HTTP_GET_OK
    
    @staticmethod
    def http_get_not_found(message, id, typ):
        return NotFoundResponse(message, id, str(typ)), HTTP_GET_NOT_FOUND
    
    @staticmethod
    def http_get_bad_request(message, typ):
        return BadRequestResponse(message, str(typ)), HTTP_GET_BAD_REQUEST

    @staticmethod
    def http_post_ok(id):
        return id, HTTP_POST_OK

    @staticmethod
    def http_post_created(id):
        return id, HTTP_POST_CREATED
    
    @staticmethod
    def http_post_bad_request(message, typ):
        return BadRequestResponse(message, str(typ)), HTTP_POST_BAD_REQUEST
