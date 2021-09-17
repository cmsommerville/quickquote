import decimal
from app.extensions import ma
from marshmallow import Schema, fields, post_dump

from .BenefitSchema import BenefitSchema


class PremiumByBenefitAgeBandRateSchema(Schema):

    plan_id = fields.Integer()
    benefit_id = fields.Integer()
    age_band_id = fields.Integer()
    smoker_status = fields.Str()
    family_code = fields.Str()
    benefit_rate_final_premium = fields.Decimal()

    @post_dump(pass_many=True)
    def formatDecimal(self, data, many, **kwargs):
        if many:
            return [{k: v if type(v) != decimal.Decimal else float(v) for k, v in item.items()}
                    for item in data]
        else:
            new_data = {k: v if type(v) != decimal.Decimal else float(v)
                        for k, v in data.items()}
            return new_data
