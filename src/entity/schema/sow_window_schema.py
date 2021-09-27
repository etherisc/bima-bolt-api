SowWindowSample = {
    "window": "1",
    "sow_date": "254720754321",
}

SowWindowSchema = {
    "$id": "sow_window.schema.json",
    "type" : "object",
    "window" : {
        "type": "string",
        "enum": ["1", "2"],
    },
    "sow_date" : {
        "type": "string",
        "pattern": "^20[0-9]{2}-[0-9]{2}-[0-9]{2}$"
    },
    "required": [ "window", "sow_date" ]
}
