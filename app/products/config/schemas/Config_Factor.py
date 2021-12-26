from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigFactor
from .Config_FactorRule import Schema_ConfigFactorRule

    
class Schema_ConfigFactor(BaseSchema): 
    class Meta:
        model = Model_ConfigFactor
        load_instance = True
        include_relationships = True
        include_fk = True
    
    factor_rules = ma.List(ma.Nested(Schema_ConfigFactorRule))
