PaymentSample = {
    "order_no": "A100687-0521",
    "phone_no": "254720754321",
    "transaction_no": "xCiKXQqnH4SeXh747",
    "amount": 50,
    "timestamp": "2021-05-19T10:30:07.000+00:00",
}

PaymentSchema = {
    "$id": "payment.schema.json",
    "type" : "object",
    "order_no" : {
        "description": "corresponds to the voucher number of the policy activation", 
        "type" : "string",
        "minLength": 3,
        "maxLength": 64,
    },
    "phone_no" : {
        "type" : "string",
        "minLength": 10,
        "maxLength": 15,
    },
    "timestamp" : {
        "type" : "string",
        "format": "date-time",
    },
    "transaction_no" : {
        "type" : "string",
        "minLength": 5,
        "maxLength": 32,
    },
    "amount" : {
        "type": "number",
        "minimum": 0
    },
    "required": [ "order_no", "phone_no", "timestamp", "transaction_no", "amount" ]
}
