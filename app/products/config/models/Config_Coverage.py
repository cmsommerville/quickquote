import datetime
from sqlalchemy import between
from sqlalchemy.orm import aliased
from app.extensions import db
from app.shared import BaseVersionedModel, BaseModel

from .constants import TBL_NAMES, COVERAGE_SECTION_DEFAULT
from .Config_States import Model_RefStates

REF_COVERAGE = TBL_NAMES['REF_COVERAGE']
REF_STATE = TBL_NAMES['REF_STATE']
CONFIG_COVERAGE = TBL_NAMES['CONFIG_COVERAGE']
CONFIG_COVERAGE_STATE_AVAILABILITY = TBL_NAMES['CONFIG_COVERAGE_STATE_AVAILABILITY']
CONFIG_PLAN = TBL_NAMES['CONFIG_PLAN']


class Model_RefCoverage(BaseModel):
    __tablename__ = REF_COVERAGE

    coverage_code = db.Column(db.String(30), primary_key=True)
    coverage_label = db.Column(db.String(100))

    def __repr__(self):
        return f"<Coverage Code: {self.coverage_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.coverage_code == code).first()


class Model_ConfigCoverage(BaseVersionedModel):
    __tablename__ = CONFIG_COVERAGE

    coverage_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey(f"{CONFIG_PLAN}.plan_id"))
    coverage_code = db.Column(
        db.String(30), db.ForeignKey(f"{REF_COVERAGE}.coverage_code"))
    coverage_effective_date = db.Column(db.Date(), nullable=False)
    coverage_expiration_date = db.Column(db.Date(), nullable=False)
    section_code = db.Column(db.String(30), default=COVERAGE_SECTION_DEFAULT)

    plan = db.relationship(
        "Model_ConfigPlan", back_populates="coverages")
    coverage = db.relationship("Model_RefCoverage")
    states = db.relationship("Model_ConfigCoverageStateAvailability", back_populates="coverage",
                             primaryjoin="""and_(
                                 Model_ConfigCoverage.coverage_id == Model_ConfigCoverageStateAvailability.coverage_id,
                                 Model_ConfigCoverageStateAvailability.active_record_indicator == 'Y'
                                )""")
    benefits = db.relationship("Model_ConfigBenefit", back_populates="coverage",
                               primaryjoin="""and_(
                                 Model_ConfigCoverage.coverage_id == Model_ConfigBenefit.coverage_id,
                                 Model_ConfigBenefit.active_record_indicator == 'Y'
                                )""")

    def __repr__(self):
        return f"<Coverage Id: {self.coverage_id}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.coverage_id == id).first()

    @classmethod
    def find_by_state(
        cls,
        state: str,
        effective_date: datetime.date,
        default_state: str = "XX",
        as_of_date: datetime.datetime = datetime.datetime(9999, 12, 31)
    ):
        # filter for coverage records
        qry_coverage = cls.query.filter(
            between(effective_date, cls.coverage_effective_date,
                    cls.coverage_expiration_date),
            between(as_of_date, cls.row_eff_dts, cls.row_exp_dts)
        )

        # subquery coverage state availability
        CSA = Model_ConfigCoverageStateAvailability.find_by_state(
            state, effective_date, default_state, as_of_date)

        # join coverage and CSA
        qry_coverage = qry_coverage.join(
            CSA, cls.coverage_id == CSA.c.coverage_id)

        return qry_coverage.all()


class Model_ConfigCoverageStateAvailability(BaseVersionedModel):
    __tablename__ = CONFIG_COVERAGE_STATE_AVAILABILITY

    coverage_state_availability_id = db.Column(db.Integer, primary_key=True)
    coverage_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_COVERAGE}.coverage_id"))
    state_code = db.Column(
        db.String(2), db.ForeignKey(f"{REF_STATE}.state_code"))
    state_effective_date = db.Column(db.Date, nullable=False)
    state_expiration_date = db.Column(db.Date, nullable=False)

    coverage = db.relationship("Model_ConfigCoverage", back_populates="states")

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.coverage_state_availability_id == id).first()

    @classmethod
    def find_by_state(
        cls,
        state: str,
        effective_date: datetime.date,
        default_state: str = 'XX',
        as_of_date: datetime.datetime = datetime.datetime(9999, 12, 31)
    ):
        """
        If cannot find specific state, query for the default state. 
        """
        base_qry = cls.query.filter(
            between(as_of_date, cls.row_eff_dts, cls.row_exp_dts)
        )
        qry = base_qry.filter(cls.state_code == state)
        if qry.first() is None:
            qry = base_qry.filter(cls.state_code == default_state)

        return qry.filter(
            between(effective_date, cls.state_effective_date,
                    cls.state_expiration_date)
        ).subquery()
