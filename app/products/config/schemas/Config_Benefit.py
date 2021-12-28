from app.extensions import ma
from app.shared import BaseSchema
from ..models import Model_ConfigBenefit

from .Ref_Benefit import Schema_RefBenefit
from .Ref_States import Schema_RefStates



class Schema_ConfigBenefit(BaseSchema):
    class Meta:
        model = Model_ConfigBenefit
        load_instance = True
        include_relationships = True
        include_fk = True

    ref_benefit = ma.Nested(Schema_RefBenefit)
    state = ma.Nested(Schema_RefStates)
    child_states = ma.List(ma.Nested('self', exclude=('child_states',)))