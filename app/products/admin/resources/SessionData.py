import json
from flask import request, session
from flask_restful import Resource


class SessionData(Resource):

    def get(self):
        try:
            session_obj = {k: v for k, v in session.items()}
            session_data = json.dumps(
                session_obj, default=lambda x: "<Object>")
        except Exception as e:
            return str(e), 400
        else:
            return session_data, 200
