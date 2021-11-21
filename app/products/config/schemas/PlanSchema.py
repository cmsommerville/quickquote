import uuid
from marshmallow import Schema, fields, validate, ValidationError

from ..data import constants
from .StateSchema import Config_StateSchema
from .CoverageSchema import Config_CoverageSchema
from .ProvisionSchema import Config_ProvisionSchema
from .BenefitSchema import Config_BenefitSchema
from .PlanVariationSchema import Config_PlanVariationSchema


class Config_PlanSchema(Schema):
    code = fields.String(required=True)
    label = fields.String(required=True)
    uuid = fields.UUID(default=uuid.uuid4())
    variations = fields.List(fields.Nested(
        Config_PlanVariationSchema), required=True)
    states = fields.List(fields.Nested(
        Config_StateSchema), required=True)
    coverages = fields.List(fields.Nested(
        Config_CoverageSchema), required=True)
    provisions = fields.List(fields.Nested(
        Config_ProvisionSchema), required=True)
    benefits = fields.List(fields.Nested(Config_BenefitSchema))