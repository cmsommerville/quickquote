import decimal
import uuid
from marshmallow import Schema, fields, validate, ValidationError

from ..data import constants
from .FactorSchema import Config_FactorSchema
from .UISchema import UI_Component
from .StateSchema import Config_StateListOrInheritSchema


class Config_ProvisionSchema(Schema):
    uuid = fields.UUID(default=uuid.uuid4())
    code = fields.String(required=True)
    label = fields.String(required=True)
    states = Config_StateListOrInheritSchema(required=False)
    ui = UI_Component(required=True)
    factor = fields.Nested(Config_FactorSchema)
