import decimal
from app.extensions import ma
from marshmallow import Schema, fields, post_dump

from .BenefitSchema import BenefitSchema


class PremiumByBenefitRateSchema(Schema):

    benefit_rate_id = fields.Integer()
    benefit_id = fields.Integer()
    plan_id = fields.Integer()
    age = fields.Integer()
    family_code = fields.Str()
    smoker_status = fields.Str()
    benefit_rate_uuid = fields.Str()
    benefit_rate_base_premium = fields.Decimal()
    benefit_rate_factor = fields.Decimal()
    benefit_rate_benefit_factor = fields.Decimal()
    benefit_rate_final_premium = fields.Decimal()

    benefit = fields.Nested(BenefitSchema)

    @post_dump(pass_many=True)
    def formatDecimal(self, data, many, **kwargs):
        if many:
            return [{k: v if type(v) != decimal.Decimal else float(v) for k, v in item.items()}
                    for item in data]
        else:
            new_data = {k: v if type(v) != decimal.Decimal else float(v)
                        for k, v in data.items()}
            return new_data
