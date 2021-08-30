from flask import request
from flask_restful import Resource
from bson.objectid import ObjectId

from app.models import mongo
from app.util.mongo import projectMongoResults


class ProductConfig(Resource):

    def get(self):
        id = request.args.get("id")
        res = mongo.db.products.find_one({'_id': ObjectId(id)})
        product = projectMongoResults(res)
        return product, 200

    def post(self):
        req = request.get_json()
        mongo.db.products.insert_one(req)
        return req, 201

    def put(self):
        id = request.args.get("id")
        req = request.get_json()
        mongo.db.products.replace_one({'_id': ObjectId(id)}, req)
        return req, 201


class ProductConfigList(Resource):

    @classmethod
    def get(cls):
        res = mongo.db.products.find()
        products = projectMongoResults(res)
        return products, 200
