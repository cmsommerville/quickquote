from app.extensions import db
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES

CONFIG_AGE_DISTRIBUTION = TBL_NAMES['CONFIG_AGE_DISTRIBUTION']
CONFIG_AGE_DISTRIBUTION_SET = TBL_NAMES['CONFIG_AGE_DISTRIBUTION_SET']

class Model_ConfigAgeDistribution(BaseModel):
    __tablename__ = CONFIG_AGE_DISTRIBUTION
    __table_args__ = (
        db.UniqueConstraint('age_distribution_set_id', 'age'),
    )

    age_distribution_id = db.Column(db.Integer, primary_key=True)
    age_distribution_set_id = db.Column(db.ForeignKey(f'{CONFIG_AGE_DISTRIBUTION_SET}.age_distribution_set_id', onupdate="CASCADE", ondelete="CASCADE"))
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Numeric(12,5), nullable=False)

