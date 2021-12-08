import datetime
from sqlalchemy import between
from sqlalchemy.orm import contains_eager, aliased
from app.extensions import db
from app.shared import BaseModel, BaseModel

from .constants import TBL_NAMES, COVERAGE_SECTION_DEFAULT
from .Config_Benefit import Model_ConfigBenefit

REF_COVERAGE = TBL_NAMES['REF_COVERAGE']
REF_STATE = TBL_NAMES['REF_STATE']
CONFIG_COVERAGE = TBL_NAMES['CONFIG_COVERAGE']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']

class Model_ConfigCoverage(BaseModel):
    __tablename__ = CONFIG_COVERAGE
    __table_args__ = (
        db.UniqueConstraint('coverage_code'),
    )

    coverage_id = db.Column(db.Integer, primary_key=True)
    coverage_code = db.Column(db.String(30), nullable=False)
    coverage_label = db.Column(db.String(100), nullable=False)
    section_code = db.Column(db.String(30), default=COVERAGE_SECTION_DEFAULT)

    benefits = db.relationship("Model_ConfigBenefit", back_populates="coverage")

    def __repr__(self):
        return f"<Coverage ID: {self.coverage_id} - {self.coverage_code}>"
