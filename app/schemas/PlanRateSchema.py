from app.schemas import ma
from app.models.PlanRateModel import PlanRateModel


class PlanRateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlanRateModel
        load_instance = True
        include_fk = True
