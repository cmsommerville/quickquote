from app.rater.base_classes.FactorBase import FactorBase
from app.models import mongo


class FactorGroupSize(FactorBase):

    def __init__(self, factor_attributes, config):
        factor_type = 'product'
        factor_name = 'groupsize'
        super().__init__(factor_attributes, factor_name, factor_type, config)
