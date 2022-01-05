from collections import defaultdict
from flask import request, session
from flask_restful import Resource

from ..models import Model_SelectionBenefit, Model_SelectionPlan
from ..schemas import Schema_SelectionBenefit, Schema_QueryBPV
from ...queries.ConfigBenefits__LEFT_JOIN__SelectionBenefits import query_benefits

_selection_schema_list = Schema_SelectionBenefit(many=True)
_config_schema_list = Schema_QueryBPV(many=True)


def formatter(config):
    """
    Allocate benefits to coverages
    """
    covg_dd = defaultdict(list)
    for bnft in config:
        covg = bnft['coverage']['coverage_label']
        covg_dd[covg].append(bnft)
    
    return [{
        **bnfts[0]['coverage'],
        "benefits": bnfts
    } for covg, bnfts in covg_dd.items()]



class Resource_SelectionBenefit(Resource):

    @classmethod
    def get(cls, plan_id):
        plan = Model_SelectionPlan.find_one(plan_id)
        if not plan: 
            return f"Plan does not exist for plan ID {plan_id}", 400
        
        # check that plan benefits exist 
        has_plan_benefits = (Model_SelectionBenefit.query.filter(Model_SelectionBenefit.selection_plan_id == plan_id).count() > 0)

        # indicates to the schema whether to set the UI values
        # equal to the defaults or the selected values
        _config_schema_list.context = {"has_plan_benefits": has_plan_benefits}

        # get query that returns config and selections
        qry = query_benefits(plan)
        data = _config_schema_list.dump(qry.populate_existing())
        data = formatter(data)
        return data, 200


    @classmethod
    def post(cls, plan_id):
        data = request.get_json()
        bnfts = _selection_schema_list.load(data)

        try:
            Model_SelectionBenefit.save_all_to_db(bnfts)
        except Exception as e:
            print(e)

        return _selection_schema_list.dump(bnfts), 201
