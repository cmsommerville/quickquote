import json
from flask import request, session
from flask_restful import Resource


class ProductFactors(Resource):

    @classmethod
    def get(cls):
        with open("data/database.json") as f:
            data = json.load(f)

        selections = {"prex": None, "reductionAt70": None, **
                      session.get("selections", {}).get("product_factors", {})}
        return {
            "product": data['product'],
            "statesApproved": data['statesApproved'],
            "factors": data['factors']['product'],
            "selections": selections
        }, 200

    def post(self):
        data = request.get_json()
        session['selections'] = {
            **session.get("selections", {}), "product_factors": data}

        print(session['selections'])
        return "Success", 201
