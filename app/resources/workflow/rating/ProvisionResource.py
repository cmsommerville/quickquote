from flask import request, session
from flask_restful import Resource
from app.models import mongo
from app.util.mongo import projectMongoResults

from app.models.ProvisionModel import ProvisionModel
from app.schemas.ProvisionSchema import ProvisionSchema


provision_schema = ProvisionSchema()


class Provision(Resource):

    @classmethod
    def get(cls):

        provision = ProvisionModel(plan_id=1, provision_code="X",
                                   provision_name="X", provision_value="1", provision_data_type="int")
        return provision_schema.dump(provision), 200
