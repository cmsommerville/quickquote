from app.extensions import db
from app.shared import BaseModel

from .constants import TBL_NAMES

REF_RATING_ALGORITHM = TBL_NAMES['REF_RATING_ALGORITHM']

class Model_RefRatingAlgorithm(BaseModel):
    __tablename__ = REF_RATING_ALGORITHM

    rating_algorithm_code = db.Column(db.String(30), primary_key=True)
    rating_algorithm_label = db.Column(db.String(100))
    rating_algorithm_description = db.Column(db.String(1000))
