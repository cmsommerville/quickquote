from app.shared import CRUD_ResourceFactory
from flask_restful import Resource
from app.products.config.models import Model_ConfigRateGroup
from app.products.config.schemas import Schema_ConfigRateGroup

# <bound method CRUD_ResourceFactory._get_list_method_generator.<locals>.get of
# <class 'app.shared.CRUD_ResourceFactory.tester'>>
test_resource = CRUD_ResourceFactory(
            resource_name='tester', 
            model=Model_ConfigRateGroup, 
            schema=Schema_ConfigRateGroup,
            primary_key='rate_group_id'
        ).generate_list_class()


_schema = Schema_ConfigRateGroup(many=True)
class real_resource(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigRateGroup.find_child_states(id)
        return _schema.dump(config), 200


print((test_resource.__dict__))
print("\n")
print((real_resource.__dict__))