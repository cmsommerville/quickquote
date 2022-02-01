from sqlalchemy.orm import aliased, contains_eager, Query
from sqlalchemy import and_, between
from app.extensions import db

from ..config.models import Model_ConfigAgeBandSet, Model_ConfigProductVariation

def query_config_age_bands(product_id: int) -> Query: 
    # base query
    qry = db.session.query(Model_ConfigAgeBandSet)

    # join to product variation
    qry = qry.join(Model_ConfigProductVariation)

    # filter on product variation and state, but not effective date YET
    qry = qry.filter(
            Model_ConfigProductVariation.product_id == product_id
        )

    return qry
