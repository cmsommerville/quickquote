from app.extensions import ma
from ..models import Model_ConfigBenefit, Model_ConfigBenefitDuration, \
    Model_ConfigBenefitStateAvailability, Model_ConfigBenefitDurationItems, \
    Model_RefBenefit, Model_RefBenefitDuration, Model_RefBenefitDurationItems, \
    Model_RefUnitCode

class Schema_ConfigBenefit(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigBenefit
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_ConfigBenefitStateAvailability(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigBenefitStateAvailability
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_ConfigBenefitDuration(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigBenefitDuration
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_ConfigBenefitDurationItems(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigBenefitDurationItems
        load_instance = True
        include_relationships = True
        include_fk = True


class Schema_RefBenefit(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefBenefit
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_RefBenefitDuration(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefBenefitDuration
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_RefBenefitDurationItems(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefBenefitDurationItems
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_RefUnitCode(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefUnitCode
        load_instance = True
        include_relationships = True
        include_fk = True
