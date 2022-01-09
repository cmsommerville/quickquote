from app.extensions import db
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES

CONFIG_GENDER_DISTRIBUTION = TBL_NAMES['CONFIG_GENDER_DISTRIBUTION']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']

class Model_ConfigGenderDistribution(BaseModel):
    __tablename__ = CONFIG_GENDER_DISTRIBUTION
    __table_args__ = (
        db.UniqueConstraint('product_id', 'gender_code'),
    )

    gender_distribution_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.product_id", onupdate="CASCADE", ondelete="CASCADE"))
    gender_code = db.Column(db.String(1), nullable=False)
    weight = db.Column(db.Numeric(12,5), nullable=False)

