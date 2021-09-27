from simple_value_object import ValueObject

from entity.constants import crop_is_valid

class PhoneNo(ValueObject):
    def __init__(self, value):
        if len(value) not in [9, 12]:
            raise ValueError("invalid phone number '{}', expected number of digits: 9 or 12".format(value))
        
        if len(value) == 12 and value[:3] != '254':
            raise ValueError("invalid phone number '{}', 12 digit numbers expected to start with country code 354".format(value))

class Crop(ValueObject):
    def __init__(self, value):
        if not crop_is_valid(value):
            raise ValueError("invalid crop '{}'".format(value))

class Latitude(ValueObject):
    def __init__(self, value: float):
        if value < -40.0 or value > 40.0:
            raise ValueError("provided latitude {} outside expected range [-40.0 .. 40.0]".format(value))

class Longitude(ValueObject):
    def __init__(self, value: float):
        if value < -20.0 or value > 55.0:
            raise ValueError("provided longitude {} outside expected range [-20.0 .. 55.0]".format(value))
