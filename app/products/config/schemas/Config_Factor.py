import decimal
from app.extensions import ma
from marshmallow import validate, post_dump
from ..models import Model_ConfigFactor, Model_RefInterpolationRule, Model_RefComparisonOperator, \
    Model_ConfigFactorRule

class Schema_RefInterpolationRule(ma.SQLAlchemyAutoSchema): 
    class Meta:
        model = Model_RefInterpolationRule
        load_instance = True
    
class Schema_RefComparisonOperator(ma.SQLAlchemyAutoSchema): 
    class Meta:
        model = Model_RefComparisonOperator
        load_instance = True

    
class Schema_ConfigFactorRule(ma.SQLAlchemyAutoSchema): 
    class Meta:
        model = Model_ConfigFactorRule
        load_instance = True
        include_relationships = True
        include_fk = True
    
    
class Schema_ConfigFactor(ma.SQLAlchemyAutoSchema): 
    class Meta:
        model = Model_ConfigFactor
        load_instance = True
        include_relationships = True
        include_fk = True
    
    factor_rules = ma.List(ma.Nested(Schema_ConfigFactorRule))

    @post_dump(pass_many=True)
    def formatDecimal(self, data, many, **kwargs):
        if many:
            return [{k: v if type(v) != decimal.Decimal else float(v) for k, v in item.items()}
                    for item in data]
        else:
            new_data = {k: v if type(v) != decimal.Decimal else float(v)
                        for k, v in data.items()}
            return new_data
