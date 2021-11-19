export const STATES = [
  { code: "AL", label: "Alabama" },
  { code: "AK", label: "Alaska" },
  { code: "AR", label: "Arkansas" },
  { code: "AZ", label: "Arizona" },
  { code: "NC", label: "North Carolina" },
  { code: "SC", label: "South Carolina" },
];

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
  range: "between",
  nrange: "not between",
};

export const COMPONENT_TYPES = [
  { code: "v-text-field", label: "Input" },
  { code: "v-select", label: "Select" },
  { code: "v-checkbox", label: "Checkbox" },
  { code: "v-radio", label: "Radio" },
  { code: "v-switch", label: "Switch" },
];

export const INPUT_TYPES = [
  { code: "text", label: "Text" },
  { code: "number", label: "Number" },
  { code: "date", label: "Date" },
  { code: "email", label: "Email" },
  { code: "password", label: "Password" },
];
