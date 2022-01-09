from app.extensions import db
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES

CONFIG_ATTRIBUTE_DISTRIBUTION = TBL_NAMES['CONFIG_ATTRIBUTE_DISTRIBUTION']
CONFIG_ATTRIBUTE_DISTRIBUTION_SET = TBL_NAMES['CONFIG_ATTRIBUTE_DISTRIBUTION_SET']

class Model_ConfigAttributeDistribution(BaseModel):
    __tablename__ = CONFIG_ATTRIBUTE_DISTRIBUTION
    __table_args__ = (
        db.UniqueConstraint('attr_distribution_set_id', 'attr_value'),
    )

    attr_distribution_id = db.Column(db.Integer, primary_key=True)
    attr_distribution_set_id = db.Column(db.ForeignKey(f"{CONFIG_ATTRIBUTE_DISTRIBUTION_SET}.attr_distribution_set_id", onupdate="CASCADE", ondelete="CASCADE"))
    attr_value = db.Column(db.String(30), nullable=False)
    weight = db.Column(db.Numeric(12,5), nullable=False)

