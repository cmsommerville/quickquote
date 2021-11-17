import decimal
from typing_extensions import Required
from marshmallow import Schema, fields, validate, ValidationError

from ..data import constants


class PrimitiveTypeField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str) or isinstance(value, float) or isinstance(value, int) or isinstance(value, bool):
            return value
        else:
            raise ValidationError('Field should be str, float, int, or bool')


class Config_FactorVariabilityRuleSchema(Schema):
    field = fields.String(required=True)
    comparison = fields.String(
        required=True, validate=validate.OneOf(constants.OPERATOR_CODES))
    value = PrimitiveTypeField(required=False)
    lower = fields.Decimal(5, required=False)
    upper = fields.Decimal(5, required=False)


class Config_FactorVariabilityRuleListSchema(Schema):
    rules = fields.List(fields.Nested(Config_FactorVariabilityRuleSchema))
    factor_value = fields.Decimal(constants.FACTOR_PRECISION)


class Config_FactorSchema(Schema):
    default_factor_value = fields.Decimal(
        constants.FACTOR_PRECISION, default=1.0)
    variability = fields.List(fields.Nested(
        Config_FactorVariabilityRuleListSchema))
