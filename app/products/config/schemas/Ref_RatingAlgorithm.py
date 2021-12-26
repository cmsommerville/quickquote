from app.shared import BaseSchema

from ..models import Model_RefRatingAlgorithm

class Schema_RefRatingAlgorithm(BaseSchema):
    class Meta:
        model = Model_RefRatingAlgorithm
        load_instance = True
        include_relationships = True
        include_fk = True
