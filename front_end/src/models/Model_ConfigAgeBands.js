export class Model_ConfigAgeBands {
  constructor(
    age_band_set_id,
    product_variation_id,
    state_id,
    age_band_effective_date,
    age_band_expiration_date,
    age_bands
  ) {
    if (age_band_set_id) {
      this.age_band_set_id = age_band_set_id;
    }
    this.product_variation_id = product_variation_id ?? null;
    this.state_id = state_id ?? null;
    this.age_band_effective_date = age_band_effective_date ?? "1900-01-01";
    this.age_band_expiration_date = age_band_expiration_date ?? "9999-12-31";
    this.age_bands = age_bands ?? [{ age_band_lower: 18, age_band_upper: 99 }];
  }

  validate() {
    return (
      !!this.product_variation_id &&
      !!this.state_id &&
      !!this.age_band_effective_date &&
      !!this.age_band_expiration_date
    );
  }
}
