from flask import request
from flask_restful import Resource
from app.models.products.ProductModel import ProductModel
from app.models.products.ProductSchema import ProductSchema


product_schema = ProductSchema()
product_list_schema = ProductSchema(many=True)


class ProductAdmin(Resource):

    @classmethod
    def get(cls):
        id = request.args.get("id")
        product = ProductModel.find_by_id(id)
        return product_schema.dump(product)

    def post(self):
        data = request.get_json()
        product = ProductModel(**product_schema.load(data))
        product.save_to_db()
        return product_schema.dump(product)


class ProductAdminList(Resource):

    @classmethod
    def get(cls):
        products = ProductModel.find_all(num_rows=1000)
        return product_list_schema.dump(products)
