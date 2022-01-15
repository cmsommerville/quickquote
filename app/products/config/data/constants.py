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


REF_COMPARISON_OPERATORS = [
    {"comparison_operator_code": "__gt__", "comparison_operator_label": "Greater Than", "comparison_operator_symbol": ">"}, 
    {"comparison_operator_code": "__lt__", "comparison_operator_label": "Less Than", "comparison_operator_symbol": "<"}, 
    {"comparison_operator_code": "__ge__", "comparison_operator_label": "Greater Than or Equal", "comparison_operator_symbol": ">="}, 
    {"comparison_operator_code": "__le__", "comparison_operator_label": "Less Than or Equal", "comparison_operator_symbol": "<="}, 
    {"comparison_operator_code": "__eq__", "comparison_operator_label": "Equal", "comparison_operator_symbol": "="}, 
    {"comparison_operator_code": "__ne__", "comparison_operator_label": "Not Equal", "comparison_operator_symbol": "!="}, 
]


CONFIG_PRODUCT = {
    "product_code": "CI", 
    "product_label": "Critical Illness", 
    "product_effective_date": '1900-01-01',
    "product_expiration_date": '9999-12-31'
}


CONFIG_PRODUCT_STATES = [
  {
    "state_id": 1,
    "state_effective_date": "1900-01-01",
    "state_expiration_date": "9999-12-31"
  },
  {
    "state_id": 2,
    "state_effective_date": "1900-01-01",
    "state_expiration_date": "9999-12-31"
  },
  {
    "state_id": 3,
    "state_effective_date": "1900-01-01",
    "state_expiration_date": "9999-12-31"
  },
  {
    "state_id": 4,
    "state_effective_date": "1900-01-01",
    "state_expiration_date": "9999-12-31"
  }
]



CONFIG_PRODUCT_VARIATION = {
    "product_variation_code": "issue_age", 
    "product_variation_label": "Issue Age", 
    "product_variation_effective_date": '1900-01-01', 
    "product_variation_expiration_date": '9999-12-31', 
    "is_gender_rated": False, 
    "is_age_rated": True, 
    "is_tobacco_rated": True, 
    "is_family_code_rated": True, 
    "vary_by_gender": False, 
    "vary_by_tobacco": True, 
    "family_code_rating_algorithm_code": "TIER4", 
    "min_issue_age": 18, 
    "max_issue_age": 99
}


