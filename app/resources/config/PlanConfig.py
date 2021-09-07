from flask import request
from flask_restful import Resource
from bson.objectid import ObjectId

from app.models import mongo
from app.util.mongo import projectMongoResults, generateUUID


class PlanConfig(Resource):

    def get(self, id):
        res = mongo.db.products.find_one({'_id': ObjectId(id)})
        product = projectMongoResults(res)
        return product, 200

    def put(self, id):
        id = request.args.get("id")
        req = generateUUID([request.get_json()])[0]
        mongo.db.products.replace_one({'_id': ObjectId(id)}, req)
        return req, 201

    def delete(self, id):
        mongo.db.products.delete_one({'_id': ObjectId(id)})
        return f"Successfully deleted {id}", 200


class PlanConfigList(Resource):

    @classmethod
    def get(cls):
        res = mongo.db.products.find()
        products = projectMongoResults(res)
        return products, 200

    @classmethod
    def post(cls):
        req = generateUUID(request.get_json())
        mongo.db.products.insert_one(req)
        return req, 201
