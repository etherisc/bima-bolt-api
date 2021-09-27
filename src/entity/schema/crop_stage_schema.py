from entity.constants import STAGE_STATUS

CropStageSample = {
    "name": "VegetationDry",
    "weight": 0.25,
    "begin_date": "2021-03-15",
    "end_date": "2021-04-11",
    "days": 28,
    "block_length": 14,
    "block_step": 1,
    "blocks": 15,
    "loss_blocks": 1,
    "payout": 0.016666,
    "status": "Completed" 
}

CropStageSchema = {
    "$id": "crop_stage.schema.json",
    "type" : "object",
    "properties" : {
        "name" : {
            "type" : "string",
            "pattern": "^[a-zA-Z0-9/\-\_.\:]*$",
            "minLength": 1,
            "maxLength": 64,
        },
        "weight" : {
            "type": "number",
            "minimum": 0
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
        "days" : {
            "type": "number",
            "minimum": 1
        },
        "block_length" : {
            "type": "number",
            "minimum": 1
        },
        "block_step" : {
            "type": "number",
            "minimum": 1
        },
        "blocks" : {
            "type": "number",
            "minimum": 1
        },
        "loss_blocks" : {
            "type": "number",
            "minimum": 0
        },
        "payout" : {
            "type": "number",
            "minimum": 0
        },
        "status" : {
            "type" : "string",
            "enum" : STAGE_STATUS
        },
    },
    "required": [ "name", "weight", "begin_date", "end_date", "days", "blocks", "block_length", "block_step", "loss_blocks", "payout", "status" ]
}
