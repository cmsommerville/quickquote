from app.extensions import ma
from ..models import Model_ConfigCoverage, Model_ConfigCoverageStateAvailability


class Schema_ConfigCoverage(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigCoverage
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_ConfigCoverageStateAvailability(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigCoverageStateAvailability
        load_instance = True
        include_relationships = True
        include_fk = True

