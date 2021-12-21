import datetime
from sqlalchemy import between
from sqlalchemy.orm import aliased, contains_eager
from app.extensions import db
from app.shared import BaseModel

from .Config_States import Model_RefStates

from .constants import TBL_NAMES

REF_COMPONENT_TYPES = TBL_NAMES["REF_COMPONENT_TYPES"]
REF_PROVISION = TBL_NAMES['REF_PROVISION']
REF_STATE = TBL_NAMES['REF_STATE']
REF_TEXT_FIELD_TYPES = TBL_NAMES['REF_TEXT_FIELD_TYPES']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
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


class Model_ConfigProvision(BaseModel):
    __tablename__ = CONFIG_PROVISION
    __table_args__ = (
        db.UniqueConstraint('product_id', 'provision_code'),
        db.CheckConstraint('provision_effective_date <= provision_expiration_date')
    )

    provision_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.product_id"), nullable=False)
    provision_code = db.Column(db.ForeignKey(f"{REF_PROVISION}.provision_code"), nullable=False)
    provision_effective_date = db.Column(db.Date(), nullable=False)
    provision_expiration_date = db.Column(db.Date(), nullable=False)

    product = db.relationship(
        "Model_ConfigProduct", back_populates="provisions")
    provision = db.relationship("Model_RefProvision")
    states = db.relationship(
        "Model_ConfigProvisionStateAvailability", back_populates="provision")
    factors = db.relationship("Model_ConfigFactor")

    def __repr__(self):
        return f"<Provision Id: {self.provision_id}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.provision_id == id).first()

    @classmethod
    def find_by_product(cls, id):
        return cls.query.filter(cls.product_id == id).all()

    @classmethod
    def find_by_state(
        cls, 
        state: str, 
        effective_date: datetime.date, 
        product_id: int
        ): 

        PSA = aliased(Model_ConfigProvisionStateAvailability, name='PSA')
        RefStateProv = aliased(Model_RefStates)

        # filter effective dates on product
        qry = db.session.query(cls)\
            .filter(between(
                effective_date, 
                cls.provision_effective_date, 
                cls.provision_expiration_date))

        # filter for product ID
        qry = qry.filter(cls.product_id == product_id)
    
        # filter coverage and benefit state availability
        qry = qry.join(cls.states)\
            .join(RefStateProv, PSA.state)\
            .filter(
                RefStateProv.state_code == state, 
                between(
                    effective_date, 
                    PSA.state_effective_date, 
                    PSA.state_expiration_date)
                )\
            .options(contains_eager(cls.states)).populate_existing()

        return qry.all()



class Model_ConfigProvisionStateAvailability(BaseModel):
    __tablename__ = CONFIG_PROVISION_STATE_AVAILABILITY
    __table_args__ = (
        db.UniqueConstraint('provision_id', 'state_id'),
        db.CheckConstraint('state_effective_date <= state_expiration_date')
    )

    provision_state_availability_id = db.Column(db.Integer, primary_key=True)
    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION}.provision_id"), nullable=False)
    state_id = db.Column(db.ForeignKey(f"{REF_STATE}.state_id"), nullable=False)
    state_effective_date = db.Column(db.Date, nullable=False)
    state_expiration_date = db.Column(db.Date, nullable=False)

    provision = db.relationship(
        "Model_ConfigProvision", back_populates="states")

    def __repr__(self):
        return f"<Provision State Availability Id: {self.provision_state_availability_id} - State: {self.state_code}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.provision_state_availability_id == id).first()

    @classmethod
    def find_by_provision(cls, id):
        return cls.query.filter(cls.provision_id == id).all()




class Model_RefComponentTypes(BaseModel):
    __tablename__ = REF_COMPONENT_TYPES

    component_type_code = db.Column(db.String(50), primary_key=True)
    component_type_label = db.Column(db.String(100), nullable=False)
    component_type_enum = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Component Type: {self.component_type_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.component_type_code == code).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

class Model_RefTextFieldTypes(BaseModel):
    __tablename__ = REF_TEXT_FIELD_TYPES

    type_code = db.Column(db.String(30), primary_key=True)

    def __repr__(self):
        return f"<Type Code: {self.type_code}>"

    @classmethod
    def find(cls, type: str):
        return cls.query.filter(cls.type_code == type).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


class Model_ConfigProvisionUIComponent(BaseModel):
    __tablename__ = CONFIG_PROVISION_UI_COMPONENT
    __table_args__ = (
        db.UniqueConstraint('provision_id'),
    )

    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION}.provision_id"), primary_key=True)
    component_type  = db.Column(db.String(50), nullable=False)
    component_type_code = db.Column(
        db.String(50), db.ForeignKey(f"{REF_COMPONENT_TYPES}.component_type_code"), nullable=False)
    ui_label = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'BASE',
        'polymorphic_on': component_type
    }

    def __repr__(self):
        return f"<Provision UI ID: {self.provision_id} - {self.component_type_code}>"

    @classmethod
    def find(cls, id: int):
        res = cls.query.filter(cls.provision_id == id).first()
        if res is None:
            return
        if res.component_type == "INPUT":
            return Model_ConfigProvisionUIComponent_TextField.find(id)
        if res.component_type == "CHECKBOX": 
            return Model_ConfigProvisionUIComponent_CheckboxField.find(id)
        if res.component_type == "SELECT": 
            return Model_ConfigProvisionUIComponent_SelectField.find(id)


class Model_ConfigProvisionUIComponent_CheckboxField(Model_ConfigProvisionUIComponent):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__checkbox"
    
    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION_UI_COMPONENT}.provision_id"), primary_key=True)
    true_value = db.Column(db.String(100))
    false_value = db.Column(db.String(100))
    hint_value = db.Column(db.String(255))
    is_switch = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'CHECKBOX',
    }

    @classmethod
    def find(cls, id: int):
        return cls.query.filter(cls.provision_id == id).first()

class Model_ConfigProvisionUIComponent_TextField(Model_ConfigProvisionUIComponent):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__text_field"

    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION_UI_COMPONENT}.provision_id"), primary_key=True)
    input_type = db.Column(db.String(30), db.ForeignKey(
        f"{REF_TEXT_FIELD_TYPES}.type_code"), default="input")
    min_value = db.Column(db.Float)
    max_value = db.Column(db.Float)
    step_value = db.Column(db.Float)

    __mapper_args__ = {
        'polymorphic_identity': 'INPUT',
    }

    @classmethod
    def find(cls, id: int):
        return cls.query.filter(cls.provision_id == id).first()


class Model_ConfigProvisionUIComponent_SelectField(Model_ConfigProvisionUIComponent):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__select"
    
    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION_UI_COMPONENT}.provision_id"), primary_key=True)
    item_text = db.Column(db.String(100))
    item_value = db.Column(db.String(100))
    hint_value = db.Column(db.String(100))
    is_radio = db.Column(db.Boolean, default=False)

    items = db.relationship(
        "Model_ConfigProvisionUIComponent_SelectItemField")

    __mapper_args__ = {
        'polymorphic_identity': 'SELECT',
    }

    @classmethod
    def find(cls, id: int):
        return cls.query.filter(cls.provision_id == id).first()


class Model_ConfigProvisionUIComponent_SelectItemField(BaseModel):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__select_items"

    ui_component_item_id = db.Column(db.Integer, primary_key=True)
    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION_UI_COMPONENT}.provision_id"))
    item_code = db.Column(db.String(30))
    item_label = db.Column(db.String(100))
