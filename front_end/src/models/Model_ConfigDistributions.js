export class Model_ConfigAgeDistribution {
  constructor(age_distribution_id, age, weight) {
    if (age_distribution_id) {
      this.age_distribution_id = age_distribution_id;
    }
    this.age = +age ?? null;
    this.weight = +weight ?? null;
  }
}

export class Model_ConfigAgeDistributionSet {
  constructor(
    age_distribution_set_id,
    age_distribution_set_label,
    age_distribution
  ) {
    if (age_distribution_set_id) {
      this.age_distribution_set_id = age_distribution_set_id;
    }
    this.age_distribution_set_label = age_distribution_set_label ?? null;
    this.age_distribution = age_distribution.map((dist) => {
      return new Model_ConfigAgeDistribution(
        dist.age_distribution_id,
        dist.age,
        dist.weight
      );
    });
  }
  validate() {
    return true;
  }
}

export class Model_ConfigAttrDistribution {
  constructor(attr_distribution_id, attr_value, weight) {
    if (attr_distribution_id) {
      this.attr_distribution_id = attr_distribution_id;
    }
    this.attr_value = attr_value ?? null;
    this.weight = +weight ?? null;
  }
}

export class Model_ConfigAttrDistributionSet {
  constructor(
    attr_distribution_set_id,
    attr_distribution_set_label,
    attr_type_code,
    attr_distribution
  ) {
    if (attr_distribution_set_id) {
      this.attr_distribution_set_id = attr_distribution_set_id;
    }
    this.attr_distribution_set_label = attr_distribution_set_label ?? null;
    this.attr_type_code = attr_type_code ?? null;
    this.attr_distribution = attr_distribution.map((dist) => {
      return new Model_ConfigAttrDistribution(
        dist.attr_distribution_id,
        dist.attr_value,
        dist.weight
      );
    });
  }
  validate() {
    return true;
  }
}
