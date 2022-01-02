import decimal
from app.extensions import ma
from marshmallow import Schema, fields, post_dump

from .Schema_SelectionAgeBands import Schema_SelectionAgeBands
from .Schema_SelectionBenefit import Schema_SelectionBenefit


class Schema_SelectionPremiumByBenefitAgeBandRate(Schema):

    selection_benefit_rate_id = fields.Integer()
    selection_plan_id = fields.Integer()
    selection_benefit_id = fields.Integer()
    selection_age_band_id = fields.Integer()
    smoker_status = fields.Str()
    family_code = fields.Str()
    benefit_rate_premium = fields.Decimal()
    age_band = fields.Nested(Schema_SelectionAgeBands)
    benefit = fields.Nested(Schema_SelectionBenefit)

    @post_dump(pass_many=True)
    def formatDecimal(self, data, many, **kwargs):
        if many:
            return [{k: v if type(v) != decimal.Decimal else float(v) for k, v in item.items()}
                    for item in data]
        else:
            new_data = {k: v if type(v) != decimal.Decimal else float(v)
                        for k, v in data.items()}
            return new_data
