from collections import defaultdict
from flask import request, session
from flask_restful import Resource

from ...queries.Selection_WeightDistribution import query_config_weight_distribution
from ...config.models import Model_ConfigProductVariation
from ..models import Model_SelectionPlan
from ..schemas import Schema_QueryWeightDistribution

_config_schema_list = Schema_QueryWeightDistribution(many=True)


class Resource_SelectionWeights(Resource):

    @classmethod
    def get(cls):
        plan = Model_SelectionPlan.find_one(1)
        product_variation = plan.product_variation
        res = query_config_weight_distribution(plan, product_variation).all()

        return _config_schema_list.dump(res), 200
