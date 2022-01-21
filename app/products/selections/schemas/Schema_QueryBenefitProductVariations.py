from app.extensions import ma
from marshmallow import post_dump
from ...config.schemas import Schema_ConfigBenefit

class Schema_QueryBPV_SelectedBenefit(ma.Schema): 
    selection_benefit_id = ma.Integer()
    selection_plan_id = ma.Integer()
    benefit_value = ma.Float()

class Schema_QueryBPV_Coverage(ma.Schema): 
    coverage_id = ma.Integer()
    coverage_code = ma.String()
    coverage_label = ma.String()
    default_value = ma.Boolean()
    section_code = ma.String()

class Schema_QueryBPV_SelectedDurationItem(ma.Schema): 
    selection_benefit_duration_id = ma.Integer()
    config_benefit_duration_item_id = ma.Integer()
    duration_data_type = ma.String()
    duration_value = ma.String()
    
class Schema_QueryBPV_DurationItem(ma.Schema): 
    benefit_duration_item_id = ma.Integer()
    item_code = ma.String()
    item_label = ma.Function(lambda obj: obj.duration_item.item_label)
    benefit_duration_factor = ma.Float()

class Schema_QueryBPV_Duration(ma.Schema): 
    benefit_duration_id = ma.Integer()
    benefit_duration_code = ma.String()
    benefit_duration_label = ma.Function(lambda obj: obj.duration.duration_label)
    default_duration_item_code = ma.String()
    duration_items = ma.List(ma.Nested(Schema_QueryBPV_DurationItem))
    selected_duration_item = ma.List(ma.Nested(Schema_QueryBPV_SelectedDurationItem))

    selected_duration_item_code = ma.Method('get_selected_duration')
    ui_duration_item_code = ma.Method('calc_ui_selection_duration')

    def get_selected_duration(self, obj): 
        try: 
            return obj.selected_duration_item[0].item_code
        except: 
            return None

    def calc_ui_selection_duration(self, obj):
        if self.context['has_plan_benefits']: 
            return self.get_selected_duration(obj) or obj.default_duration_item_code
        return obj.default_duration_item_code
        


class Schema_QueryBPV_Benefit(ma.Schema):
    benefit_id = ma.Integer(data_key="config_benefit_id")
    benefit_code = ma.String()
    benefit_label = ma.Function(lambda obj: obj.ref_benefit.benefit_label)
    benefit_effective_date = ma.String()
    benefit_expiration_date = ma.String()
    coverage = ma.Nested(Schema_QueryBPV_Coverage)
    rate_group_id = ma.Integer(data_key="config_rate_group_id")
    default_value = ma.Float(data_key="default_benefit_value")
    selected_benefit = ma.List(ma.Nested(Schema_QueryBPV_SelectedBenefit))
    selected_benefit_value = ma.Method('get_selected_benefit')
    ui_benefit_value = ma.Method('calc_ui_selection_benefit')
    unit_code = ma.String()
    is_durational = ma.Boolean()
    selections_exist = ma.Boolean()
    # selected_benefit = ma.List(ma.Nested(Schema_QueryBPV_SelectedBenefit))
    durations = ma.List(ma.Nested(Schema_QueryBPV_Duration))

    def get_selected_benefit(self, obj): 
        try: 
            return float(obj.selected_benefit[0].benefit_value)
        except: 
            return None

    def calc_ui_selection_benefit(self, obj):
        if self.context.get('has_plan_benefits', False): 
            return self.get_selected_benefit(obj) or 0
        return float(obj.default_value)
        

class Schema_QueryBPV(ma.Schema):

    benefit = ma.Nested(Schema_QueryBPV_Benefit, required=True)

    @post_dump(pass_many=True)
    def unwrap_envelope(self, data, many, **kwargs):
        if many: 
            return [{**d['benefit']} for d in data]
        return {**data['benefit']}