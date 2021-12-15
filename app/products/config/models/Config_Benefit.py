import datetime
from sqlalchemy import DDL, event, between, or_
from marshmallow import ValidationError
from app.extensions import db
from app.shared import BaseModel

from .constants import TBL_NAMES, FACTOR_DECIMAL_PRECISION

REF_BENEFIT = TBL_NAMES['REF_BENEFIT']
REF_BENEFIT_DURATION = TBL_NAMES['REF_BENEFIT_DURATION']
REF_BENEFIT_DURATION_ITEMS = TBL_NAMES['REF_BENEFIT_DURATION_ITEMS']
REF_STATE = TBL_NAMES['REF_STATE']
REF_UNIT_CODE = TBL_NAMES['REF_UNIT_CODE']
CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_BENEFIT_DURATION = TBL_NAMES['CONFIG_BENEFIT_DURATION']
CONFIG_BENEFIT_DURATION_ITEMS = TBL_NAMES['CONFIG_BENEFIT_DURATION_ITEMS']
CONFIG_BENEFIT_PRODUCT_VARIATION_APPLICABILITY = TBL_NAMES['CONFIG_BENEFIT_PRODUCT_VARIATION_APPLICABILITY']
CONFIG_BENEFIT_STATE_AVAILABILITY = TBL_NAMES['CONFIG_BENEFIT_STATE_AVAILABILITY']
CONFIG_COVERAGE = TBL_NAMES['CONFIG_COVERAGE']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PRODUCT_VARIATIONS = TBL_NAMES['CONFIG_PRODUCT_VARIATIONS']
CONFIG_RATE_GROUP = TBL_NAMES['CONFIG_RATE_GROUP']


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


class Model_ConfigBenefit(BaseModel):
    __tablename__ = CONFIG_BENEFIT
    __table_args__ = (
        db.UniqueConstraint('benefit_code', 'state_id'),
        db.CheckConstraint('benefit_effective_date <= benefit_expiration_date'),
    )

    benefit_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.ForeignKey(
        f"{CONFIG_PRODUCT}.product_id"))
    coverage_id = db.Column(db.ForeignKey(
        f"{CONFIG_COVERAGE}.coverage_id"), nullable=False)
    rate_group_id = db.Column(db.ForeignKey(
        f"{CONFIG_RATE_GROUP}.rate_group_id"), nullable=False)
    state_id = db.Column(db.ForeignKey(
        f"{REF_STATE}.state_id"), nullable=False)
    benefit_code = db.Column(db.ForeignKey(
        f"{REF_BENEFIT}.benefit_code"), nullable=False)
    benefit_effective_date = db.Column(db.Date(), nullable=False)
    benefit_expiration_date = db.Column(db.Date(), nullable=False)
    min_value = db.Column(db.Numeric(12, 2), nullable=False)
    max_value = db.Column(db.Numeric(12, 2), nullable=False)
    step_value = db.Column(db.Numeric(12, 4), nullable=False)
    unit_code = db.Column(db.String(30), db.ForeignKey(
        f"{REF_UNIT_CODE}.unit_code"), nullable=False)
    is_durational = db.Column(db.Boolean, default=False)

    product = db.relationship(
        "Model_ConfigProduct", back_populates="benefits")
    product_variations = db.relationship(
        "Model_ConfigBenefitProductVariation", back_populates="benefit")
    coverage = db.relationship(
        "Model_ConfigCoverage", back_populates="benefits")
    benefit = db.relationship("Model_RefBenefit")
    rate_group = db.relationship("Model_ConfigRateGroup")
    durations = db.relationship(
        "Model_ConfigBenefitDuration", back_populates="benefit")
    state = db.relationship("Model_RefStates")
    benefit_states = db.relationship(
        "Model_ConfigBenefitStateAvailability", back_populates="benefit")

    def __repr__(self):
        return f"<Benefit Id: {self.benefit_id}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.benefit_id == id).first()

    @classmethod
    def find_by_product(cls, id: int):
        return cls.query.filter(cls.product_id == id).all()

    @classmethod
    def find_all_state_benefit(cls, benefit_code: str):
        return cls.query.filter(cls.benefit_code == benefit_code, cls.state_id == 0).first()

    @classmethod
    def count_specific_state_benefit(cls, 
        benefit_code: str, 
        state_id: int, 
        effective_date: datetime.date, 
        expiration_date: datetime.date
    ):
        return cls.query.filter(
            cls.benefit_code == benefit_code, 
            cls.state_id == state_id, 
            or_(
                between(effective_date, cls.benefit_effective_date, cls.benefit_expiration_date), 
                between(expiration_date, cls.benefit_effective_date, cls.benefit_expiration_date)
            )
        ).count()

    def _state_handler(self, 
        state_id: id, 
        benefit_code: str, 
        benefit_effective_date: datetime.date
    ): 
        # if adding a state specific benefit configuration
        if state_id > 0: 
            # lookup the benefit id associated with 'all' states
            expireBenefitState = self.find_all_state_benefit(benefit_code)
            expire_benefit_id = expireBenefitState.benefit_id

            # expire the state 
            Model_ConfigBenefitStateAvailability.expire_state(
                expire_benefit_id, state_id, benefit_effective_date - datetime.timedelta(days=1))

    def save_to_db(self):
        # get incoming state and benefit
        state_id = self.state_id
        benefit_code = self.benefit_code
        benefit_effective_date = self.benefit_effective_date
        
        try: 
            self._state_handler(state_id, benefit_code, benefit_effective_date)
        except: 
            db.session.rollback()
            raise

        try:
            db.session.add(self)
        except Exception:
            db.session.rollback()
            raise

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        

