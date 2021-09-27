from entity.constants import POSITION_ITEMS, POSITION_STATUS

ClaimPositionSample = {
    "no": "3",
    "name": "Vegetation",
    "weight": 0.125,
    "amount": 150,
    "status": "notarized",
    "mpesa_tx": "OB548CGCVB",
    "blockchain_tx": "0x07238314ca07a2a890526b27939079773d6515aea4bf4395c56f60395c33a298",
    "job_id": "run-policy-review-20210726_100638",
    "timestamp": "2021-07-26T10:12:43.000+00:00",
}

ClaimPositionSchema = {
    "$id": "claim_position.schema.json",
    "type" : "object",
    "no" : {
        "description": "sequence order of position", 
        "type": "string",
        "pattern": "[0-9]{1}"
    },
    "name" : {
        "description": "unique item name", 
        "type" : "string",
        "enum": POSITION_ITEMS,
    },
    "weight" : {
        "description": "multiplication factor for sum insured to obtain the amount of the claims position", 
        "type": "number",
        "minimum": -1.0,
        "maximum": 1.0,
    },
    "amount" : {
        "description": "payout amount for this position. might be positive (for claims) and negative (for deductible)", 
        "type": "number",
    },
    "status" : {
        "description": "current status of this position. used to make sure position is consitent with claims position state machine", 
        "type": "string",
        "enum": POSITION_STATUS,
    },
    "mpesa_tx" : {
        "description": "mpesa tx id of corresponding payout. only allowed if claim went through status 'PaidOut'", 
        "type": "string",
        "pattern": "/^0x([A-Z0-9]{10})$/"
    },
    "blockchain_tx" : {
        "description": "blockchain tx for notarization of this payout position. only allowed if position went through state 'PaidOut'", 
        "type": "string",
        "pattern": "/^0x([A-Fa-f0-9]{64})$/"
    },
    "job_id" : {
        "type" : "string",
        "pattern": "^[a-zA-Z0-9/\-\_.\:]*$",
        "minLength": 1,
        "maxLength": 64,
    },
    "created_at" : {
        "type" : "string",
        "format": "date-time",
    },
    "required": [ "no", "name", "amount", "status", "mpesa_tx", "blockchain_tx", "job_id", "created_at" ]
}
