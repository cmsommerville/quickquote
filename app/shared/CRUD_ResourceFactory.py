from flask import request
from flask_restful import Resource
from .BaseModels import BaseModel


class CRUD_ResourceFactory: 

    def __init__(self, resource_name, model, schema, primary_key):
        self.resource_name = resource_name
        self.model = model
        self.schema = schema
        self.primary_key = primary_key
        self.schema_instance = schema()
        self.schema_list_instance = schema(many=True)

    def generate_class(self):
        cls = type(self.resource_name, (Resource,), {
                "__init__": self._constructor, 
                "get": self._get_method_generator(), 
                "post": self._post_method_generator(),
                "put": self._put_method_generator(),
                "delete": self._delete_method_generator()
            }, 
        )

        return cls

    def generate_list_class(self):
        cls = type(self.resource_name, (Resource,), {
                "__init__": self._constructor, 
                "get": self._get_list_method_generator(), 
                "post": self._post_list_method_generator()
            }, 
        )

        return cls

    def _constructor(self, **kwargs): 
        super(BaseModel).__init__

    def _get_method_generator(self):
        """
        This method returns a new method called `get`. 
        """
        @classmethod
        def get(cls, id):
            obj = self.model.find_one(id)
            return self.schema_instance.dump(obj), 200
        
        return get

    def _post_method_generator(self):
        """
        This method returns a new method called `post`. 
        """
        @classmethod
        def post(cls):
            req = request.get_json()
            obj = self.schema_instance.load(req)
            obj.save_to_db()
            return self.schema_instance.dump(obj), 201

        return post 

    def _put_method_generator(self):
        """
        This method returns a new method called `put`. 
        """
        @classmethod
        def put(cls, id): 
            req = request.get_json()
            obj = self.schema_instance.load({**req, self.primary_key: id})
            obj.save_to_db()
            return self.schema_instance.dump(obj), 201
        
        return put

    def _delete_method_generator(self):
        """
        This method returns a new method called `delete`. 
        """
        @classmethod
        def delete(cls, id): 
            obj = self.model.find_one(id)
            obj.delete()
            return "Deleted", 204

        return delete


    def _get_list_method_generator(self):
        """
        This method returns a new method called `get`. 
        """
        @classmethod
        def get(cls):
            params = {}
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            if limit: 
                params['limit'] = int(limit)

            if offset: 
                params['offset'] = int(offset)

            obj = self.model.find_all(**params)
            return self.schema_list_instance.dump(obj), 200
        
        return get

    def _post_list_method_generator(self):
        """
        This method returns a new method called `post`. 
        """
        @classmethod
        def post(cls):
            req = request.get_json()
            obj = self.schema_list_instance.load(req)
            self.model.save_all_to_db(obj)
            return self.schema_list_instance.dump(obj), 201

        return post 
