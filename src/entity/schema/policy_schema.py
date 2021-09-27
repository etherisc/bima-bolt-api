from entity.constants import CROPS, ACTIVATION_WINDOWS, PHONE_NO_PATTERN, ORDER_NO_PATTERN, SEASON_PATTERN

from entity.schema.location_schema import LocationSample
from entity.schema.payment_schema import PaymentSample
from entity.schema.claim_position_schema import ClaimPositionSample
from entity.schema.meta_schema import MetaSample

PolicySample = {
    "id": "254720754321-LR2021-A100687-0521",
    "application_id": "b181845b-4c10-406a-943a-26f773bc08a1",
    "group_policy_id": "BimaPima.LR2021.Maize.5.Pixel389568",
    "order_no": "A100687-0521",
    "phone_no": "254720754321",
    "begin_date": "2021-03-31",
    "end_date": "2021-08-11",
    "season": "LR2021",
    "crop": "Maize",
    "activation_window": "5",
    "location": LocationSample,
    "premium_amount": 50, # TODO decide if this should go to a method (=sum of premium payments)
    "sum_insured_amount": 500, # TODO decide if this should go to a method (=premium amount * 10.0)
    "payments": [ PaymentSample ],
    "claims": [ ClaimPositionSample ], 
    "meta" : MetaSample
}

PolicySchema = {
    "$id": "policy.schema.json",
    "type" : "object",
    "properties" : {
        "id" : {
            "description": "policy business key: phone_no-season-order_no", 
            "type" : "string",
            "minLength": 3,
            "maxLength": 64,
        },
        "application_id" : {
            "type" : "string",
            "format": "uuid",
        },
        "group_policy_id" : {
            "description": "reference to group policy", 
            "type" : "string",
            "minLength": 4,
            "maxLength": 64,
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
        "begin_date" : {
            "anyOf": [
                {
                    "type": "string",
                    "pattern": "^20[0-9]{2}-[0-9]{2}-[0-9]{2}$"
                },
                {
                    "type": "null"
                }
            ]
        },
        "end_date" : {
            "anyOf": [
                {
                    "type": "string",
                    "pattern": "^20[0-9]{2}-[0-9]{2}-[0-9]{2}$"
                },
                {
                    "type": "null"
                }
            ]
        },
        "season" : {
            "type" : "string",
            "pattern" : SEASON_PATTERN
        },
        "crop" : {
            "type" : "string",
            "enum" : CROPS
        },
        "activation_window" : {
            "type" : "string",
            "enum" : ACTIVATION_WINDOWS
        },
        "location" : {
            "type" : "object",
            "$ref": "location.schema.json"
        },
        "premium_amount" : {
            "type": "number",
            "minimum": 0
        },
        "sum_insured_amount" : {
            "type": "number",
            "minimum": 0
        },
        "payments" : {
            "type" : "array",
            "items" : {
                "type" : "object",
                "$ref": "payment.schema.json"
            },
            "minItems": 1,
            "uniqueItems": True
        },
        "claims" : {
            "type" : "array",
            "items" : {
                "type" : "object",
                "$ref": "claim_position.schema.json"
            },
            "minItems": 5,
            "maxItems": 5,
            "uniqueItems": True
        },
        "meta" : {
            "type" : "object",
            "$ref": "meta.schema.json"
        },
    },
    "required": [ "id", "application_id", "group_policy_id", "order_no", "phone_no", "begin_date", "end_date", "season", "crop", "activation_window", "location", "premium_amount", "sum_insured_amount", "payments", "claims", "meta" ]
}
