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
        with open("data/database.json") as f:
            data = json.load(f)

        selections = {}
        group = session.get("selections", {}).get("group")

        if group:
            selections = group_schema.dump(group)

        return {
            "selections": selections
        }, 200

    def post(self):

        data = request.get_json()
        group = session.get("selections", {}).get("group")
        if group:
            group.reset(data)
        else:
            group = group_schema.load(data)

        try:
            group.save_to_db()
        except:
            print("Couldn't write to db")

        session['selections'] = {
            **session.get('selections', {}),
            "group": group
        }

        return "Success", 201
