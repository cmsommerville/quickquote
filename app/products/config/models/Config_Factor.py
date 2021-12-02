import datetime
from sqlalchemy import between
from app.extensions import db
from app.shared import BaseModel, BaseModel

from .constants import TBL_NAMES, FACTOR_DECIMAL_PRECISION

REF_COMPARISON_OPERATOR = TBL_NAMES['REF_COMPARISON_OPERATOR']
REF_INTERPOLATION_RULE = TBL_NAMES['REF_INTERPOLATION_RULE']
REF_PROVISION = TBL_NAMES['REF_PROVISION']
REF_STATE = TBL_NAMES['REF_STATE']
CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_BENEFIT_FACTOR_APPLICABILITY = TBL_NAMES['CONFIG_BENEFIT_FACTOR_APPLICABILITY']
CONFIG_FACTOR = TBL_NAMES['CONFIG_FACTOR']
CONFIG_FACTOR_RULE = TBL_NAMES['CONFIG_FACTOR_RULE']
CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']


class Model_RefInterpolationRule(BaseModel):
    __tablename__ = REF_INTERPOLATION_RULE

    interpolation_rule_code = db.Column(db.String(30), primary_key=True)

    def __repr__(self):
        return f"<Interpolation Rule Code: {self.interpolation_rule_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.interpolation_rule_code == code).first()


class Model_ConfigFactor(BaseModel):
    __tablename__ = CONFIG_FACTOR

    factor_id = db.Column(db.Integer, primary_key=True)
    provision_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_PROVISION}.provision_id"), nullable=False)
    factor_value = db.Column(db.Numeric(
        FACTOR_DECIMAL_PRECISION), nullable=False)
    factor_priority = db.Column(db.Integer, nullable=False)
    factor_interpolation_low_value = db.Column(
        db.Numeric(FACTOR_DECIMAL_PRECISION))
    factor_interpolation_high_value = db.Column(
        db.Numeric(FACTOR_DECIMAL_PRECISION))
    factor_interpolation_rule_code = db.Column(db.String(30), db.ForeignKey(
        f"{REF_INTERPOLATION_RULE}.interpolation_rule_code"))

    provision = db.relationship(
        "Model_ConfigProvision", back_populates="factors")

    def __repr__(self):
        return f"<Factor Id: {self.factor_id} - {self.factor_priority}: {self.factor_value}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.factor_id == id).first()


class Model_RefComparisonOperator(BaseModel):
    __tablename__ = REF_COMPARISON_OPERATOR

    comparison_operator_code = db.Column(db.String(10), primary_key=True)
    comparison_operator_label = db.Column(db.String(100))
    comparison_operator_symbol = db.Column(db.String(100))

    def __repr__(self):
        return f"< Comparison Operator Code: {self.comparison_operator_code} >"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.comparison_operator_code == code).first()


class Model_ConfigFactorRule(BaseModel):
    __tablename__ = CONFIG_FACTOR_RULE

    factor_rule_id = db.Column(db.Integer, primary_key=True)
    factor_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_FACTOR}.factor_id"))
    class_name = db.Column(db.String(100), nullable=False)
    field_name = db.Column(db.String(100), nullable=False)
    comparison_operator_code = db.Column(db.String(10), db.ForeignKey(
        f"{REF_COMPARISON_OPERATOR}.comparison_operator_code"), nullable=False)
    field_value = db.Column(db.String(100), nullable=False)
    field_value_data_type = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Factor Rule ID: {self.factor_rule_id}>"

    @classmethod
    def find(cls, id: int):
        return cls.query.filter(cls.factor_rule_id == id).first()


class Model_ConfigBenefitFactorApplicability(BaseModel):
    __tablename__ = CONFIG_BENEFIT_FACTOR_APPLICABILITY

    benefit_id = db.Column(db.ForeignKey(
        f'{CONFIG_BENEFIT}.benefit_id'), primary_key=True)
    factor_id = db.Column(db.ForeignKey(
        f'{CONFIG_FACTOR}.factor_id'), primary_key=True)
