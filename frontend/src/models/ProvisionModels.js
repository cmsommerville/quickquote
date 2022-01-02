class ProvisionUIComponent {
  constructor(provision_id, component_type, component_type_code, ui_label) {
    this.provision_id = provision_id;
    this.component_type = component_type;
    this.component_type_code = component_type_code;
    this.ui_label = ui_label;
  }

  validate() {
    try {
      for (const key in this) {
        if (this[key] == null) {
          return false;
        }
      }
      return true;
    } catch (err) {
      return false;
    }
  }
}

class ProvisionUIComponent_TextField extends ProvisionUIComponent {
  constructor(
    provision_id,
    component_type,
    component_type_code,
    ui_label,
    input_type,
    min_value,
    max_value,
    step_value
  ) {
    super(provision_id, component_type, component_type_code, ui_label);
    this.input_type = input_type;
    this.min_value = min_value ?? null;
    this.max_value = max_value ?? null;
    this.step_value = step_value ?? null;
  }
  validate() {
    return (
      this.provision_id != null &&
      this.component_type != null &&
      this.component_type_code != null &&
      this.ui_label != null &&
      this.input_type != null
    );
  }
}

class ProvisionUIComponent_SelectField extends ProvisionUIComponent {
  constructor(
    provision_id,
    component_type,
    component_type_code,
    ui_label,
    item_text,
    item_value,
    is_radio,
    items
  ) {
    super(provision_id, component_type, component_type_code, ui_label);
    this.item_text = item_text;
    this.item_value = item_value;
    this.is_radio = is_radio;
    this.items = items;
  }
}

class ProvisionUIComponent_CheckboxField extends ProvisionUIComponent {
  constructor(
    provision_id,
    component_type,
    component_type_code,
    ui_label,
    is_switch
  ) {
    super(provision_id, component_type, component_type_code, ui_label);
    this.is_switch = is_switch;
  }
}

export function ProvisionUIModel(data) {
  if (data.component_type === "INPUT") {
    const {
      provision_id,
      component_type,
      component_type_code,
      ui_label,
      input_type,
      min_value,
      max_value,
      step_value,
    } = data;
    return new ProvisionUIComponent_TextField(
      provision_id,
      component_type,
      component_type_code,
      ui_label,
      input_type,
      min_value,
      max_value,
      step_value
    );
  }
  if (data.component_type === "CHECKBOX") {
    const { provision_id, component_type, component_type_code, ui_label } =
      data;

    return new ProvisionUIComponent_CheckboxField(
      provision_id,
      component_type,
      component_type_code,
      ui_label,
      false
    );
  }
  if (data.component_type === "SWITCH") {
    const { provision_id, component_type, component_type_code, ui_label } =
      data;

    return new ProvisionUIComponent_CheckboxField(
      provision_id,
      component_type,
      component_type_code,
      ui_label,
      true
    );
  }
  if (data.component_type === "SELECT") {
    const {
      provision_id,
      component_type,
      component_type_code,
      ui_label,
      item_text,
      item_value,
      items,
    } = data;
    return new ProvisionUIComponent_SelectField(
      provision_id,
      component_type,
      component_type_code,
      ui_label,
      item_text,
      item_value,
      false,
      items
    );
  }
  if (data.component_type === "RADIO") {
    const {
      provision_id,
      component_type,
      component_type_code,
      ui_label,
      item_text,
      item_value,
      items,
    } = data;
    return new ProvisionUIComponent_SelectField(
      provision_id,
      component_type,
      component_type_code,
      ui_label,
      item_text,
      item_value,
      true,
      items
    );
  }
}
