import uuid
from marshmallow import Schema, fields, validate, ValidationError

from ..data import constants


class PrimitiveTypeField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, (str, bool, float, int,)):
            return value
        else:
            raise ValidationError('Field should be str, float, int, or bool')


class Policy_ProvisionRuleSchema(Schema):
    code = fields.String(required=True)
    comparison = fields.String(
        required=True, validate=validate.OneOf(constants.OPERATOR_CODES))
    value = PrimitiveTypeField(required=False)


class Policy_BenefitDurationItemsSchema(Schema):
    value = fields.String(required=True)
    accessLevel = fields.String(
        required=True, validate=validate.OneOf(constants.QUOTING_ACCESS_LEVELS))


class Policy_BenefitAmountsSchema(Schema):
    min = fields.Float(required=True)
    max = fields.Float(required=True)
    step = fields.Float(required=True)


class Policy_BenefitSchema(Schema):
    code = fields.String(required=True)
    accessLevel = fields.String(
        required=True, validate=validate.OneOf(constants.QUOTING_ACCESS_LEVELS))
    amounts = fields.Nested(Policy_BenefitAmountsSchema, required=False)
    durations = fields.List(fields.Nested(
        Policy_BenefitDurationItemsSchema), required=False)


class Policy_CoverageSchema(Schema):
    code = fields.String(required=True)
    accessLevel = fields.String(
        required=True, validate=validate.OneOf(constants.QUOTING_ACCESS_LEVELS))


class Policy_PlanDesignSchema(Schema):
    code = fields.String(required=True)


class Policy_StateSchema(Schema):
    code = fields.String(required=True)
    applicability = fields.String(
        required=True, validate=validate.OneOf(constants.APPLICABILITY_VALUES))


class Policy_ProductVariationSchema(Schema):
    code = fields.String(required=True)
    applicability = fields.String(
        required=True, validate=validate.OneOf(constants.APPLICABILITY_VALUES))


class Policy_ProductSchema(Schema):
    uuid = fields.UUID(default=uuid.uuid4())
    code = fields.String(required=True)
    label = fields.String(required=True)
    effectiveDate = fields.Date(required=True)
    expiryDate = fields.Date(required=True)

    product_code = fields.String(required=True)
    variations = fields.List(fields.Nested(
        Policy_ProductVariationSchema), required=True)
    states = fields.List(fields.Nested(Policy_StateSchema), required=True)
    coverageVariability = fields.Boolean(required=True)
    benefitVariability = fields.Boolean(required=True)
    provisionVariability = fields.Boolean(required=True)
    permittedPlanDesigns = fields.List(
        fields.Nested(Policy_PlanDesignSchema), required=False)

    coverages = fields.List(fields.Nested(
        Policy_CoverageSchema), required=True)
    benefits = fields.List(fields.Nested(Policy_BenefitSchema), required=False)
    provisions = fields.List(fields.Nested(
        Policy_ProvisionRuleSchema), required=False)