class Model_ConfigBenefitStateAvailability(BaseModel):
    __tablename__ = CONFIG_BENEFIT_STATE_AVAILABILITY
    __table_args__ = (
        db.UniqueConstraint('benefit_id', 'state_id', 'state_effective_date'),
        db.CheckConstraint('state_effective_date <= state_expiration_date'),
    )

    benefit_state_availability_id = db.Column(db.Integer, primary_key=True)
    benefit_id = db.Column(db.ForeignKey(f"{CONFIG_BENEFIT}.benefit_id"), nullable=False)
    state_id = db.Column(db.ForeignKey(
        f"{REF_STATE}.state_id"), nullable=False)
    state_effective_date = db.Column(db.Date(), nullable=False)
    state_expiration_date = db.Column(db.Date(), nullable=False)

    benefit = db.relationship("Model_ConfigBenefit", 
        primaryjoin="and_(Model_ConfigBenefitStateAvailability.benefit_id == Model_ConfigBenefit.benefit_id, Model_ConfigBenefit.state_id == 0)")
    state = db.relationship("Model_RefStates")

    def __repr__(self):
        return f"<Benefit State Availability Id: {self.benefit_state_availability_id}>"

    @classmethod
    def find(cls, id: int):
        return cls.query.filter(cls.benefit_state_availability_id == id).first()

    @classmethod
    def find_by_benefit(cls, id: int):
        return cls.query.filter(cls.benefit_id == id).all()

    def _state_handler(self, benefit_code: str): 
        # check if any benefits associated with specific state
        existingBenefitStateCount = Model_ConfigBenefit.count_specific_state_benefit(
            benefit_code, 
            self.state_id, 
            self.state_effective_date, 
            self.state_expiration_date
        )
        if existingBenefitStateCount > 0:
            raise ValidationError("A state-specific benefit has already been configured")

    def save_to_db(self):
        # get incoming benefit
        benefit_code = Model_ConfigBenefit.find(self.benefit_id).benefit_code
        
        try: 
            self._state_handler(benefit_code)
        except: 
            db.session.rollback()
            raise

        try:
            db.session.add(self)
        except Exception:
            db.session.rollback()
            raise

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        
    @classmethod
    def expire_state(cls, benefit_id: int, state_id: int, expiration_date: datetime.date):
        try: 
            cls.query.filter(cls.benefit_id == benefit_id, cls.state_id == state_id).update({cls.state_expiration_date: expiration_date})
        except:
            cls.query.filter(cls.benefit_id == benefit_id, cls.state_id == state_id).delete()
        return True


class Model_ConfigBenefitProductVariation(BaseModel):
    __tablename__ = CONFIG_BENEFIT_PRODUCT_VARIATION_APPLICABILITY

    benefit_id = db.Column(db.ForeignKey(f"{CONFIG_BENEFIT}.benefit_id"), primary_key=True)
    product_variation_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT_VARIATIONS}.product_variation_id"), primary_key=True)

    benefit = db.relationship(
        "Model_ConfigBenefit", back_populates="product_variations")
    product_variation = db.relationship(
        "Model_ConfigProductVariations", back_populates="benefits")

    def __repr__(self):
        return f"<Benefit Id: {self.benefit_id} - Variation ID: {self.product_variation_id}>"

    @classmethod
    def find_benefits(cls, id):
        return cls.query.filter(cls.benefit_id == id).all()

    @classmethod
    def find_product_variations(cls, id):
        return cls.query.filter(cls.product_variation_id == id).all()


class Model_ConfigBenefitDuration(BaseModel):
    __tablename__ = CONFIG_BENEFIT_DURATION
    __table_args__ = (
        db.UniqueConstraint('benefit_id', 'benefit_duration_code'),
    )

    benefit_duration_id = db.Column(db.Integer, primary_key=True)
    benefit_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_BENEFIT}.benefit_id"))
    benefit_duration_code = db.Column(
        db.String(30), db.ForeignKey(f"{REF_BENEFIT_DURATION}.duration_code"))

    benefit = db.relationship("Model_ConfigBenefit",
                              back_populates="durations")
    duration = db.relationship("Model_RefBenefitDuration")
    duration_items = db.relationship(
        "Model_ConfigBenefitDurationItems", back_populates="duration", lazy="joined")

    def __repr__(self):
        return f"<Benefit Duration Id: {self.benefit_duration_id}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.benefit_duration_id == id).first()

    @classmethod
    def find_by_benefit(cls, id):
        return cls.query.filter(cls.benefit_id == id).all()


class Model_ConfigBenefitDurationItems(BaseModel):
    __tablename__ = CONFIG_BENEFIT_DURATION_ITEMS
    __table_args__ = (
        db.UniqueConstraint('benefit_duration_id', 'item_code'),
    )

    benefit_duration_item_id = db.Column(db.Integer, primary_key=True)
    benefit_duration_id = db.Column(db.ForeignKey(f"{CONFIG_BENEFIT_DURATION}.benefit_duration_id"), nullable=False)
    item_code = db.Column(db.ForeignKey(f"{REF_BENEFIT_DURATION_ITEMS}.item_code"), nullable=False)
    benefit_duration_factor = db.Column(
        db.Numeric(FACTOR_DECIMAL_PRECISION + 3, FACTOR_DECIMAL_PRECISION), nullable=False)

    duration = db.relationship(
        "Model_ConfigBenefitDuration", back_populates="duration_items")

    duration_item = db.relationship("Model_RefBenefitDurationItems")
        
    def __repr__(self):
        return f"<Benefit Duration Item Id: {self.benefit_duration_item_id}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.benefit_duration_item_id == id).first()
