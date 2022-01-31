export class Model_ConfigProductVariation {
  constructor(
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
    vary_by_gender,
    vary_by_tobacco
  ) {
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
    this.vary_by_gender = vary_by_gender ?? false;
    this.vary_by_tobacco = vary_by_tobacco ?? false;
  }

  validate() {
    return (
      !!this.product_id &&
      !!this.product_variation_code &&
      !!this.product_variation_label &&
      !!this.product_variation_effective_date &&
      !!this.product_variation_expiration_date
    );
  }
}
