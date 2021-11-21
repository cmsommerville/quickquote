import decimal
import uuid
from marshmallow import Schema, fields, validate, ValidationError
from ..data import constants


class StringOrBooleanField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str) or isinstance(value, bool):
            return value
        else:
            raise ValidationError('Field should be str or bool')


class Config_CoverageUISchema(Schema):
    section = fields.String(
        default="main", validate=validate.OneOf(constants.UI_SECTIONS))
    default = StringOrBooleanField(required=True)


class Config_CoverageSchema(Schema):
    code = fields.String(required=True)
    label = fields.String(required=True)
    uuid = fields.UUID(default=uuid.uuid4())
    ui = fields.Nested(Config_CoverageUISchema, required=True)
