from marshmallow import Schema, fields, validate, ValidationError

from ..data import constants


class Config_StateSchema(Schema):
    code = fields.String(
        required=True, validate=validate.OneOf(constants.STATE_CODES))
    value = fields.String(required=True, validate=validate.OneOf(
        constants.STATE_APPLICABILITY_VALUES))
    effectiveDate = fields.Date(required=False)
    expiryDate = fields.Date(required=False)
