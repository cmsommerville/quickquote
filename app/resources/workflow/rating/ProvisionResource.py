from flask import request, session
from flask_restful import Resource
from app.models import mongo
from app.util.mongo import projectMongoResults

from app.models.ProvisionModel import ProvisionModel
from app.schemas.ProvisionSchema import ProvisionSchema


provision_schema = ProvisionSchema()
provision_list_schema = ProvisionSchema(many=True)


class Provision(Resource):

    def get(self):
        return "success", 200

    def post(self):
        return "success", 200


class ProvisionList(Resource):

    @classmethod
    def get(cls):
        res = mongo.db.products.find(
            projection=["provisions"])

        provisions = projectMongoResults(res, ["provisions"])[0]['provisions']

        return provisions, 200

    @classmethod
    def post(cls):

        data = request.get_json()
        provisions = provision_list_schema.load(data)

        try:
            ProvisionModel.save_all_to_db(provisions)
        except:
            print("Couldn't write to db")

        return {"message": "Success"}, 201
