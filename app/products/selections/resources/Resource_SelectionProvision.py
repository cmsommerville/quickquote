import requests
from flask import request, session
from flask_restful import Resource

from ..models import Model_SelectionPlan, Model_SelectionProvision
from ..schemas import Schema_SelectionPlan, Schema_SelectionProvision, Schema_QueryProvision
from ...queries.Selection_Provisions import query_config_provisions, query_selection_provisions

_config_provision_list_schema = Schema_QueryProvision(many=True)
_selection_provision_list_schema = Schema_SelectionProvision(many=True)

class Resource_SelectionProvision(Resource):

    @classmethod
    def get(cls, plan_id):
        plan = Model_SelectionPlan.find_one(plan_id)
        if len(plan.provisions) > 0: 
            data = query_selection_provisions(plan).populate_existing()
            return _config_provision_list_schema.dump(data), 200

        data = query_config_provisions(plan).populate_existing()
        return _config_provision_list_schema.dump(data), 200

        

    @classmethod
    def post(cls, plan_id):
        data = request.get_json()
        provisions = _selection_provision_list_schema.load(data)
        Model_SelectionProvision.save_all_to_db(provisions)
        return _selection_provision_list_schema.dump(provisions), 201
