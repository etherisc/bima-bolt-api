from entity.constants import PHONE_NO_PATTERN, ORDER_NO_PATTERN, SEASON_PATTERN, CROPS, LOCATION_PATTERN

from entity.schema.meta_schema import MetaSample

ApplicationSample = {
    "id": "b181845b-4c10-406a-943a-26f773bc08a1",
    "order_no": "A100687-0521",
    "phone_no": "254720754321",
    "timestamp": "2021-03-23T14:20:10.712859+02:00",
    "crop": "Maize",
    "location": "Pixel404557",
    "amount": "500",
    "meta": MetaSample,
}

ApplicationSchema = {
    "$id": "application.schema.json",
    "type" : "object",
    "properties" : {
        "id" : {
            "type" : "string",
            "format": "uuid",
        },
        "activation_id" : {
            "type" : "string",
            "format": "uuid",
        },
        "order_no" : {
            "description": "order number from activation",
            "type" : "string",
            "pattern": ORDER_NO_PATTERN,
        },
        "phone_no" : {
            "type" : "string",
            "pattern": PHONE_NO_PATTERN,
        },
        "timestamp" : {
            "type" : "string",
            "format": "date-time",
        },
        "season" : {
            "type" : "string",
            "pattern": SEASON_PATTERN,
        },
        "crop" : {
           "anyOf": [
                {
                    "type" : "string",
                    "enum" : CROPS,
                },
                {
                    "type": "null"
                }
            ]        
        },
        "location" : {
           "anyOf": [
                {
                    "type" : "string",
                    "pattern": LOCATION_PATTERN,
                },
                {
                    "type": "null"
                }
            ]        
        },
        "amount" : {
            "type" : "number",
            "minimum": 0.0,
        },
        "meta" : {
            "type" : "object",
            "$ref": "meta.schema.json"
        },
    },
    "required": [ "id", "activation_id", "order_no", "phone_no", "timestamp", "season", "crop", "location", "amount", "meta" ]
}
