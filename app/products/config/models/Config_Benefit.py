import datetime
from sqlalchemy import between
from sqlalchemy.ext.hybrid import hybrid_method
from app.extensions import db
from app.shared import BaseVersionedModel, BaseModel

from .constants import TBL_NAMES, FACTOR_DECIMAL_PRECISION
from .Config_States import Model_RefStates

REF_BENEFIT = TBL_NAMES['REF_BENEFIT']
REF_BENEFIT_DURATION = TBL_NAMES['REF_BENEFIT_DURATION']
REF_BENEFIT_DURATION_ITEMS = TBL_NAMES['REF_BENEFIT_DURATION_ITEMS']
REF_STATE = TBL_NAMES['REF_STATE']
REF_UNIT_CODE = TBL_NAMES['REF_UNIT_CODE']
CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_BENEFIT_DURATION = TBL_NAMES['CONFIG_BENEFIT_DURATION']
CONFIG_BENEFIT_DURATION_ITEMS = TBL_NAMES['CONFIG_BENEFIT_DURATION_ITEMS']
CONFIG_BENEFIT_DURATION_ITEM_STATE_AVAILABILITY = TBL_NAMES[
    'CONFIG_BENEFIT_DURATION_ITEM_STATE_AVAILABILITY']
CONFIG_BENEFIT_STATE_AVAILABILITY = TBL_NAMES['CONFIG_BENEFIT_STATE_AVAILABILITY']
CONFIG_COVERAGE = TBL_NAMES['CONFIG_COVERAGE']


class Model_RefBenefit(BaseModel):
    __tablename__ = REF_BENEFIT

    benefit_code = db.Column(db.String(30), primary_key=True)
    benefit_label = db.Column(db.String(100))

    def __repr__(self):
        return f"<Benefit Code: {self.benefit_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.benefit_code == code).first()


class Model_RefUnitCode(BaseModel):
    __tablename__ = REF_UNIT_CODE

    unit_code = db.Column(db.String(30), primary_key=True)
    unit_label = db.Column(db.String(100))

    def __repr__(self):
        return f"<Unit Code: {self.unit_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.unit_code == code).first()


class Model_RefBenefitDuration(BaseModel):
    __tablename__ = REF_BENEFIT_DURATION

    duration_code = db.Column(db.String(30), primary_key=True)
    duration_label = db.Column(db.String(100))

    def __repr__(self):
        return f"<Duration Code: {self.duration_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.duration_code == code).first()


class Model_RefBenefitDurationItems(BaseModel):
    __tablename__ = REF_BENEFIT_DURATION_ITEMS

    item_code = db.Column(db.String(30), primary_key=True)
    item_label = db.Column(db.String(100))

    def __repr__(self):
        return f"<Item Code: {self.item_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.item_code == code).first()


class Model_ConfigBenefit(BaseVersionedModel):
    __tablename__ = CONFIG_BENEFIT

    benefit_id = db.Column(db.Integer, primary_key=True)
    coverage_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_COVERAGE}.coverage_id"), nullable=False)
    benefit_code = db.Column(
        db.String(30), db.ForeignKey(f"{REF_BENEFIT}.benefit_code"), nullable=False)
    benefit_effective_date = db.Column(db.Date(), nullable=False)
    benefit_expiration_date = db.Column(db.Date(), nullable=False)
    min_value = db.Column(db.Numeric(2), nullable=False)
    max_value = db.Column(db.Numeric(2), nullable=False)
    step_value = db.Column(db.Numeric(2), nullable=False)
    unit_code = db.Column(db.String(30), db.ForeignKey(
        f"{REF_UNIT_CODE}.unit_code"), nullable=False)

    coverage = db.relationship(
        "Model_ConfigCoverage", back_populates="benefits")
    benefit = db.relationship("Model_RefBenefit")
    states = db.relationship("Model_ConfigBenefitStateAvailability", back_populates="benefit",
                             primaryjoin="""and_(
                                 Model_ConfigBenefit.benefit_id == Model_ConfigBenefitStateAvailability.benefit_id,
                                 Model_ConfigBenefitStateAvailability.active_record_indicator == 'Y'
                                )""")

    @hybrid_method
    def check_valid_state(
        self,
        state: str,
        effective_date: datetime.date,
        as_of_date: datetime.datetime = datetime.datetime(9999, 12, 31)
    ):
        return Model_ConfigBenefitStateAvailability.check_valid_state(
            self.benefit_id, state, effective_date, as_of_date
        )

    def __repr__(self):
        return f"<Benefit Id: {self.benefit_id}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.benefit_id == id).first()


