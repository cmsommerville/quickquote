export const BENEFIT_UNITS = [
  {
    value: "dollar",
    text: "$",
  },
  {
    value: "percent",
    text: "%",
  },
];

export const OPERATORS = {
  eq: "=",
  lt: "<",
  le: "<=",
  gt: ">",
  ge: ">=",
  ne: "!=",
};

export const FACTOR_RULE_FIELDS = [
  {
    class_code: "plan",
    class_label: "Plan",
    attributes: [
      { label: "Product Variation Code", code: "product_variation_code" },
      { label: "Rating State", code: "state_code" },
      { label: "Plan Effective Date", code: "plan_effective_date" },
      { label: "Broker ID", code: "broker_id" },
    ],
  },
  {
    class_code: "rate_table",
    class_label: "Rate Table",
    attributes: [
      { label: "Family Tier Code", code: "family_code" },
      { label: "Tobacco Status Code", code: "tobacco_status" },
      { label: "Age", code: "age" },
      { label: "Gender Code", code: "gender" },
    ],
  },
  {
    class_code: "provision",
    class_label: "Provision",
    attributes: [{ label: "Provision Value", code: "provision_value" }],
  },
];
