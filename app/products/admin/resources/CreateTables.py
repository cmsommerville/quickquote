from flask import request
from flask_restful import Resource
from app.extensions import db


class CreateTables(Resource):

    @classmethod
    def get(cls):
        try:
            dropTables = request.args.get('drop')
            if dropTables == 'Y':
                db.drop_all()
            db.create_all()
        except Exception as e:
            return str(e), 400
        else:
            return {"message": "Created tables"}, 200
