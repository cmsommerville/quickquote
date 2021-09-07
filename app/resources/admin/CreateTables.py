from flask_restful import Resource
from app.models import db


class CreateTables(Resource):

    @classmethod
    def get(cls):
        try:
            db.drop_all()
            db.create_all()
        except Exception as e:
            return str(e), 400
        else:
            return {"message": "Created tables"}, 200
