import decimal
import uuid
from marshmallow import Schema, fields, validate, ValidationError


class Config_AgeBandSchema(Schema):
    lower_age = fields.Integer(required=True)
    upper_age = fields.Integer(required=True)


class Config_AgeBandsStateSchema(Schema):
    state = fields.String(required=True)
    age_bands = fields.List(fields.Nested(Config_AgeBandSchema))


class Config_PlanVariationSchema(Schema):
    code = fields.String(required=True)
    label = fields.String(required=True)
    default = fields.Boolean(required=True)
    is_age_rated = fields.Boolean(required=True)
    is_tobacco_rated = fields.Boolean(required=True)
    is_family_code_rated = fields.Boolean(required=True)
    min_issue_age = fields.Integer(required=False)
    max_issue_age = fields.Integer(required=False)
    age_bands = fields.List(fields.Nested(Config_AgeBandsStateSchema))
