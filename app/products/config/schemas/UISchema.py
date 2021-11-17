from marshmallow import Schema, fields, validate, ValidationError

from ..data import constants


class PrimitiveTypeField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str) or isinstance(value, float) or isinstance(value, int) or isinstance(value, bool):
            return value
        else:
            raise ValidationError('Field should be str, float, int, or bool')


class UI_TextField(Schema):
    component = fields.Constant("v-text-field")
    type = fields.String(
        default="input", validate=validate.OneOf(constants.UI_TEXT_FIELD_TYPES))


class UI_SelectItems(Schema):
    value = fields.String()
    text = fields.String()


class UI_Select(Schema):
    component = fields.Constant("v-select")
    items = fields.List(fields.Nested(UI_SelectItems))


class UI_Switch(Schema):
    component = fields.Constant("v-switch")
    "false-value" = PrimitiveTypeField()
    "true-value" = PrimitiveTypeField()


class UI_Component(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        valid_types = (UI_TextField, UI_Select, UI_Switch,)
        if isinstance(value, valid_types):
            return value
        else:
            raise ValidationError('Field should be a valid UI type')
