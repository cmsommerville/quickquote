from flask import request
from flask_restful import Resource
from app.extensions import db

from ..handlers.versioning_handlers import alter_versioned_table, drop_history_table

class CreateTables(Resource):

    @classmethod
    def get(cls):
        try:
            tables = [tbl for nm, tbl in db.metadata.tables.items()]

            dropTables = request.args.get('drop', "N")
            createTables = request.args.get('create', "N")

            if dropTables == 'Y':
                for tbl in tables:
                    drop_history_table(tbl)

                db.drop_all()

            if createTables == "Y": 
                db.create_all()
                for tbl in tables:
                    alter_versioned_table(tbl)

        except Exception as e:
            return str(e), 400
        else:
            return {"message": "Success"}, 200

