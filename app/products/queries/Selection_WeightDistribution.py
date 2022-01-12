from sqlalchemy.orm import aliased, contains_eager, Query
from sqlalchemy import and_, between, literal
from app.extensions import db

from ..config.models import Model_ConfigAgeDistribution, Model_ConfigAttributeDistribution,\
    Model_ConfigProductVariation
from ..selections.models import Model_SelectionAgeBands, Model_SelectionPlan

def query_config_weight_distribution(
    plan: Model_SelectionPlan, 
    product_variation: Model_ConfigProductVariation) -> Query: 

    Gender = aliased(Model_ConfigAttributeDistribution)
    SmokerStatus = aliased(Model_ConfigAttributeDistribution)
    Age = aliased(Model_ConfigAgeDistribution)

    sqry = db.session.query(
        Age.age.label("age"), 
        Age.weight.label("age_weight"))\
        .filter(
            Age.age_distribution_set_id == product_variation.age_distribution_set_id,
        ).subquery()


    # cross join to smoker status
    if plan.is_smoker_distinct: 
        sqry = db.session.query(
                sqry, SmokerStatus.attr_value.label("smoker_status"), 
                SmokerStatus.weight.label("smoker_weight"))\
            .filter(SmokerStatus.attr_distribution_set_id == product_variation.smoker_distinct_distribution_set_id)\
            .join(SmokerStatus, literal(True)).subquery()
    else: 
        sqry = db.session.query(
                sqry, SmokerStatus.attr_value.label("smoker_status"), 
                SmokerStatus.weight.label("smoker_weight"))\
            .filter(SmokerStatus.attr_distribution_set_id == product_variation.unismoker_distribution_set_id)\
            .join(SmokerStatus, literal(True)).subquery()
        
    
    # cross join to gender
    if plan.is_gender_distinct: 
        qry = db.session.query(
                sqry, Gender.attr_value.label("gender"), 
                Gender.weight.label("gender_weight"))\
            .filter(Gender.attr_distribution_set_id == product_variation.sex_distinct_distribution_set_id)\
            .join(Gender, literal(True))
    else: 
        qry = db.session.query(
                sqry, Gender.attr_value.label("gender"), 
                Gender.weight.label("gender_weight"))\
            .filter(Gender.attr_distribution_set_id == product_variation.unisex_distribution_set_id)\
            .join(Gender, literal(True))
        
    qry = qry.add_columns((sqry.c.age_weight * sqry.c.smoker_weight * Gender.weight).label("weight"))

    return qry