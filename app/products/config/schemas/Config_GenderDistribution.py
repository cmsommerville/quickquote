from app.shared import BaseSchema

from ..models import Model_ConfigGenderDistribution

class Schema_ConfigGenderDistribution(BaseSchema):
    class Meta:
        model = Model_ConfigGenderDistribution
        load_instance = True
        include_relationships = True
        include_fk = True
