from app.extensions import ma



class Schema_QueryFactors_FactorRule(ma.Schema): 
    factor_rule_id = ma.Integer()
    class_name = ma.String()
    field_name = ma.String()
    comparison_operator_code = ma.String()
    field_value = ma.String()
    field_value_data_type = ma.String()
    

class Schema_QueryFactors_Factor(ma.Schema): 
    factor_id = ma.Integer()
    factor_priority = ma.Integer()
    factor_value = ma.Float()
    factor_interpolation_low_value = ma.Float()
    factor_interpolation_high_value = ma.Float()
    factor_interpolation_rule_code = ma.String()

    factor_rules = ma.List(ma.Nested(Schema_QueryFactors_FactorRule))


class Schema_QueryFactors_ConfigProvision(ma.Schema): 
    config_provision_id = ma.Integer()
    provision_code = ma.String()
    factors = ma.List(ma.Nested(Schema_QueryFactors_Factor))

class Schema_QueryFactors_SelectionProvision(ma.Schema):
    selection_provision_id = ma.Integer()
    selection_plan_id = ma.Integer()
    config_provision_id = ma.Integer()
    provision_code = ma.Function(lambda obj: obj.config_provision.provision_code or None)
    provision_value = ma.String()
    provision_data_type = ma.String()

    config_provision = ma.Nested(Schema_QueryFactors_ConfigProvision)

    # def get_selected_provision(self, obj): 
    #     try: 
    #         return obj.selected_provision[0].provision_value
    #     except: 
    #         return None

    # def get_selected_provision_data_type(self, obj): 
    #     try: 
    #         return obj.selected_provision[0].provision_data_type
    #     except: 
    #         return None