from app.models import ma
from .StateModel import StateModel


class StateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StateModel
