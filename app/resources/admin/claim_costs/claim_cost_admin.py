from flask import request
from flask_restful import Resource
from app.models.claim_costs.ClaimCostModel import ClaimCostModel
from app.models.claim_costs.ClaimCostSchema import ClaimCostSchema


claim_cost_schema = ClaimCostSchema()
claim_cost_list_schema = ClaimCostSchema(many=True)


class ClaimCostAdmin(Resource):

    @classmethod
    def get(cls):
        id = request.args.get("id")
        claim_cost = ClaimCostModel.find_by_id(id)
        return claim_cost_schema.dump(claim_cost)

    def post(self):
        data = request.get_json()
        claim_cost = ClaimCostModel(**claim_cost_schema.load(data))
        claim_cost.save_to_db()
        return claim_cost_schema.dump(claim_cost)


class ClaimCostAdminList(Resource):

    @classmethod
    def get(cls):
        claim_costs = ClaimCostModel.find_all(num_rows=1000)
        return claim_cost_list_schema.dump(claim_costs)
