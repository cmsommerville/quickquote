from app.extensions import ma
from ..models import Model_RefStates


class Schema_RefStates(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefStates
        load_instance = True
        include_relationships = True
        include_fk = True
