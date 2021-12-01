from marshmallow import Schema, fields, validate, ValidationError, post_dump

from ..data import constants


class Config_StateSchema(Schema):
    code = fields.String(
        required=True, validate=validate.OneOf(constants.STATE_CODES))
    value = fields.String(required=True, validate=validate.OneOf(
        constants.APPLICABILITY_VALUES))
    effectiveDate = fields.DateTime(required=False)
    expiryDate = fields.DateTime(required=False)


class Config_StateListOrInheritSchema(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if value == 'inherit':
            return value
        elif isinstance(value, list):
            if all([isinstance(item, Config_StateSchema) for item in value]):
                return value
        else:
            raise ValidationError('Field should be a valid state or `inherit`')
