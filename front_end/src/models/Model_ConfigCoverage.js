export class Model_ConfigCoverage {
  constructor(product_id, coverage_code, coverage_label, section_code) {
    this.product_id = +product_id ?? null;
    this.coverage_code = coverage_code ?? null;
    this.coverage_label = coverage_label ?? null;
    this.section_code = section_code ?? null;
    this.default_value = true;
  }

  set_coverage_id(id) {
    this.coverage_id = +id;
  }

  validate() {
    return (
      !!this.product_id &&
      !!this.coverage_code &&
      !!this.coverage_label &&
      !!this.section_code
    );
  }
}
