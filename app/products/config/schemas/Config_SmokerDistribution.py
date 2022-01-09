from app.shared import BaseSchema

from ..models import Model_ConfigSmokerDistribution

class Schema_ConfigSmokerDistribution(BaseSchema):
    class Meta:
        model = Model_ConfigSmokerDistribution
        load_instance = True
        include_relationships = True
        include_fk = True
