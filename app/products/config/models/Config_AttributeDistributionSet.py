from app.extensions import db
from app.shared import BaseModel
from sqlalchemy.ext.hybrid import hybrid_method

from ...__constants__ import TBL_NAMES

CONFIG_ATTRIBUTE_DISTRIBUTION_SET = TBL_NAMES['CONFIG_ATTRIBUTE_DISTRIBUTION_SET']

class Model_ConfigAttributeDistributionSet(BaseModel):
    __tablename__ = CONFIG_ATTRIBUTE_DISTRIBUTION_SET

    attr_distribution_set_id = db.Column(db.Integer, primary_key=True)
    attr_type_code = db.Column(db.String(), nullable=False)
    attr_distribution_set_label = db.Column(db.String(100), nullable=False)

    attr_distribution = db.relationship("Model_ConfigAttributeDistribution")

