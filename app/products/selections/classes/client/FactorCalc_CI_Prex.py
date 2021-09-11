from ..base.FactorCalc import FactorCalc
from app.extensions import mongo


class FactorCalc_CI_Prex(FactorCalc):

    def __init__(self, factor_attributes, config):
        factor_type = 'product'
        factor_name = 'prex'
        super().__init__(factor_attributes, factor_name, factor_type, config)
