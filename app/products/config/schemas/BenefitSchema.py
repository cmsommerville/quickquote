import decimal
from marshmallow import Schema, fields, validate, ValidationError

from ..data import constants
from .StateSchema import Config_StateSchema
from .UISchema import UI_Component
from .CoverageSchema import Config_CoverageSchema
from .PlanRateSchema import Config_PlanRateSchema


class Config_BenefitRangeAmountsSchema(Schema):
    default = fields.Decimal(2, required=True)
    min = fields.Decimal(2, required=True)
    max = fields.Decimal(2, required=True)
    step = fields.Decimal(2, required=True)
    unit = fields.String(required=True, validate=validate.OneOf(['dollar']))


class Config_BenefitSchema(Schema):
    code = fields.String(required=True)
    label = fields.String(required=True)
    ui = UI_Component(required=True)
    coverage_code = fields.Nested(
        lambda: Config_CoverageSchema(only=("code",)))
    plan_rate_code = fields.Nested(
        lambda: Config_PlanRateSchema(only=("code", )))
    amounts = fields.Nested(Config_BenefitRangeAmountsSchema, required=True)
    states = fields.List(fields.Nested(
        Config_StateSchema), required=False)
