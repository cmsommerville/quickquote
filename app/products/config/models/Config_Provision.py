import datetime
from sqlalchemy import between
from app.extensions import db
from app.shared import BaseVersionedModel, BaseModel

from .constants import TBL_NAMES

REF_COMPONENT_TYPES = TBL_NAMES["REF_COMPONENT_TYPES"]
REF_PROVISION = TBL_NAMES['REF_PROVISION']
REF_STATE = TBL_NAMES['REF_STATE']
REF_TEXT_FIELD_TYPES = TBL_NAMES['REF_TEXT_FIELD_TYPES']
CONFIG_PLAN = TBL_NAMES['CONFIG_PLAN']
CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']
CONFIG_PROVISION_STATE_AVAILABILITY = TBL_NAMES['CONFIG_PROVISION_STATE_AVAILABILITY']
CONFIG_PROVISION_UI_COMPONENT = TBL_NAMES['CONFIG_PROVISION_UI_COMPONENT']


class Model_RefProvision(BaseModel):
    __tablename__ = REF_PROVISION

    provision_code = db.Column(db.String(30), primary_key=True)
    provision_label = db.Column(db.String(100))

    def __repr__(self):
        return f"<Provision Code: {self.provision_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.provision_code == code).first()


class Model_ConfigProvision(BaseVersionedModel):
    __tablename__ = CONFIG_PROVISION

    provision_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_PLAN}.plan_id"), nullable=False)
    provision_code = db.Column(
        db.String(30), db.ForeignKey(f"{REF_PROVISION}.provision_code"), nullable=False)
    provision_effective_date = db.Column(db.Date(), nullable=False)
    provision_expiration_date = db.Column(db.Date(), nullable=False)

    plan = db.relationship(
        "Model_ConfigPlan", back_populates="provisions")
    provision = db.relationship("Model_RefProvision")
    states = db.relationship(
        "Model_ConfigProvisionStateAvailability", back_populates="provision",
        primaryjoin="""and_(
            Model_ConfigProvision.provision_id == Model_ConfigProvisionStateAvailability.provision_id,
            Model_ConfigProvisionStateAvailability.active_record_indicator == 'Y'
        )""", lazy="joined")

    factors = db.relationship(
        "Model_ConfigFactor", back_populates="provision",
        primaryjoin="""and_(
            Model_ConfigProvision.provision_id == Model_ConfigFactor.provision_id,
            Model_ConfigFactor.active_record_indicator == 'Y'
        )""", lazy="joined")

    def __repr__(self):
        return f"<Provision Id: {self.provision_id}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.provision_id == id).first()


class Model_ConfigProvisionStateAvailability(BaseVersionedModel):
    __tablename__ = CONFIG_PROVISION_STATE_AVAILABILITY

    provision_state_availability_id = db.Column(db.Integer, primary_key=True)
    provision_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_PROVISION}.provision_id"))
    ui_component_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_PROVISION_UI_COMPONENT}.ui_component_id"))
    state_code = db.Column(
        db.String(2), db.ForeignKey(f"{REF_STATE}.state_code"))
    state_effective_date = db.Column(db.Date, nullable=False)
    state_expiration_date = db.Column(db.Date, nullable=False)

    provision = db.relationship(
        "Model_ConfigProvision", back_populates="states")

    def __repr__(self):
        return f"<Provision State Availability Id: {self.provision_state_availability_id} - State: {self.state_code}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.benefit_state_availability_id == id).first()

    @classmethod
    def find_by_state(
        cls,
        state: str,
        effective_date: datetime.date,
        active_record_indicator: str = "Y",
        default_value: str = "XX"
    ):
        base_query = cls.query.filter(between(
            effective_date, cls.provision_effective_date, cls.provision_expiration_date),
            cls.active_record_indicator == active_record_indicator).all()

        query = base_query.filter(cls.state_code == state)
        if query.first() is None:
            query = base_query.filter(cls.state_code == default_value)

        return query.all()


class Model_RefComponentTypes(BaseModel):
    __tablename__ = REF_COMPONENT_TYPES

    component_type = db.Column(db.String(50), primary_key=True)

    def __repr__(self):
        return f"<Component Type: {self.component_type}>"

    @classmethod
    def find(cls, type: str):
        return cls.query.filter(cls.component_type == type).first()


class Model_RefTextFieldTypes(BaseModel):
    __tablename__ = REF_TEXT_FIELD_TYPES

    type_code = db.Column(db.String(30), primary_key=True)

    def __repr__(self):
        return f"<Type Code: {self.type_code}>"

    @classmethod
    def find(cls, type: str):
        return cls.query.filter(cls.type_code == type).first()


class Model_ConfigProvisionUIComponent(BaseVersionedModel):
    __tablename__ = CONFIG_PROVISION_UI_COMPONENT

    ui_component_id = db.Column(db.Integer, primary_key=True)
    component_type = db.Column(
        db.String(2), db.ForeignKey(f"{REF_COMPONENT_TYPES}.component_type"))
    label = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': 'base_component',
        'polymorphic_on': component_type
    }

    def __repr__(self):
        return f"<UI Component ID: {self.ui_component_id} - {self.component_type}>"

    @classmethod
    def find(cls, id: int):
        return cls.query.filter(cls.ui_component_id == id).first()


class Model_ConfigProvisionUIComponent_CheckboxField(Model_ConfigProvisionUIComponent):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__checkbox"
    ui_component_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_PROVISION_UI_COMPONENT}.ui_component_id"), primary_key=True)
    true_value = db.Column(db.String(100))
    false_value = db.Column(db.String(100))
    hint_value = db.Column(db.String(255))
    is_switch = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'checkbox',
    }


class Model_ConfigProvisionUIComponent_TextField(Model_ConfigProvisionUIComponent):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__text_field"
    ui_component_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_PROVISION_UI_COMPONENT}.ui_component_id"), primary_key=True)
    type = db.Column(db.String(30), db.ForeignKey(
        f"{REF_TEXT_FIELD_TYPES}.type_code"), default="input")
    min_value = db.Column(db.Float)
    max_value = db.Column(db.Float)
    step_value = db.Column(db.Float)

    __mapper_args__ = {
        'polymorphic_identity': 'text_field',
    }


class Model_ConfigProvisionUIComponent_SelectField(Model_ConfigProvisionUIComponent):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__select"
    ui_component_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_PROVISION_UI_COMPONENT}.ui_component_id"), primary_key=True)
    item_text = db.Column(db.String(100))
    item_value = db.Column(db.String(100))
    hint_value = db.Column(db.String(100))
    is_radio = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'select',
    }


class Model_ConfigProvisionUIComponent_SelectItemField(BaseVersionedModel):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__select_items"

    ui_component_item_id = db.Column(db.Integer, primary_key=True)
    ui_component_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_PROVISION_UI_COMPONENT}.ui_component_id"))
    item_code = db.Column(db.String(30))
    item_label = db.Column(db.String(100))