class Model_ConfigBenefitStateAvailability(BaseVersionedModel):
    __tablename__ = CONFIG_BENEFIT_STATE_AVAILABILITY

    benefit_state_availability_id = db.Column(db.Integer, primary_key=True)
    benefit_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_BENEFIT}.benefit_id"))
    state_code = db.Column(
        db.String(2), db.ForeignKey(f"{REF_STATE}.state_code"))
    state_effective_date = db.Column(db.Date, nullable=False)
    state_expiration_date = db.Column(db.Date, nullable=False)
    min_value = db.Column(db.Numeric(2), nullable=False)
    max_value = db.Column(db.Numeric(2), nullable=False)
    step_value = db.Column(db.Numeric(2), nullable=False)
    unit_code = db.Column(db.String(30), db.ForeignKey(
        f"{REF_UNIT_CODE}.unit_code"), nullable=False)

    benefit = db.relationship("Model_ConfigBenefit", back_populates="states")
    durations = db.relationship(
        "Model_ConfigBenefitDuration", back_populates="benefit", lazy="joined",
        primaryjoin="""and_(
            Model_ConfigBenefitStateAvailability.benefit_state_availability_id == Model_ConfigBenefitDuration.benefit_state_availability_id,
            Model_ConfigBenefitDuration.active_record_indicator == 'Y'
        )""")

    def __repr__(self):
        return f"<Benefit Id: {self.benefit_id} - State: {self.state_code}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.benefit_state_availability_id == id).first()

    @classmethod
    def check_valid_state(
        cls,
        benefit_id: int,
        state: str,
        effective_date: datetime.date,
        as_of_date: datetime.datetime = datetime.datetime(9999, 12, 31)
    ):
        """
        For a specific benefit ID, filter for the specific state. If not there, 
        look for the default state value. Then filter, for the effective date. 

        There should be a record if the state is valid.
        """
        base_qry = cls.query.filter(
            cls.benefit_id == benefit_id,
            between(as_of_date, cls.row_eff_dts, cls.row_exp_dts))
        qry = base_qry.filter(cls.state_code == state)
        if qry.first() is None:
            qry = base_qry.filter(cls.state_code == 'XX')

        qry = qry.filter(
            between(effective_date, cls.state_effective_date, cls.state_expiration_date))
        return qry.first() is not None

    @classmethod
    def find_by_state(cls, state: str, effective_date: datetime.date = None, active_record_indicator: str = "Y"):
        qry = cls.query.filter(
            cls.state_code == state, cls.active_record_indicator == active_record_indicator)
        if effective_date:
            return qry.filter(between(effective_date, cls.state_effective_date, cls.state_expiration_date)).all()
        return qry.all()


class Model_ConfigBenefitDuration(BaseVersionedModel):
    __tablename__ = CONFIG_BENEFIT_DURATION

    benefit_duration_id = db.Column(db.Integer, primary_key=True)
    benefit_state_availability_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_BENEFIT_STATE_AVAILABILITY}.benefit_state_availability_id"))
    benefit_duration_code = db.Column(
        db.String(2), db.ForeignKey(f"{REF_BENEFIT_DURATION}.duration_code"))

    benefit = db.relationship("Model_ConfigBenefitStateAvailability",
                              back_populates="durations")
    duration_items = db.relationship(
        "Model_ConfigBenefitDurationItems", back_populates="duration", lazy="joined",
        primaryjoin="""and_(
            Model_ConfigBenefitDuration.benefit_duration_id == Model_ConfigBenefitDurationItems.benefit_duration_id,
            Model_ConfigBenefitDurationItems.active_record_indicator == 'Y'
        )""")

    def __repr__(self):
        return f"<Benefit Duration Id: {self.benefit_duration_id}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.benefit_duration_id == id).first()


class Model_ConfigBenefitDurationItems(BaseVersionedModel):
    __tablename__ = CONFIG_BENEFIT_DURATION_ITEMS

    benefit_duration_item_id = db.Column(db.Integer, primary_key=True)
    benefit_duration_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_BENEFIT_DURATION}.benefit_duration_id"), nullable=False)
    item_code = db.Column(
        db.String(2), db.ForeignKey(f"{REF_BENEFIT_DURATION_ITEMS}.item_code"), nullable=False)
    benefit_duration_factor = db.Column(
        db.Numeric(FACTOR_DECIMAL_PRECISION), nullable=False)

    duration = db.relationship(
        "Model_ConfigBenefitDuration", back_populates="duration_items")
    states = db.relationship("Model_ConfigBenefitDurationItemStateAvailability", back_populates="duration_item",
                             primaryjoin="""and_(
                                 Model_ConfigBenefitDurationItems.benefit_duration_item_id == Model_ConfigBenefitDurationItemStateAvailability.benefit_duration_item_id,
                                 Model_ConfigBenefitDurationItemStateAvailability.active_record_indicator == 'Y'
                                )""")

    def __repr__(self):
        return f"<Benefit Duration Item Id: {self.benefit_duration_item_id}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.benefit_duration_item_id == id).first()


class Model_ConfigBenefitDurationItemStateAvailability(BaseVersionedModel):
    __tablename__ = CONFIG_BENEFIT_DURATION_ITEM_STATE_AVAILABILITY

    benefit_duration_item_state_availability_id = db.Column(
        db.Integer, primary_key=True)
    benefit_duration_item_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_BENEFIT_DURATION_ITEMS}.benefit_duration_item_id"), nullable=False)
    state_code = db.Column(
        db.String(2), db.ForeignKey(f"{REF_STATE}.state_code"), nullable=False)
    state_effective_date = db.Column(db.Date, nullable=False)
    state_expiration_date = db.Column(db.Date, nullable=False)

    duration_item = db.relationship("Model_ConfigBenefitDurationItems",
                                    back_populates="states")

    def __repr__(self):
        return f"<Benefit Duration Item State Availability ID: {self.benefit_duration_item_state_availability_id}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.benefit_duration_item_state_availability_id == id).first()

    @classmethod
    def find_by_state(cls, state: str, effective_date: datetime.date = None, active_record_indicator: str = "Y"):
        qry = cls.query.filter(
            cls.state_code == state, cls.active_record_indicator == active_record_indicator)
        if effective_date:
            return qry.filter(between(effective_date, cls.state_effective_date, cls.state_expiration_date)).all()
        return qry.all()
