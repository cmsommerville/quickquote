import decimal
from marshmallow import Schema, fields, validate, ValidationError

from ..data import constants
from .FactorSchema import Config_FactorSchema
from .UISchema import UI_Component
from .StateSchema import Config_StateSchema


class Config_ProvisionSchema(Schema):
    code = fields.String(required=True)
    label = fields.String(required=True)
    states = fields.List(fields.Nested(Config_StateSchema), required=False)
    ui = UI_Component(required=True)
    factor = fields.Nested(Config_FactorSchema)
