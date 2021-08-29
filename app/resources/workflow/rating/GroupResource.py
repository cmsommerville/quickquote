import json
from flask import request, session
from flask_restful import Resource

from app.models.GroupModel import GroupModel
from app.models.PlanModel import PlanModel
from app.schemas.GroupSchema import GroupSchema

group_schema = GroupSchema()


class Group(Resource):
    @classmethod
    def get(cls):
        selections = {}
        group_id = session.get("quote", {}).get("group_id")
        if group_id:
            group = GroupModel.find_by_id(group_id)
            selections = group_schema.dump(group)

        return {"selections": selections}, 200

    def post(self):
        data = request.get_json()
        group_id = session.get("quote", {}).get("group_id")
        if group_id:
            group = GroupModel.find_by_id(group_id)
            group.reset(data)
        else:
            group = group_schema.load(data)

        try:
            group.save_to_db()
        except:
            print("Couldn't write to db")

        if session.get("quote") is None:
            session['quote'] = {}

        session['quote']['group_id'] = group.group_id

        return "Success", 201
