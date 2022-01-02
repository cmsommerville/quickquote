import decimal
from app.extensions import ma
from marshmallow import Schema, fields, post_dump

from .Schema_SelectionAgeBands import Schema_SelectionAgeBands


class Schema_SelectionPremiumByRateGroup(Schema):

    plan_id = fields.Integer()
    rate_group_summary_id = fields.Integer()
    family_code = fields.Str()
    smoker_status = fields.Str()
    plan_rate_premium = fields.Decimal()

    age_band = fields.Nested(Schema_SelectionAgeBands)

    @post_dump(pass_many=True)
    def formatDecimal(self, data, many, **kwargs):
        if many:
            return [{k: v if type(v) != decimal.Decimal else float(v) for k, v in item.items()}
                    for item in data]
        else:
            new_data = {k: v if type(v) != decimal.Decimal else float(v)
                        for k, v in data.items()}
            return new_data
