import requests
from flask_restful import Resource
from .constants import *
from app.extensions import db

def insertAllStatesRecord():
    db.session.execute("SET IDENTITY_INSERT DBO.ref_state ON")
    db.session.execute("INSERT INTO DBO.ref_state (state_id, state_code, state_name) VALUES(0, 'XX', 'All States')")
    db.session.execute("SET IDENTITY_INSERT DBO.ref_state OFF")
    db.session.commit()

class Resource_InitializeData(Resource):
    def get(self): 
        # drop and create tables
        requests.get('http://localhost:5000/admin/create-tables?drop=Y&create=Y')

        # states
        requests.post('http://localhost:5000/config/ref-states', json=REF_STATES)
        insertAllStatesRecord()

        # # unit codes
        requests.post('http://localhost:5000/config/ref-unit-codes', json=REF_UNIT_CODES)

        # # ui component types
        for typ in REF_UI_COMPONENT_TYPES: 
            requests.post('http://localhost:5000/config/ref-component-type', json=typ)

        # # text field types
        for typ in REF_INPUT_TYPES: 
            requests.post('http://localhost:5000/config/ref-text-field-type', json=typ)

        # comparison operators
        for op in REF_COMPARISON_OPERATORS:
            requests.post('http://localhost:5000/config/ref-comparison-operator', json=op)

        for alg in REF_RATING_ALGORITHMS: 
            requests.post('http://localhost:5000/config/ref-rating-algorithm', json=alg)

        # # product
        res = requests.post('http://localhost:5000/config/product', json=CONFIG_PRODUCT)
        product = res.json()

        # product variation
        requests.post('http://localhost:5000/config/product-variations', json={
            **CONFIG_PRODUCT_VARIATION, "product_id": product['product_id']})
        
        # coverage
        requests.post('http://localhost:5000/config/coverage', json={
            **CONFIG_COVERAGE, "product_id": product['product_id']})

        # rate group
        requests.post('http://localhost:5000/config/rate-group', json={
            **CONFIG_RATE_GROUP, "product_id": product['product_id']
        })

        return "Data loaded", 200
