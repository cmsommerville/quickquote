from app.extensions import db
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES

CONFIG_AGE_DISTRIBUTION_SET = TBL_NAMES['CONFIG_AGE_DISTRIBUTION_SET']

class Model_ConfigAgeDistributionSet(BaseModel):
    __tablename__ = CONFIG_AGE_DISTRIBUTION_SET

    age_distribution_set_id = db.Column(db.Integer, primary_key=True)
    age_distribution_set_label = db.Column(db.String(100))

    age_distribution = db.relationship("Model_ConfigAgeDistribution")

