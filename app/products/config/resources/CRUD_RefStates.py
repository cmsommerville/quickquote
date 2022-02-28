from flask import request
from flask_restful import Resource
from app.shared import CRUD_ResourceFactory

from ..models import Model_RefStates
from ..schemas import Schema_RefStates

_config_list_schema = Schema_RefStates(many=True)
_Standard_CRUD_Ref_States_List = CRUD_ResourceFactory(
    resource_name='_Standard_CRUD_Ref_States_List', 
    model=Model_RefStates, 
    schema=Schema_RefStates,
    primary_key='state_id'
).generate_list_class()

class CRUD_RefStates_List(_Standard_CRUD_Ref_States_List):

    @classmethod
    def get(cls):
        allStates = request.args.get('all', 'Y')
        states = Model_RefStates.find_all()
        states_data = _config_list_schema.dump(states)
        if allStates == 'Y': 
            return states_data, 200
        else: 
            return [s for s in states_data if s['state_id'] > 0], 200
