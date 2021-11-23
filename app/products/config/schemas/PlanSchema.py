import uuid
from marshmallow import Schema, fields, validate, ValidationError, pre_load

from ..data import constants
from .StateSchema import Config_StateSchema
from .CoverageSchema import Config_CoverageSchema
from .ProvisionSchema import Config_ProvisionSchema
from .BenefitSchema import Config_BenefitSchema
from .PlanVariationSchema import Config_PlanVariationSchema


class Config_PlanSchema(Schema):
    _id = fields.String(dump_only=True)
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

    @pre_load
    def pre_load(self, data, *args, **kwargs):
        if data.get('_id'):
            data.pop('_id', data)
        return data
