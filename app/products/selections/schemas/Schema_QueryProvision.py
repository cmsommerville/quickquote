from app.extensions import ma



class Schema_QueryProvision_UIComponent_SelectionItems(ma.Schema): 
    ui_component_item_id = ma.Integer()
    item_code = ma.String() 
    item_label = ma.String()


class Schema_QueryProvision_UIComponent(ma.Schema): 
    component_type = ma.String()
    component_type_code = ma.String()
    ui_label = ma.String(data_key="label")
    input_type = ma.String(data_key="type")
    min_value = ma.Integer(data_key="min")
    max_value = ma.Integer(data_key="max")
    step_value = ma.Integer(data_key="step")
    item_text = ma.String(data_key="item-text")
    item_value = ma.String(data_key="item-value")
    items = ma.List(ma.Nested(Schema_QueryProvision_UIComponent_SelectionItems))
    is_radio = ma.Boolean()
    true_value = ma.String(data_key="true-value")
    false_value = ma.String(data_key="false-value")
    is_switch = ma.Boolean()


class Schema_QueryProvision_Selection(ma.Schema): 
    selection_provision_id = ma.Integer()
    selection_plan_id = ma.Integer()
    provision_value = ma.String()
    provision_data_type = ma.String()


class Schema_QueryProvision_States(ma.Schema): 
    state_id = ma.Integer()
    state_effective_date = ma.Date()
    state_expiration_date = ma.Date()

class Schema_QueryProvision(ma.Schema):
    provision_id = ma.Integer(data_key="config_provision_id")
    provision_code = ma.String()
    provision_effective_date = ma.Date()
    provision_expiration_date = ma.Date()

    states = ma.List(ma.Nested(Schema_QueryProvision_States))
    ui_component = ma.Nested(Schema_QueryProvision_UIComponent)
    selection_provision_id = ma.Method('get_selected_provision_id')
    selected_provision_value = ma.Method('get_selected_provision')
    selected_provision_data_type = ma.Method('get_selected_provision_data_type')

    ui_provision_value = ma.Method('get_selected_provision')
    ui_provision_data_type = ma.Method('get_selected_provision_data_type')

    def get_selected_provision_id(self, obj): 
        try: 
            return obj.selected_provision[0].selection_provision_id
        except: 
            return None

    def get_selected_provision(self, obj): 
        try: 
            return obj.selected_provision[0].provision_value
        except: 
            return None

    def get_selected_provision_data_type(self, obj): 
        try: 
            return obj.selected_provision[0].provision_data_type
        except: 
            return None