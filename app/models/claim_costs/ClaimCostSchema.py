from app.models import ma
from .ClaimCostModel import ClaimCostModel


class ClaimCostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClaimCostModel
