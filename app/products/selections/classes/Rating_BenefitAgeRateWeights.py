from typing import List
from decimal import Decimal
from sqlalchemy.orm import aliased
from sqlalchemy import literal
from app.extensions import db

from ..models import Model_SelectionPlan
from ...config.models import Model_ConfigProductVariation
from ...queries.Selection_WeightDistribution import query_config_weight_distribution
from ..schemas import Schema_QueryWeightDistribution

_config_schema_list = Schema_QueryWeightDistribution(many=True)

class Rating_BenefitAgeRateWeights:

    def __init__(
            self,
            plan: Model_SelectionPlan,
            weights: list = None,
            *args, **kwargs):
        
        self.plan = plan
        self.product_variation = plan.product_variation
        if weights:
            self.weights = {**self._formatter(**weights)}
        else:
            self.weights = {**self._formatter(self.default_weights())}

    def _formatter(self, weights: list, *args, **kwargs): 
        return {(w['age'], w['smoker_status'], w['gender'],): w['weight'] for w in weights}

    def default_weights(self) -> list:
        """
        Calculates the default weight distribution
        """
        return query_config_weight_distribution(self.plan, self.product_variation).all()

    def get(self, age, smoker_status, gender, *args, **kwargs): 
        return self.weights.get((age, smoker_status, gender,))
