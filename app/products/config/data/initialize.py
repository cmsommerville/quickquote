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

        # ui component types
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
        # res = requests.post('http://localhost:5000/config/product/states', json=[
        #     {
        #         **state, 
        #         "product_id": product['product_id']
        #     } for state in CONFIG_PRODUCT_STATES
        # ])

        # age distribution
        res = requests.post('http://localhost:5000/config/age-distribution-set', json=AGE_DISTRIBUTION)
        age_distribution_set = res.json()

        # sex distinct distribution
        res = requests.post('http://localhost:5000/config/attr-distribution-set', json=SEX_DISTINCT_DISTRIBUTION)
        sex_distinct_distribution_set = res.json()

        # unisex distribution
        res = requests.post('http://localhost:5000/config/attr-distribution-set', json=UNISEX_DISTRIBUTION)
        unisex_distribution_set = res.json()

        # unismoker distribution
        res = requests.post('http://localhost:5000/config/attr-distribution-set', json=SMOKER_DISTINCT_DISTRIBUTION)
        smoker_distinct_distribution_set = res.json()
        
        # unismoker distribution
        res = requests.post('http://localhost:5000/config/attr-distribution-set', json=UNISMOKER_DISTRIBUTION)
        unismoker_distribution_set = res.json()
        
        # product variation
        res = requests.post('http://localhost:5000/config/product-variations', json={
            **CONFIG_PRODUCT_VARIATION, 
            "age_distribution_set_id": age_distribution_set['age_distribution_set_id'], 
            "sex_distinct_distribution_set_id": sex_distinct_distribution_set['attr_distribution_set_id'], 
            "smoker_distinct_distribution_set_id": smoker_distinct_distribution_set['attr_distribution_set_id'], 
            "unisex_distribution_set_id": unisex_distribution_set['attr_distribution_set_id'], 
            "unismoker_distribution_set_id": unismoker_distribution_set['attr_distribution_set_id'], 
            "product_id": product['product_id']
        })
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

        try: 
            # benefits
            benefits = []
            for bnft in CONFIG_BENEFIT: 
                res = requests.post('http://localhost:5000/config/benefit', json={
                    **bnft, 
                    "child_states": [{**child, "product_id": product['product_id']} for child in bnft['child_states']], 
                    "product_id": product['product_id'], 
                    "rate_group_id": rate_group['rate_group_id'], 
                    "coverage_id": coverage['coverage_id']
                })
                benefits.append(res.json())
        except Exception as e: 
            print("BENEFITS ERROR")

        try: 
            # provisions
            provisions = []
            for prov in CONFIG_PROVISION: 
                res = requests.post('http://localhost:5000/config/provision', json={
                    **prov, 
                    "product_id": product['product_id'], 
                })
                provisions.append(res.json())
        except Exception as e: 
            print("PROVISION ERROR")

        # provision ui
        for prov_code, ui in CONFIG_PROVISION_UI.items(): 
            res = requests.post('http://localhost:5000/config/provision-ui-component', json={
                **ui, 
                "provision_id": [prov['provision_id'] for prov in provisions if prov['provision_code'] == prov_code][0], 
            })
            

        # factors
        for prov_code, factors in CONFIG_FACTORS.items(): 
            res = requests.post('http://localhost:5000/config/factors', json=[
                {
                    **factor, 
                    "provision_id": [prov['provision_id'] for prov in provisions if prov['provision_code'] == prov_code][0], 
                } for factor in factors]
            )
            

        try: 
            # benefit product variation
            for bnft in benefits: 
                res = requests.post('http://localhost:5000/config/benefit-product-variations', json=[{
                    "product_variation_id": product_variation['product_variation_id'], 
                    "benefit_id": bnft['benefit_id']
                }])
        except Exception as e: 
            print("BENEFIT PRODUCT VARIATION ERROR")
        
        try: 
            # benefit provision
            for bnft in benefits: 
                for prov in provisions: 
                    res = requests.post('http://localhost:5000/config/benefit-provisions', json={
                        "provision_id": prov['provision_id'], 
                        "benefit_id": bnft['benefit_id']
                    })
        except Exception as e: 
            print("BENEFIT PROVISION ERROR")

        return "Data loaded", 200
