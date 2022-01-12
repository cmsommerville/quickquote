from app.extensions import ma
from app.shared import BaseSchema

class Schema_QueryWeightDistribution(BaseSchema):
    smoker_status = ma.String()
    gender = ma.String()
    age = ma.Integer()
    total_weight = ma.Decimal(5, data_key="weight")