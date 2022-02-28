export class Model_ConfigBenefitState {
  constructor(
    parent_id,
    product_id,
    state_id,
    benefit_code,
    benefit_effective_date,
    benefit_expiration_date
  ) {
    this.parent_id = +parent_id ?? null;
    this.product_id = +product_id ?? null;
    this.state_id = state_id ?? null;
    this.benefit_code = benefit_code ?? null;
    this.benefit_effective_date = benefit_effective_date ?? "1900-01-01";
    this.benefit_expiration_date = benefit_expiration_date ?? "9999-12-31";
  }
  validate() {
    return true;
  }
}

export class Model_ConfigBenefit {
  constructor(
    benefit_id,
    product_id,
    state_id,
    benefit_code,
    benefit_label,
    benefit_effective_date,
    benefit_expiration_date,
    coverage_id,
    rate_group_id,
    min_value,
    max_value,
    step_value,
    default_value,
    unit_code,
    is_durational
  ) {
    if (benefit_id) {
      this.benefit_id = benefit_id;
    }
    this.product_id = +product_id ?? null;
    this.state_id = state_id ?? null;
    this.benefit_code = benefit_code ?? null;
    this.benefit_label = benefit_label ?? null;
    this.benefit_effective_date = benefit_effective_date ?? "1900-01-01";
    this.benefit_expiration_date = benefit_expiration_date ?? "9999-12-31";
    this.coverage_id = coverage_id ?? null;
    this.rate_group_id = rate_group_id ?? null;
    this.min_value = min_value ?? null;
    this.max_value = max_value ?? null;
    this.step_value = step_value ?? null;
    this.default_value = default_value ?? null;
    this.unit_code = unit_code ?? null;
    this.is_durational = is_durational ?? false;
  }
  validate() {
    return true;
  }
}
