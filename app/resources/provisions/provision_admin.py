from flask import request
from flask_restful import Resource
from app.models.provisions.ProvisionModel import ProvisionModel
from app.models.provisions.ProvisionSchema import ProvisionSchema


provision_schema = ProvisionSchema()
provision_list_schema = ProvisionSchema(many=True)


class ProvisionAdmin(Resource):

    @classmethod
    def get(cls):
        id = request.args.get("id")
        provision = ProvisionModel.find_by_id(id)
        return provision_schema.dump(provision)

    def post(self):
        data = request.get_json()
        provision = ProvisionModel(**provision_schema.load(data))
        provision.save_to_db()
        return provision_schema.dump(provision)


class ProvisionAdminList(Resource):

    @classmethod
    def get(cls):
        provisions = ProvisionModel.find_all(num_rows=1000)
        return provision_list_schema.dump(provisions)
