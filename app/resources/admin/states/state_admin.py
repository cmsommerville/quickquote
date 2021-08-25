from flask import request
from flask_restful import Resource
from app.models.states.StateModel import StateModel
from app.models.states.StateSchema import StateSchema


state_schema = StateSchema()
state_list_schema = StateSchema(many=True)


class StateAdmin(Resource):

    @classmethod
    def get(cls):
        id = request.args.get("id")
        state = StateModel.find_by_id(id)
        return state_schema.dump(state)

    def post(self):
        data = request.get_json()
        state = StateModel(**state_schema.load(data))
        state.save_to_db()
        return state_schema.dump(state)


class StateAdminList(Resource):

    @classmethod
    def get(cls):
        states = StateModel.find_all(num_rows=1000)
        return state_list_schema.dump(states)
