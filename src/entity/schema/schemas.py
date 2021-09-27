
import json

from jsonschema import RefResolver, Draft7Validator, FormatChecker

from entity.schema.activation_schema import ActivationSchema
from entity.schema.application_schema import ApplicationSchema
from entity.schema.sow_window_schema import SowWindowSchema
from entity.schema.crop_stage_schema import CropStageSchema
from entity.schema.group_policy_schema import GroupPolicySchema
from entity.schema.location_schema import LocationSchema
from entity.schema.meta_schema import MetaSchema
from entity.schema.payment_schema import PaymentSchema
from entity.schema.claim_position_schema import ClaimPositionSchema
from entity.schema.policy_schema import PolicySchema

ID = '$id'
SCHEMA_STORE = {
    ActivationSchema[ID]: ActivationSchema,
    ApplicationSchema[ID]: ApplicationSchema,
    SowWindowSchema[ID]: SowWindowSchema,
    CropStageSchema[ID]: CropStageSchema,
    GroupPolicySchema[ID]: GroupPolicySchema,
    LocationSchema[ID]: LocationSchema,
    MetaSchema[ID]: MetaSchema,
    PaymentSchema[ID]: PaymentSchema,
    PolicySchema[ID]: PolicySchema,
    ClaimPositionSchema[ID]: ClaimPositionSchema,
}

def validate_object(obj, schema):
    resolver = RefResolver.from_schema(PolicySchema, store=SCHEMA_STORE)
    validator = Draft7Validator(schema, resolver=resolver, format_checker=FormatChecker())

    validator.validate(obj)

    return obj