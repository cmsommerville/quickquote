import datetime

REF_STATES = [
    {"state_code": "AL", "state_name": "Alabama"}, 
    {"state_code": "AK", "state_name": "Alaska"}, 
    {"state_code": "AR", "state_name": "Arkansas"}, 
    {"state_code": "AZ", "state_name": "Arizona"}, 
    {"state_code": "CA", "state_name": "California"}, 
    {"state_code": "CO", "state_name": "Colorado"}, 
    {"state_code": "CT", "state_name": "Connecticut"}, 
    {"state_code": "DC", "state_name": "District of Columbia"}, 
    {"state_code": "DE", "state_name": "Delaware"}, 
    {"state_code": "FL", "state_name": "Florida"}, 
    {"state_code": "GA", "state_name": "Georgia"}, 
    {"state_code": "HI", "state_name": "Hawaii"}, 
    {"state_code": "ID", "state_name": "Idaho"}, 
    {"state_code": "IL", "state_name": "Illinois"}, 
    {"state_code": "IN", "state_name": "Indiana"}, 
    {"state_code": "IA", "state_name": "Iowa"}, 
    {"state_code": "KS", "state_name": "Kansas"}, 
    {"state_code": "KY", "state_name": "Kentucky"}, 
    {"state_code": "LA", "state_name": "Louisiana"}, 
    {"state_code": "MD", "state_name": "Maryland"}, 
    {"state_code": "ME", "state_name": "Maine"}, 
    {"state_code": "MA", "state_name": "Massachusetts"}, 
    {"state_code": "MS", "state_name": "Mississippi"}, 
    {"state_code": "MO", "state_name": "Missouri"}, 
    {"state_code": "MI", "state_name": "Michigan"}, 
    {"state_code": "MT", "state_name": "Montana"}, 
    {"state_code": "MN", "state_name": "Minnesota"}, 
    {"state_code": "NM", "state_name": "New Mexico"}, 
    {"state_code": "NC", "state_name": "North Carolina"}, 
    {"state_code": "ND", "state_name": "North Dakota"}, 
    {"state_code": "NY", "state_name": "New York"}, 
    {"state_code": "NJ", "state_name": "New Jersey"}, 
    {"state_code": "NH", "state_name": "New Hampshire"}, 
    {"state_code": "NE", "state_name": "Nebraska"}, 
    {"state_code": "NV", "state_name": "Nevada"}, 
    {"state_code": "OH", "state_name": "Ohio"}, 
    {"state_code": "OK", "state_name": "Oklahoma"}, 
    {"state_code": "OR", "state_name": "Oregon"}, 
    {"state_code": "PA", "state_name": "Pennsylvania"}, 
    {"state_code": "RI", "state_name": "Rhode Island"}, 
    {"state_code": "SC", "state_name": "South Carolina"}, 
    {"state_code": "SD", "state_name": "South Dakota"}, 
    {"state_code": "TX", "state_name": "Texas"}, 
    {"state_code": "TN", "state_name": "Tennessee"}, 
    {"state_code": "UT", "state_name": "Utah"}, 
    {"state_code": "WI", "state_name": "Wisconsin"}, 
    {"state_code": "WV", "state_name": "West Virginia"}, 
    {"state_code": "VT", "state_name": "Vermont"}, 
    {"state_code": "VA", "state_name": "Virginia"}, 
    {"state_code": "WY", "state_name": "Wyoming"}, 
    {"state_code": "WA", "state_name": "Washington"}
]


REF_UNIT_CODES = [
    {
        "unit_code": "dollars",
        "unit_label": "Dollars"
    }, 
    {
        "unit_code": "percent",
        "unit_label": "Percent"
    }
]


REF_RATING_ALGORITHMS = [
    {
        "rating_algorithm_code": "TIER4",
        "rating_algorithm_label": "4 Tier Rates",
        "rating_algorithm_description": "4 Tier Rates"
    }
]

REF_UI_COMPONENT_TYPES = [
    {"component_type_code": "v-text-field", "component_type_label": "Input Field", "component_type_enum": "INPUT"}, 
    {"component_type_code": "v-checkbox", "component_type_label": "Checkbox", "component_type_enum": "CHECKBOX"}, 
    {"component_type_code": "v-switch", "component_type_label": "Switch", "component_type_enum": "SWITCH"}, 
    {"component_type_code": "v-select", "component_type_label": "Select", "component_type_enum": "SELECT"}, 
    {"component_type_code": "v-radio", "component_type_label": "Radio", "component_type_enum": "RADIO"}, 
]


REF_INPUT_TYPES = [
    {"type_code": "input"}, 
    {"type_code": "number"}, 
    {"type_code": "date"}, 
]


CONFIG_PRODUCT = {
    "product_code": "AC", 
    "product_label": "Accident", 
    "product_effective_date": '1900-01-01',
    "product_expiration_date": '9999-12-31'
}


CONFIG_PRODUCT_VARIATION = {
    "product_variation_code": "base", 
    "product_variation_label": "Base", 
    "product_variation_effective_date": '1900-01-01', 
    "product_variation_expiration_date": '9999-12-31', 
    "is_gender_rated": False, 
    "is_age_rated": True, 
    "is_tobacco_rated": True, 
    "is_family_code_rated": True, 
    "family_code_rating_algorithm_code": "TIER4", 
    "min_issue_age": 18, 
    "max_issue_age": 99
}


CONFIG_COVERAGE = {
    "coverage_code": "base", 
    "coverage_label": "Base", 
    "section_code": "main"
}


CONFIG_RATE_GROUP = {
    "rate_group_code": "LS", 
    "rate_type_code": "APU",
    "rate_type": {
        "rate_type_code": "APU", 
        "rate_type_label": "Annual Rate per $1000"
    }, 
    "rate_group": {
        "rate_group_code": "LS", 
        "rate_group_label": "Lump Sum"
    }
}

