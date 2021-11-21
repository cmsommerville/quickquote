from flask import request
from flask_restful import Resource
from bson.objectid import ObjectId

from app.extensions import mongo
from app.shared import projectMongoResults, generateUUID
from ..schemas import Config_PlanSchema


plan_schema = Config_PlanSchema()
plan_list_schema = Config_PlanSchema(many=True)


class PlanConfig(Resource):

    def get(self, id):
        res = mongo.db.products.find_one({'_id': ObjectId(id)})
        product = plan_schema.dump(res)
        return product, 200

    def put(self, id):
        req = request.get_json()
        data = plan_schema.load(req)
        mongo.db.products.replace_one({'_id': ObjectId(id)}, data)
        return plan_schema.dump(data), 201

    def delete(self, id):
        mongo.db.products.delete_one({'_id': ObjectId(id)})
        return f"Successfully deleted {id}", 200


class PlanConfigList(Resource):

    @classmethod
    def get(cls):
        res = mongo.db.products.find()
        products = plan_list_schema.dump(res)
        return products, 200

    @classmethod
    def post(cls):
        req = request.get_json()
        data = plan_list_schema.load(req)
        mongo.db.products.insert_many(data)
        return plan_list_schema.dump(data), 201
