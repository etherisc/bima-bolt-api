from entity.constants import PHONE_NO_PATTERN
from entity.schema.location_schema import LocationSample

ActivationSample = {
    "voucher_no": "A100687-0521",
    "phone_no": "254720754321",
    "location": LocationSample,
    "timestamp": "2021-05-19T10:30:07.000+00:00",
}

ActivationSchema = {
    "$id": "activation.schema.json",
    "type" : "object",
    "voucher_no" : {
        "description": "corresponds to the voucher number of the policy activation", 
        "type" : "string",
        "minLength": 3,
        "maxLength": 64,
    },
    "phone_no" : {
        "type" : "string",
        "pattern": PHONE_NO_PATTERN,
    },
    "location" : {
        "type" : "object",
        "$ref": "location.schema.json"
    },
    "timestamp" : {
        "type" : "string",
        "format": "date-time",
    },
    "required": [ "voucher_no", "phone_no", "location", "timestamp" ]
}
