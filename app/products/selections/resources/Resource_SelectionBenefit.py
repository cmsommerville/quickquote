import requests
from flask import request, session
from flask_restful import Resource

from ..models import Model_SelectionBenefit
from ..schemas import Schema_SelectionBenefit

_schema = Schema_SelectionBenefit()
_schema_list = Schema_SelectionBenefit(many=True)


class Resource_SelectionBenefit(Resource):

    @classmethod
    def get(cls, plan_id):
        try:
            bnfts = Model_SelectionBenefit.find_by_plan(plan_id)
            return _schema_list.dump(bnfts), 200
        except:
            return None, 200

    @classmethod
    def post(cls, plan_id):
        data = request.get_json()
        bnfts = _schema_list.load(data)

        try:
            Model_SelectionBenefit.save_all_to_db(bnfts)
        except Exception as e:
            print(e)

        return _schema_list.dump(bnfts), 201
