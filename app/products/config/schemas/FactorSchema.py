import decimal
import uuid
from marshmallow import Schema, fields, validate, ValidationError

from ..data import constants


class PrimitiveTypeField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str) or isinstance(value, float) or isinstance(value, int) or isinstance(value, bool):
            return value
        else:
            raise ValidationError('Field should be str, float, int, or bool')


class Config_FactorVariabilityRuleSchema(Schema):
    uuid = fields.UUID(default=uuid.uuid4())
    field = fields.String(required=True)
    comparison = fields.String(
        required=True, validate=validate.OneOf(constants.OPERATOR_CODES))
    value = PrimitiveTypeField(required=False)
    lower = fields.Float(required=False)
    upper = fields.Float(required=False)


class Config_FactorVariabilityRuleListSchema(Schema):
    rules = fields.List(fields.Nested(
        Config_FactorVariabilityRuleSchema), required=True)
    factor_value = fields.Float(required=True)


class Config_FactorSchema(Schema):
    uuid = fields.UUID(default=uuid.uuid4())
    default_factor_value = fields.Float(default=1.0)
    variability = fields.List(fields.Nested(
        Config_FactorVariabilityRuleListSchema), required=False)
