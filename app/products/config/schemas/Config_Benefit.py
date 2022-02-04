from app.extensions import ma
from app.shared import BaseSchema
from ..models import Model_ConfigBenefit

from .Ref_Benefit import Schema_RefBenefit
from .Ref_States import Schema_RefStates
from .Config_Coverage import Schema_ConfigCoverage
from .Config_BenefitDuration import Schema_ConfigBenefitDuration


class Schema_ConfigBenefit(BaseSchema):
    class Meta:
        model = Model_ConfigBenefit
        load_instance = True
        include_relationships = True
        include_fk = True

    benefit_label = ma.Function(lambda obj: obj.ref_benefit.benefit_label)
    coverage_code = ma.Function(lambda obj: getattr(obj.coverage, 'coverage_code', None))
    
    
    ref_benefit = ma.Nested(Schema_RefBenefit)
    state = ma.Nested(Schema_RefStates)
    child_states = ma.List(ma.Nested('self', exclude=('child_states',)))
    coverage = ma.Nested(Schema_ConfigCoverage)
    durations = ma.List(ma.Nested(Schema_ConfigBenefitDuration))