from app.extensions import db
from app.shared import BaseModel

from .constants import TBL_NAMES

CONFIG_AGE_BANDS = TBL_NAMES['CONFIG_AGE_BANDS']
CONFIG_AGE_BANDS_SET = TBL_NAMES['CONFIG_AGE_BANDS_SET']

class Model_ConfigAgeBand(BaseModel):
    __tablename__ = CONFIG_AGE_BANDS
    __table_args__ = (
        db.UniqueConstraint('age_band_set_id', 'age_band_lower'),
        db.CheckConstraint('age_band_lower <= age_band_upper')
    )

    age_band_id = db.Column(db.Integer, primary_key=True)
    age_band_set_id = db.Column(db.ForeignKey(f"{CONFIG_AGE_BANDS_SET}.age_band_set_id"))
    age_band_lower = db.Column(db.Integer, nullable=False)
    age_band_upper = db.Column(db.Integer, nullable=False)

