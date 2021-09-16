from flask import request
from flask_restful import Resource

from ..models import RateTableModel
from ..schemas import RateTableSchema

rate_table_list_schema = RateTableSchema(many=True)


class RateTableList(Resource):

    @classmethod
    def get(cls):
        product_code = request.args.get('product_code')
        product_variation_code = request.args.get('product_variation_code')
        benefit_code = request.args.get('benefit_code')

        rates = RateTableModel.find_benefit_rateset(
            product_code, product_variation_code, benefit_code)
        return rate_table_list_schema.dump(rates), 200

    @classmethod
    def post(cls):
        data = request.get_json()
        rates = rate_table_list_schema.load(data)
        RateTableModel.save_all_to_db(rates)
        return rate_table_list_schema.dump(rates), 201
