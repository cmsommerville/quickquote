from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigAttributeDistributionSet
from .Config_AttributeDistribution import Schema_ConfigAttributeDistribution

class Schema_ConfigAttributeDistributionSet(BaseSchema):
    class Meta:
        model = Model_ConfigAttributeDistributionSet
        load_instance = True
        include_relationships = True
        include_fk = True

    attr_distribution = ma.List(ma.Nested(Schema_ConfigAttributeDistribution))
