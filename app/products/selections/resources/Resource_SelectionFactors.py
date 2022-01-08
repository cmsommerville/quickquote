from collections import defaultdict
from flask import request, session
from flask_restful import Resource

from ..models import Model_SelectionProvision, Model_SelectionPlan
from ..schemas import Schema_QueryFactors_SelectionProvision
from ...queries.Selection_Factors import query_config_factors

_selection_schema_list = Schema_QueryFactors_SelectionProvision(many=True)
# _config_schema_list = Schema_QueryBPV(many=True)



class Resource_SelectionFactors(Resource):

    @classmethod
    def get(cls, plan_id):
        plan = Model_SelectionPlan.find_one(plan_id)
        if not plan: 
            return f"Plan does not exist for plan ID {plan_id}", 400
        
        # get query that returns config and selections
        qry = query_config_factors(plan)
        
        return _selection_schema_list.dump(qry.populate_existing()), 200

