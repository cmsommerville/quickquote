import decimal
import uuid
from marshmallow import Schema, fields, validate, ValidationError

from ..data import constants
from .StateSchema import Config_StateListOrInheritSchema
from .UISchema import UI_Component


class Config_BenefitRangeAmountsSchema(Schema):
    default = fields.Float(required=True)
    min = fields.Float(required=True)
    max = fields.Float(required=True)
    step = fields.Float(required=True)
    unit = fields.String(
        required=True, validate=validate.OneOf(['dollar', 'percent']))

    # "duration": {
    #     "default": 30,
    #     "component": "v-select",
    #     "code": "hosp_confinement_days",
    #     "outlined": true,
    #     "label": "Confinement Days",
    #     "items": [
    #         {"value": 30, "label": 30, "factor": 1},
    #         {"value": 365, "label": 365, "factor": 1.47}
    #     ]
    # },


class Config_BenefitDurationItemsSchema(Schema):
    value = fields.String(required=True)
    label = fields.String(required=True)
    factor = fields.Float(required=True)


class Config_BenefitDurationSchema(Schema):
    code = fields.String(required=True)
    label = fields.String(required=True)
    component = fields.String(
        required=True, validate=validate.OneOf(constants.UI_COMPONENTS))
    items = fields.List(fields.Nested(
        Config_BenefitDurationItemsSchema), required=True)


class Config_BenefitFactorApplicabilitySchema(Schema):
    code = fields.String(required=True)
    applicability = fields.Boolean(required=True)


class Config_BenefitSchema(Schema):
    code = fields.String(required=True)
    label = fields.String(required=True)
    uuid = fields.UUID(default=uuid.uuid4())
    ui = UI_Component(required=True)
    coverage_code = fields.String(required=True)
    plan_rate_code = fields.String(required=True)
    amounts = fields.Nested(Config_BenefitRangeAmountsSchema, required=True)
    durations = fields.List(fields.Nested(
        Config_BenefitDurationSchema), required=False)
    states = Config_StateListOrInheritSchema(required=False)
    factors = fields.List(fields.Nested(
        Config_BenefitFactorApplicabilitySchema), required=False)
