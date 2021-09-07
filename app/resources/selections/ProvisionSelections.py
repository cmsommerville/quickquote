from flask import request
from flask_restful import Resource

from app.models.ProvisionModel import ProvisionModel

from app.schemas.ProvisionSchema import ProvisionSchema

provision_list_schema = ProvisionSchema(many=True)


class ProvisionSelections(Resource):

    @classmethod
    def get(cls):
        plan_id = request.args.get("plan_id")
        if plan_id is None:
            raise Exception("Please provide a plan_id query parameter")

        provisions = ProvisionModel.find_plan_provisions(plan_id)
        return provision_list_schema.dump(provisions), 200

    @classmethod
    def post(cls):
        data = request.get_json()
        try:
            plan_id = data[0]["plan_id"]
        except Exception as e:
            return str(e), 400

        try:
            provisions = provision_list_schema.load(data)
            ProvisionModel.save_all_to_db(provisions, plan_id)
        except Exception as e:
            return str(e), 400

        return "created", 201
