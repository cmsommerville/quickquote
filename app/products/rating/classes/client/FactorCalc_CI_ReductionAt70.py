from ..base.FactorCalc import FactorCalc
from app.models import mongo


class FactorCalc_CI_ReductionAt70(FactorCalc):

    def __init__(self, factor_attributes, config):
        factor_type = 'product'
        factor_name = 'reductionAt70'
        super().__init__(factor_attributes, factor_name, factor_type, config)
