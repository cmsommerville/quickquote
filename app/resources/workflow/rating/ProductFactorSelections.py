from flask import request
from flask_restful import Resource


class ProductFactorSelections(Resource):

    @classmethod
    def get(cls):
        return "Success", 200

    def post(self):
        data = request.get_json()
        print(data)
        return data, 200
