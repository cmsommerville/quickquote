from flask import request
from flask_restful import Resource
from werkzeug.datastructures import FileStorage
from app.shared import CRUD_ResourceFactory

from ..models import Model_ConfigRateTable
from ..schemas import Schema_ConfigRateTable

_schema_list = Schema_ConfigRateTable(many=True)

_Standard_CRUD_Config_RateTable_List = CRUD_ResourceFactory(
    resource_name='_Standard_CRUD_Config_RateTable_List', 
    model=Model_ConfigRateTable, 
    schema=Schema_ConfigRateTable,
    primary_key='rate_table_id'
).generate_list_class()


upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

class Resource_UploadRateTable(Resource):
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        url = do_something_with_file(uploaded_file)
        return {'url': url}, 201
