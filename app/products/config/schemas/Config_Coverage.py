from app.extensions import ma
from ..models import Model_ConfigCoverage


class Schema_ConfigCoverage(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigCoverage
        load_instance = True
        include_relationships = True
        include_fk = True
