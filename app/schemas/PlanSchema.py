from app.schemas import ma
from app.models.PlanModel import PlanModel


class PlanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlanModel
        load_instance = True
