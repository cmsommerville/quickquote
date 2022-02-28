class Model_ConfigUISelectItem {
  constructor(ui_component_item_id, provision_id, item_code, item_label) {
    if (ui_component_item_id) this.ui_component_item_id = ui_component_item_id;
    this.provision_id = provision_id;
    this.item_code = item_code;
    this.item_label = item_label;
  }
}

export class Model_ConfigProvisionUI {
  constructor(data) {
    this.provision_id = +data.provision_id ?? null;
    this.component_type = data.component_type ?? null;
    this.component_type_code = data.component_type_code ?? null;

    if (data.component_type === "INPUT") {
      this.input_type = data.input_type ?? "input";
      this.min_value = +data.min_value ?? null;
      this.max_value = +data.max_value ?? null;
      this.step_value = +data.step_value ?? null;
    }

    if (data.component_type === "CHECKBOX") {
      this.is_switch = data.is_switch ?? false;
    }

    if (data.component_type === "SELECT") {
      this.item_text = data.item_text ?? "item_label";
      this.item_value = data.item_value ?? "item_code";
      this.is_radio = data.is_radio ?? false;
      this.items = data.items.map((item) => {
        return new Model_ConfigUISelectItem(
          item.ui_component_item_id ?? null,
          data.provision_id,
          item.item_code ?? null,
          item.item_label ?? null
        );
      });
    }
  }
  validate() {
    return true;
  }
}

export class Model_ConfigProvisionState {
  constructor(
    provision_state_id,
    provision_id,
    state_id,
    state_effective_date,
    state_expiration_date
  ) {
    if (provision_state_id) {
      this.provision_state_id = provision_state_id;
    }
    this.provision_id = +provision_id ?? null;
    this.state_id = state_id ?? null;
    this.state_effective_date = state_effective_date ?? "1900-01-01";
    this.state_expiration_date = state_expiration_date ?? "9999-12-31";
  }
  validate() {
    return true;
  }
}

export class Model_ConfigProvision {
  constructor(
    provision_id,
    product_id,
    provision_code,
    provision_label,
    provision_effective_date,
    provision_expiration_date
  ) {
    if (provision_id) {
      this.provision_id = provision_id;
    }
    this.product_id = +product_id ?? null;
    this.provision_code = provision_code ?? null;
    this.provision_label = provision_label ?? null;
    this.provision_effective_date = provision_effective_date ?? "1900-01-01";
    this.provision_expiration_date = provision_expiration_date ?? "9999-12-31";
  }
  validate() {
    return true;
  }
}
