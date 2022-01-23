export default class Model_SelectionBenefit {
  constructor(
    selection_plan_id,
    config_benefit_id,
    config_rate_group_id,
    benefit_value
  ) {
    this.selection_plan_id = selection_plan_id;
    this.config_benefit_id = config_benefit_id;
    this.config_rate_group_id = config_rate_group_id;
    this.benefit_value = benefit_value;
  }

  set_selection_benefit_id(id) {
    this.selection_benefit_id = id;
  }
}
