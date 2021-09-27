from entity.constants import SEASON_PATTERN, CROPS, ACTIVATION_WINDOWS

from entity.schema.meta_schema import MetaSample
from entity.schema.location_schema import LocationSample
from entity.schema.sow_window_schema import SowWindowSample
from entity.schema.crop_stage_schema import CropStageSample

GroupPolicySample = {
    "id": "BimaPima.LR2021.Maize.5.Pixel389568",
    "season": "LR2021",
    "crop": "Maize",
    "activation_window": "5",
    "location": LocationSample,
    "sow_window": SowWindowSample,
    "begin_date": "2021-03-31",
    "end_date": "2021-08-11",
    "stages" : [
        CropStageSample
    ],
    "payout": {
        "hurdle": 0.15,
        "deductible": 0.15,
        "maximum": 1.0,
        "minimum": 0.0,
        "total": 0.03542857,
        "actual": 0.0,
    },
    "meta" : MetaSample
}

GroupPolicySchema = {
    "$id": "group_policy.schema.json",
    "type" : "object",
    "properties" : {
        "id" : {
            "type" : "string",
            "minLength": 4,
            "maxLength": 64,
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
        "sow_window" : {
            "type" : "object",
            "$ref": "sow_window.schema.json"
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
        "crop_stages" : {
            "type" : "array",
            "items" : {
                "type" : "object",
                "$ref": "crop_stage.schema.json"
            },
            "minItems": 5,
            "maxItems": 5,
            "uniqueItems": True
        },
        "payout" : {
            "type" : "object",
            "properties" : {
                "hurdle": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                },
                "deductible": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                },
                "total": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                },
                "maximum": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                },
                "minimum": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                },
                "actual": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                }
            }
        },
        "meta" : {
            "type" : "object",
            "$ref": "meta.schema.json"
        },
    },
    "required": [ "id", "season", "crop", "activation_window", "sow_window", "begin_date", "end_date", "payout", "meta" ]
}
