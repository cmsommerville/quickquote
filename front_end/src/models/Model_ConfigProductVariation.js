export class Model_ConfigProductVariation {
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
    family_code_rating_algorithm_code,
    min_issue_age,
    max_issue_age,
    unismoker_distribution_set_id,
    unisex_distribution_set_id,
    age_distribution_set_id,
    smoker_distinct_distribution_set_id,
    sex_distinct_distribution_set_id,
    vary_by_gender,
    vary_by_tobacco
  ) {
    if (product_variation_id) {
      this.product_variation_id = product_variation_id;
    }
    this.product_id = product_id;
    this.product_variation_code = product_variation_code;
    this.product_variation_label = product_variation_label;
    this.product_variation_effective_date =
      product_variation_effective_date ?? "1900-01-01";
    this.product_variation_expiration_date =
      product_variation_expiration_date ?? "9999-12-31";
    this.is_gender_rated = is_gender_rated ?? false;
    this.is_age_rated = is_age_rated ?? false;
    this.is_tobacco_rated = is_tobacco_rated ?? false;
    this.is_family_code_rated = is_family_code_rated ?? false;
    this.family_code_rating_algorithm_code = is_family_code_rated
      ? family_code_rating_algorithm_code
      : null;

    this.min_issue_age = min_issue_age ?? null;
    this.max_issue_age = max_issue_age ?? null;
    this.unismoker_distribution_set_id = unismoker_distribution_set_id ?? null;
    this.unisex_distribution_set_id = unisex_distribution_set_id ?? null;
    this.age_distribution_set_id = age_distribution_set_id ?? null;
    this.smoker_distinct_distribution_set_id =
      smoker_distinct_distribution_set_id ?? null;
    this.sex_distinct_distribution_set_id =
      sex_distinct_distribution_set_id ?? null;
    this.vary_by_gender = vary_by_gender ?? false;
    this.vary_by_tobacco = vary_by_tobacco ?? false;
  }

  validate() {
    return (
      !!this.product_id &&
      !!this.product_variation_code &&
      !!this.product_variation_label &&
      !!this.product_variation_effective_date &&
      !!this.min_issue_age &&
      !!this.max_issue_age &&
      !!this.unismoker_distribution_set_id &&
      !!this.unisex_distribution_set_id &&
      !!this.age_distribution_set_id
    );
  }
}
