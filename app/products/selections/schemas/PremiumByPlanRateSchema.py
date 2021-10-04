import decimal
from app.extensions import ma
from marshmallow import Schema, fields, post_dump

from .AgeBandsSchema import AgeBandsSchema


class PremiumByPlanRateSchema(Schema):

    plan_id = fields.Integer()
    plan_rate_code = fields.Str()
    family_code = fields.Str()
    smoker_status = fields.Str()
    plan_rate_premium = fields.Decimal()

    age_band = fields.Nested(AgeBandsSchema)

    @post_dump(pass_many=True)
    def formatDecimal(self, data, many, **kwargs):
        if many:
            return [{k: v if type(v) != decimal.Decimal else float(v) for k, v in item.items()}
                    for item in data]
        else:
            new_data = {k: v if type(v) != decimal.Decimal else float(v)
                        for k, v in data.items()}
            return new_data
