from app.extensions import ma
from ..models.PlanModel import PlanModel


class PlanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlanModel
        load_instance = True
        include_fk = True
