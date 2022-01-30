export default class Model_SelectionBenefit {
  constructor(
    product_variation_id,
    product_id,
    product_variation_code,
    product_variation_label,
    product_variation_effective_date,
    product_variation_expiration_date,
    is_gender_rated,
    is_age_rated,
    is_tobacco_rated,
    is_family_code_rated,
    vary_by_gender,
    vary_by_tobacco
  ) {
    this.product_variation_id = product_variation_id;
    this.product_id = product_id;
    this.product_variation_code = product_variation_code;
    this.product_variation_label = product_variation_label;
    this.product_variation_effective_date = product_variation_effective_date;
    this.product_variation_expiration_date = product_variation_expiration_date;
    this.is_gender_rated = is_gender_rated;
    this.is_age_rated = is_age_rated;
    this.is_tobacco_rated = is_tobacco_rated;
    this.is_family_code_rated = is_family_code_rated;
    this.vary_by_gender = vary_by_gender;
    this.vary_by_tobacco = vary_by_tobacco;
  }

  set_base_attributes(
    product_id,
    product_variation_code,
    product_variation_label,
    product_variation_effective_date,
    product_variation_expiration_date
  ) {
    this.product_id = product_id;
    this.product_variation_code = product_variation_code;
    this.product_variation_label = product_variation_label;
    this.product_variation_effective_date = product_variation_effective_date;
    this.product_variation_expiration_date = product_variation_expiration_date;
  }
  set_config_attributes(
    is_gender_rated,
    is_age_rated,
    is_tobacco_rated,
    is_family_code_rated,
    vary_by_gender,
    vary_by_tobacco
  ) {
    this.is_gender_rated = is_gender_rated;
    this.is_age_rated = is_age_rated;
    this.is_tobacco_rated = is_tobacco_rated;
    this.is_family_code_rated = is_family_code_rated;
    this.vary_by_gender = vary_by_gender;
    this.vary_by_tobacco = vary_by_tobacco;
  }
}
