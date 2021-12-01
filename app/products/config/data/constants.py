# UI constants
UI_COMPONENTS = [
    "v-text-field", "v-select", "v-switch", "v-checkbox", "v-radio"
]

UI_SECTIONS = ["main"]

UI_TEXT_FIELD_TYPES = ["input", "number", "date", "email", "password", "tel"]

# generic constants
STATE_CODES = [
    "AK", "AL", "AZ", "AR", "CA", "NC", "SC"
]

APPLICABILITY_VALUES = [
    "prohibited", "mandatory", "permitted"
]

QUOTING_ACCESS_LEVELS = [
    {"level": 100, "code": "hidden"},
    {"level": 200, "code": "disabled"},
    {"level": 300, "code": "underwritten"},
    {"level": 400, "code": "permitted"}
]

OPERATOR_CODES = [
    "eq", "ne", "le", "lt", "ge", "gt", "range", "nrange"
]

# rounding rules
FACTOR_PRECISION = 5
