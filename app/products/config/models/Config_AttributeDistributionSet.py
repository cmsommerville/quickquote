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
    is_composite_default_dist = db.Column(db.Boolean(), default=False)

    attr_distribution = db.relationship("Model_ConfigAttributeDistribution")

    @classmethod
    def find_by_attr_type(cls, attr_type, is_composite_default_dist=False): 
        return cls.query.filter(cls.attr_type_code == attr_type, cls.is_composite_default_dist == is_composite_default_dist).all()
