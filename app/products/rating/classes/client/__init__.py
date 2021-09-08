from .FactorCalc_CI_GroupSize import FactorCalc_CI_GroupSize
from .FactorCalc_CI_Prex import FactorCalc_CI_Prex
from .FactorCalc_CI_ReductionAt70 import FactorCalc_CI_ReductionAt70


ELIGIBLE_FACTORS = {
    'groupsize': FactorCalc_CI_GroupSize,
    'prex': FactorCalc_CI_Prex,
    'reductionAt70': FactorCalc_CI_ReductionAt70
}