CONFIG_COVERAGE = {
    "coverage_code": "base", 
    "coverage_label": "Base", 
    "section_code": "main", 
    "default_value": True
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

CONFIG_BENEFIT = [
  {
      "state_id":0,
      "benefit_effective_date":"1900-01-01",
      "benefit_expiration_date":"9999-12-31",
      "min_value":"0",
      "max_value":"100",
      "step_value":"2.5",
      "default_value":"100",
      "unit_code":"Percent",
      "is_durational":False,
      "benefit_code":"cancer",
      "ref_benefit":{
          "benefit_code":"cancer",
          "benefit_label":"Internal Cancer"
      }, 
      "child_states": [
        {
          "state_id": 1,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "cancer"
        },
        {
          "state_id": 2,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "cancer"
        },
        {
          "state_id": 3,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "cancer"
        },
        {
          "state_id": 4,
          "benefit_effective_date": "2023-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "cancer"
        }
      ]
  }, 
  {
      "state_id":0,
      "benefit_effective_date":"1900-01-01",
      "benefit_expiration_date":"9999-12-31",
      "min_value":"0",
      "max_value":"100",
      "step_value":"2.5",
      "default_value":"100",
      "unit_code":"Percent",
      "is_durational":False,
      "benefit_code":"heart_attack",
      "ref_benefit":{
          "benefit_code":"heart_attack",
          "benefit_label":"Heart Attack"
      }, 
      "child_states": [
        {
          "state_id": 1,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "heart_attack"
        },
        {
          "state_id": 2,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "heart_attack"
        },
        {
          "state_id": 3,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "heart_attack"
        },
        {
          "state_id": 4,
          "benefit_effective_date": "2023-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "heart_attack"
        }
      ]
  }, 
  {
      "state_id":0,
      "benefit_effective_date":"1900-01-01",
      "benefit_expiration_date":"9999-12-31",
      "min_value":"0",
      "max_value":"100",
      "step_value":"2.5",
      "default_value":"100",
      "unit_code":"Percent",
      "is_durational":False,
      "benefit_code":"stroke",
      "ref_benefit":{
          "benefit_code":"stroke",
          "benefit_label":"Stroke"
      }, 
      "child_states": [
        {
          "state_id": 1,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "stroke"
        },
        {
          "state_id": 2,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "stroke"
        },
        {
          "state_id": 3,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "stroke"
        },
        {
          "state_id": 4,
          "benefit_effective_date": "2023-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "stroke"
        }
      ]
  }, 
  {
      "state_id":0,
      "benefit_effective_date":"1900-01-01",
      "benefit_expiration_date":"9999-12-31",
      "min_value":"0",
      "max_value":"100",
      "step_value":"2.5",
      "default_value":"100",
      "unit_code":"Percent",
      "is_durational":False,
      "benefit_code":"transplant",
      "ref_benefit":{
          "benefit_code":"transplant",
          "benefit_label":"Major Organ Transplant"
      }, 
      "child_states": [
        {
          "state_id": 1,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "transplant"
        },
        {
          "state_id": 2,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "transplant"
        },
        {
          "state_id": 3,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "transplant"
        },
        {
          "state_id": 4,
          "benefit_effective_date": "2023-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "transplant"
        }
      ]
  }, 
  {
      "state_id":0,
      "benefit_effective_date":"1900-01-01",
      "benefit_expiration_date":"9999-12-31",
      "min_value":"0",
      "max_value":"100",
      "step_value":"2.5",
      "default_value":"100",
      "unit_code":"Percent",
      "is_durational":False,
      "benefit_code":"renal_failure",
      "ref_benefit":{
          "benefit_code":"renal_failure",
          "benefit_label":"End Stage Renal Failure"
      }, 
      "child_states": [
        {
          "state_id": 1,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "renal_failure"
        },
        {
          "state_id": 2,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "renal_failure"
        },
        {
          "state_id": 3,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "renal_failure"
        },
        {
          "state_id": 4,
          "benefit_effective_date": "2023-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "renal_failure"
        }
      ]
  }, 
  {
      "state_id":0,
      "benefit_effective_date":"1900-01-01",
      "benefit_expiration_date":"9999-12-31",
      "min_value":"0",
      "max_value":"100",
      "step_value":"2.5",
      "default_value":"25",
      "unit_code":"Percent",
      "is_durational":False,
      "benefit_code":"alzheimers",
      "ref_benefit":{
          "benefit_code":"alzheimers",
          "benefit_label":"Advanced Alzheimer's"
      }, 
      "child_states": [
        {
          "state_id": 1,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "alzheimers"
        },
        {
          "state_id": 2,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "alzheimers"
        },
        {
          "state_id": 3,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "alzheimers"
        },
        {
          "state_id": 4,
          "benefit_effective_date": "2023-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "alzheimers"
        }
      ]
  }, 
  {
      "state_id":0,
      "benefit_effective_date":"1900-01-01",
      "benefit_expiration_date":"9999-12-31",
      "min_value":"0",
      "max_value":"100",
      "step_value":"2.5",
      "default_value":"100",
      "unit_code":"Percent",
      "is_durational":False,
      "benefit_code":"parkinsons",
      "ref_benefit":{
          "benefit_code":"parkinsons",
          "benefit_label":"Parkinson's Disease"
      }, 
      "child_states": [
        {
          "state_id": 1,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "parkinsons"
        },
        {
          "state_id": 2,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "parkinsons"
        },
        {
          "state_id": 3,
          "benefit_effective_date": "1900-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "parkinsons"
        },
        {
          "state_id": 4,
          "benefit_effective_date": "2023-01-01",
          "benefit_expiration_date": "9999-12-31",
          "benefit_code": "parkinsons"
        }
      ]
  }, 
]



CONFIG_PROVISION = [
  {
    "provision_code": "group_size",
    "provision_effective_date": "1900-01-01",
    "provision_expiration_date": "9999-12-31",
    "provision": {
        "provision_label": "Group Size",
        "provision_code": "group_size",
    },
    "states": [
        {
            "state_id": 1,
            "state_effective_date": "1900-01-01",
            "state_expiration_date": "9999-12-31",
        }, 
        {
            "state_id": 2,
            "state_effective_date": "1900-01-01",
            "state_expiration_date": "9999-12-31",
        }, 
        {
            "state_id": 3,
            "state_effective_date": "1900-01-01",
            "state_expiration_date": "9999-12-31",
        }, 
        {
            "state_id": 4,
            "state_effective_date": "1900-01-01",
            "state_expiration_date": "9999-12-31",
        }, 
    ],
  }, 
  {
    "provision_code": "prex",
    "provision_effective_date": "1900-01-01",
    "provision_expiration_date": "9999-12-31",
    "provision": {
        "provision_label": "Pre-Existing Condition Limitation",
        "provision_code": "prex",
    },
    "states": [
        {
            "state_id": 1,
            "state_effective_date": "1900-01-01",
            "state_expiration_date": "9999-12-31",
        }, 
        {
            "state_id": 2,
            "state_effective_date": "1900-01-01",
            "state_expiration_date": "9999-12-31",
        }, 
        {
            "state_id": 3,
            "state_effective_date": "1900-01-01",
            "state_expiration_date": "9999-12-31",
        }, 
        {
            "state_id": 4,
            "state_effective_date": "1900-01-01",
            "state_expiration_date": "9999-12-31",
        }, 
    ],
  }, 
]


CONFIG_PROVISION_UI = {
  "group_size": {
        "ui_label": "Group Size",
        "component_type": "INPUT",
        "input_type": "number",
        "min_value": 0.0,
        "step_value": 1.0,
        "max_value": 9999999.0,
        "component_type_code": "v-text-field"
  }, 
  "prex": {
        "ui_label": "Pre-Existing Condition Limitation",
        "component_type": "SELECT",
        "component_type_code": "v-select", 
        "item_text": "item_label", 
        "item_value": "item_code", 
        "items": [
          {"item_label": "No Pre-Ex", "item_code": "none"}, 
          {"item_label": "12/12", "item_code": "12-12"}, 
          {"item_label": "3/12", "item_code": "3-12"}, 
          {"item_label": "6/12", "item_code": "6-12"},
        ]
    },
}

CONFIG_FACTORS = {
  "group_size": [
      {
          "factor_rules": [
              {
                  "class_name": "provision",
                  "field_name": "provision_value",
                  "comparison_operator_code": "__lt__",
                  "field_value": "1000",
                  "field_value_data_type": "number",
              }
          ],
          "factor_priority": 0,
          "factor_value": 1.2,
      }, 
      {
          "factor_rules": [
              {
                  "class_name": "provision",
                  "field_name": "provision_value",
                  "comparison_operator_code": "__lt__",
                  "field_value": "5000",
                  "field_value_data_type": "number",
              }
          ],
          "factor_priority": 1,
          "factor_value": 0.91,
      }, 
      {
          "factor_rules": [
              {
                  "class_name": "provision",
                  "field_name": "provision_value",
                  "comparison_operator_code": "__ge__",
                  "field_value": "5000",
                  "field_value_data_type": "number",
              }
          ],
          "factor_priority": 2,
          "factor_value": 0.83,
      }, 
    ], 
    "prex": [
      {
          "factor_rules": [
              {
                  "class_name": "provision",
                  "field_name": "provision_value",
                  "comparison_operator_code": "__eq__",
                  "field_value": "none",
                  "field_value_data_type": "string",
              }
          ],
          "factor_priority": 0,
          "factor_value": 1,
      }, 
      {
          "factor_rules": [
              {
                  "class_name": "provision",
                  "field_name": "provision_value",
                  "comparison_operator_code": "__eq__",
                  "field_value": "12-12",
                  "field_value_data_type": "string",
              }
          ],
          "factor_priority": 1,
          "factor_value": 0.87,
      }, 
      {
          "factor_rules": [
              {
                  "class_name": "provision",
                  "field_name": "provision_value",
                  "comparison_operator_code": "__eq__",
                  "field_value": "3-12",
                  "field_value_data_type": "string",
              }
          ],
          "factor_priority": 2,
          "factor_value": 0.95,
      }, 
      {
          "factor_rules": [
              {
                  "class_name": "provision",
                  "field_name": "provision_value",
                  "comparison_operator_code": "__eq__",
                  "field_value": "6-12",
                  "field_value_data_type": "string",
              }
          ],
          "factor_priority": 3,
          "factor_value": 0.93,
      }, 
    ]
}




# CONFIG_BENEFIT_DURATION = {
#   "benefit_duration_code": "dur1",
#   "duration": { "duration_code": "dur1", "duration_label": "Duration 1" },
#   "default_duration_item_code": "item3",
#   "duration_items": [
#     {
#       "item_code": "item1",
#       "benefit_duration_factor": "1.1",
#       "duration_item": { "item_code": "item1", "item_label": "Item 1" }
#     },
#     {
#       "item_code": "item2",
#       "benefit_duration_factor": "1.2",
#       "duration_item": { "item_code": "item2", "item_label": "Item 2" }
#     },
#     {
#       "item_code": "item3",
#       "benefit_duration_factor": "1.3",
#       "duration_item": { "item_code": "item3", "item_label": "Item 3" }
#     }
#   ]
# }



AGE_DISTRIBUTION =  {
  "age_distribution_set_label": "Normal(45,15) Age Distribution", 
  "age_distribution": [
    { 'age': 18, 'weight': 49.6 },
    { 'age': 19, 'weight': 55.9 },
    { 'age': 20, 'weight': 62.7 },
    { 'age': 21, 'weight': 70.1 },
    { 'age': 22, 'weight': 78.0 },
    { 'age': 23, 'weight': 86.4 },
    { 'age': 24, 'weight': 95.2 },
    { 'age': 25, 'weight': 104.5 },
    { 'age': 26, 'weight': 114.3 },
    { 'age': 27, 'weight': 124.3 },
    { 'age': 28, 'weight': 134.7 },
    { 'age': 29, 'weight': 145.2 },
    { 'age': 30, 'weight': 155.9 },
    { 'age': 31, 'weight': 166.7 },
    { 'age': 32, 'weight': 177.4 },
    { 'age': 33, 'weight': 187.9 },
    { 'age': 34, 'weight': 198.2 },
    { 'age': 35, 'weight': 208.1 },
    { 'age': 36, 'weight': 217.6 },
    { 'age': 37, 'weight': 226.5 },
    { 'age': 38, 'weight': 234.7 },
    { 'age': 39, 'weight': 242.1 },
    { 'age': 40, 'weight': 248.6 },
    { 'age': 41, 'weight': 254.2 },
    { 'age': 42, 'weight': 258.8 },
    { 'age': 43, 'weight': 262.2 },
    { 'age': 44, 'weight': 264.6 },
    { 'age': 45, 'weight': 265.8 },
    { 'age': 46, 'weight': 265.8 },
    { 'age': 47, 'weight': 264.6 },
    { 'age': 48, 'weight': 262.2 },
    { 'age': 49, 'weight': 258.8 },
    { 'age': 50, 'weight': 254.2 },
    { 'age': 51, 'weight': 248.6 },
    { 'age': 52, 'weight': 242.1 },
    { 'age': 53, 'weight': 234.7 },
    { 'age': 54, 'weight': 226.5 },
    { 'age': 55, 'weight': 217.6 },
    { 'age': 56, 'weight': 208.1 },
    { 'age': 57, 'weight': 198.2 },
    { 'age': 58, 'weight': 187.9 },
    { 'age': 59, 'weight': 177.4 },
    { 'age': 60, 'weight': 166.7 },
    { 'age': 61, 'weight': 155.9 },
    { 'age': 62, 'weight': 145.2 },
    { 'age': 63, 'weight': 134.7 },
    { 'age': 64, 'weight': 124.3 },
    { 'age': 65, 'weight': 114.3 },
    { 'age': 66, 'weight': 104.5 },
    { 'age': 67, 'weight': 95.2 },
    { 'age': 68, 'weight': 86.4 },
    { 'age': 69, 'weight': 78.0 },
    { 'age': 70, 'weight': 70.1 },
    { 'age': 71, 'weight': 62.7 },
    { 'age': 72, 'weight': 55.9 },
    { 'age': 73, 'weight': 49.6 },
    { 'age': 74, 'weight': 43.8 },
    { 'age': 75, 'weight': 38.5 },
    { 'age': 76, 'weight': 33.7 },
    { 'age': 77, 'weight': 29.3 },
    { 'age': 78, 'weight': 25.5 },
    { 'age': 79, 'weight': 22.0 },
  ]
};


SEX_DISTINCT_DISTRIBUTION = {
  "attr_type_code": "gender", 
  "attr_distribution_set_label": "Male/Female", 
  "attr_distribution": [
    {"attr_value": "M", "weight": 1}, 
    {"attr_value": "F", "weight": 1}, 
  ]
}

UNISEX_DISTRIBUTION = {
  "attr_type_code": "gender", 
  "attr_distribution_set_label": "50/50 Male/Female", 
  "attr_distribution": [
    {"attr_value": "M", "weight": 0.5}, 
    {"attr_value": "F", "weight": 0.5}, 
  ]
}

SMOKER_DISTINCT_DISTRIBUTION =  {
  "attr_type_code": "smoker_status", 
  "attr_distribution_set_label": "Non-Smoker/Smoker", 
  "attr_distribution": [
    {"attr_value": "N", "weight": 1}, 
    {"attr_value": "T", "weight": 1},
  ]
}
UNISMOKER_DISTRIBUTION =  {
  "attr_type_code": "smoker_status", 
  "attr_distribution_set_label": "85/15 Non-Smoker/Smoker", 
  "attr_distribution": [
    {"attr_value": "N", "weight": 0.85}, 
    {"attr_value": "T", "weight": 0.15},
  ]
}