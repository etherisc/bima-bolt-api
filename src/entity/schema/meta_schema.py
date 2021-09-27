from entity.constants import PROCESS_ID_PATTERN, META_STATUS

MetaSample = {
    "business_tx_id": "run-systemtest-20210708_051805",
    "task_id": "1",
    "status": "Completed",
    "created_at": '2021-06-21T19:25:45.712859+02:00',
}

MetaSchema = {
    "$id": "meta.schema.json",
    "type" : "object",
    "properties" : {
        "business_tx_id" : {
            "type" : "string",
            "pattern": PROCESS_ID_PATTERN,
            "minLength": 1,
            "maxLength": 64,
        },
        "task_id" : {
            "type" : "string",
            "pattern": PROCESS_ID_PATTERN,
            "minLength": 1,
            "maxLength": 64,
        },
        "status" : {
            "type" : "string",
            "enum" : META_STATUS
        },
        "comment" : {
            "type" : "string",
            "maxLength": 128,
        },
        "created_at" : {
            "type" : "string",
            "format": "date-time",
        },
        "completed_at" : {
            "type" : "string",
            "format": "date-time",
        },
    },
    "required": [ "business_tx_id", "task_id", "status", "created_at" ]
}
