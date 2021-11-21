from marshmallow import Schema, fields, validate, ValidationError
import uuid

from ..data import constants


class PrimitiveTypeField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str) or isinstance(value, float) or isinstance(value, int) or isinstance(value, bool):
            return value
        else:
            raise ValidationError('Field should be str, float, int, or bool')


class UI_TextField(Schema):
    component = fields.String(required=True)
    type = fields.String(
        default="input", validate=validate.OneOf(constants.UI_TEXT_FIELD_TYPES))
    min = fields.String(required=False)
    max = fields.String(required=False)
    step = fields.String(required=False)


class UI_SelectItems(Schema):
    value = fields.String()
    text = fields.String()
    uuid = fields.UUID(default=uuid.uuid4())


class UI_Select(Schema):
    component = fields.String(required=True)
    items = fields.List(fields.Nested(UI_SelectItems))
    uuid = fields.UUID(default=uuid.uuid4())


class UI_Switch(Schema):
    component = fields.String(required=True)
    false_value = PrimitiveTypeField(data_key="false-value")
    true_value = PrimitiveTypeField(data_key="true-value")


class UI_Component(fields.Field):
    def _serialize(self, value, attr, data, **kwargs):
        if value['component'] == 'v-text-field':
            schema = UI_TextField()
            return schema.dump(value)
        if value['component'] == 'v-select':
            schema = UI_Select()
            return schema.dump(value)
        if value['component'] == 'v-switch':
            schema = UI_Switch()
            return schema.dump(value)
        raise ValidationError('Field should be a valid UI type')

    def _deserialize(self, value, attr, data, **kwargs):
        if value['component'] == 'v-text-field':
            schema = UI_TextField()
            return schema.load(value)
        if value['component'] == 'v-select':
            schema = UI_Select()
            return schema.load(value)
        if value['component'] == 'v-switch':
            schema = UI_Switch()
            return schema.load(value)
        raise ValidationError('Field should be a valid UI type')
