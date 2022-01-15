from flask import request, session
from flask_restful import Resource

from ..models import Model_SelectionRateGroupSummary
from ..schemas import Schema_SelectionRateGroupSummary

_selection_schema_list = Schema_SelectionRateGroupSummary(many=True)


class Resource_SelectionRateGroupSummary(Resource):

    @classmethod
    def get(cls, plan_id):
        data = Model_SelectionRateGroupSummary.calculate(plan_id)
        return _selection_schema_list.dump(data), 200
