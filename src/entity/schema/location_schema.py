from entity.constants import LOCATION_PATTERN

LocationSample = {
    "name": "Pixel404557",
    "latitude": 0.3,
    "longitude": 35.6,
}

LocationSchema = {
    "$id": "location.schema.json",
    "type" : "object",
    "properties" : {
        "name" : {
            "type" : "string",
            "pattern": LOCATION_PATTERN,
        },
        "latitude" : {
            "type": "number",
            "minimum": -40.0,
            "maximum": 40.0,
        },
        "longitude" : {
            "type": "number",
            "minimum": -20.0,
            "maximum": 55.0,
        },
    },
    "required": [ "name", "latitude", "longitude" ]
}
