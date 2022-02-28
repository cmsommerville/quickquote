class Model_ConfigBenefitDurationItem {
  constructor(
    benefit_duration_item_id,
    benefit_duration_id,
    item_code,
    item_label,
    benefit_duration_factor
  ) {
    if (benefit_duration_item_id) {
      this.benefit_duration_item_id = benefit_duration_item_id;
    }
    if (benefit_duration_id) {
      this.benefit_duration_id = benefit_duration_id;
    }
    this.item_code = item_code;
    this.item_label = item_label;
    this.benefit_duration_factor = benefit_duration_factor;
  }
}

export class Model_ConfigBenefitDuration {
  constructor(
    benefit_duration_id,
    benefit_id,
    benefit_duration_code,
    benefit_duration_label,
    default_duration_item_code,
    items
  ) {
    if (benefit_duration_id) {
      this.benefit_duration_id = benefit_duration_id;
    }
    this.benefit_id = benefit_id;
    this.benefit_duration_code = benefit_duration_code;
    this.benefit_duration_label = benefit_duration_label;
    this.default_duration_item_code = default_duration_item_code;
    this.items = items.map((item) => {
      return new Model_ConfigBenefitDurationItem(
        item.benefit_duration_item_id,
        benefit_duration_id,
        item.item_code,
        item.item_label,
        item.benefit_duration_factor
      );
    });
  }
  validate() {
    return true;
  }
}
