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

        # product states
        res = requests.post('http://localhost:5000/config/product/states', json=[
            {
                **state, 
                "product_id": product['product_id']
            } for state in CONFIG_PRODUCT_STATES
        ])

        # age distribution
        res = requests.post('http://localhost:5000/config/age-distribution', json=[
            {
                **x, 
                "product_id": product['product_id']
            } for x in CONFIG_AGE_DISTRIBUTION
        ])

        # gender distribution
        res = requests.post('http://localhost:5000/config/gender-distribution', json=[
            {
                **x, 
                "product_id": product['product_id']
            } for x in CONFIG_GENDER_DISTRIBUTION
        ])

        # smooker distribution
        res = requests.post('http://localhost:5000/config/smoker-distribution', json=[
            {
                **x, 
                "product_id": product['product_id']
            } for x in CONFIG_SMOKER_DISTRIBUTION
        ])
        
        # product variation
        res = requests.post('http://localhost:5000/config/product-variations', json={
            **CONFIG_PRODUCT_VARIATION, "product_id": product['product_id']})
        product_variation = res.json()
        
        # coverage
        res = requests.post('http://localhost:5000/config/coverage', json={
            **CONFIG_COVERAGE, "product_id": product['product_id']})
        coverage = res.json()

        # rate group
        res = requests.post('http://localhost:5000/config/rate-group', json={
            **CONFIG_RATE_GROUP, "product_id": product['product_id']
        })
        rate_group = res.json()

        # main benefit
        res = requests.post('http://localhost:5000/config/benefit', json={
            **CONFIG_BENEFIT, 
            "product_id": product['product_id'], 
            "rate_group_id": rate_group['rate_group_id'], 
            "coverage_id": coverage['coverage_id']
        })
        parent_benefit = res.json()

        # benefit states
        res = requests.post('http://localhost:5000/config/benefits', json=[
            {
                **state, 
                "parent_id": parent_benefit['benefit_id'], 
                "product_id": product['product_id']
            } for state in CONFIG_BENEFIT_STATES
        ])

        # benefit duration
        res = requests.post('http://localhost:5000/config/benefit-duration', json={
                **CONFIG_BENEFIT_DURATION, 
                "benefit_id": parent_benefit['benefit_id']
            }
        )

        # benefit product variation
        res = requests.post('http://localhost:5000/config/benefit-product-variations', json=[{
            "product_variation_id": product_variation['product_variation_id'], 
            "benefit_id": parent_benefit['benefit_id']
        }])

        return "Data loaded", 200
