export class Model_ConfigFactorUI {
  constructor(data) {
    this.provision_id = +data.provision_id ?? null;
    this.field_name = data.ui_label;
    this.field_code = "provision_value";
    this.component_type = data.component_type ?? null;
    this.component_type_code = data.component_type_code ?? null;

    if (data.component_type === "INPUT") {
      this.input_type = data.input_type ?? "input";
      this.min_value = +data.min_value ?? null;
      this.max_value = +data.max_value ?? null;
      this.step_value = +data.step_value ?? null;
      if (data.min_value && !isNaN(data.min_value)) {
        this.field_value_data_type = "number";
      } else {
        this.field_value_data_type = "string";
      }
    }

    if (data.component_type === "CHECKBOX") {
      this.is_switch = data.is_switch ?? false;
      this.field_value_data_type = typeof true;
    }

    if (data.component_type === "SELECT") {
      this.item_text = data.item_text ?? "item_label";
      this.item_value = data.item_value ?? "item_code";
      this.is_radio = data.is_radio ?? false;
      this.field_value_list = () => {
        return data.items.map((item) => {
          return {
            code: item.item_code ?? null,
            label: item.item_label ?? null,
          };
        });
      };
      this.field_value_data_type = "string";
    }
  }
  validate() {
    return true;
  }
}

class Model_ConfigFactorRule {
  constructor(
    factor_rule_id,
    factor_id,
    class_name,
    field_name,
    comparison_operator_code,
    field_value,
    field_value_data_type
  ) {
    if (factor_rule_id) {
      this.factor_rule_id = factor_rule_id;
    }
    if (factor_id) {
      this.factor_id = factor_id;
    }
    this.class_name = class_name ?? null;
    this.field_name = field_name ?? null;
    this.comparison_operator_code = comparison_operator_code ?? null;
    this.field_value = field_value ?? null;
    this.field_value_data_type = field_value_data_type ?? null;
  }
}
export class Model_ConfigFactor {
  constructor(
    factor_id,
    provision_id,
    factor_priority,
    factor_value,
    factor_rules
  ) {
    if (factor_id) {
      this.factor_id = +factor_id;
    }
    this.provision_id = +provision_id ?? null;
    this.factor_priority = factor_priority ?? null;
    this.factor_value = factor_value ?? null;
    this.factor_rules =
      factor_rules && factor_rules.length
        ? factor_rules.map((rule) => {
            return new Model_ConfigFactorRule(
              rule.factor_rule_id,
              factor_id,
              rule.class_name,
              rule.field_name,
              rule.comparison_operator_code,
              rule.field_value,
              rule.field_value_data_type
            );
          })
        : null;
  }
  validate() {
    return true;
  }
}
