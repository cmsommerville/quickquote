import decimal
from typing_extensions import Required
from marshmallow import Schema, fields, validate, ValidationError

from ..data import constants


class Config_PlanRateSchema(Schema):
    code = fields.String(required=True)
    label = fields.String(required=False)
