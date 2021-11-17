policy = [
    {
        "code": "critical_illness",
        "variations": [
            {
                "code": "issue_age",
            },
            {
                "code": "attained_age"
            }
        ],
        "states": [
            {
                "code": "SC",
                "effectiveDate": "2020-01-01",
                "expiryDate": "9999-12-31"
            },
            {
                "code": "NC",
                "effectiveDate": "2021-07-01",
                "expiryDate": "9999-12-31"
            }
        ],
        "coverages": [
            {
                "code": "base"
            },
            {
                "code": "progressive_disease"
            },
            {
                "code": "optional_benefits"
            }
        ],
        "provisions": [
            {
                "code": "prex",
                "states": "inherit"
            },
            {
                "code": "reductionAt70",
                "states": "inherit"
            },
            {
                "code": "group_size",
                "states": "inherit"
            }
        ],
        "benefits": [
            {
                "code": "heart_attack",
                "states": "inherit",
                "amounts": {
                    "default": 100,
                    "min": 0,
                    "max": 100,
                    "step": 6.25,
                    "unit": "percent"
                }
            },
            {
                "code": "cancer",
                "states": "inherit",
                "amounts": {
                    "default": 100,
                    "min": 0,
                    "max": 100,
                    "step": 6.25,
                    "unit": "percent"
                }
            },
            {
                "code": "ms",
                "states": "inherit",
                "amounts": {
                    "default": 100,
                    "min": 0,
                    "max": 100,
                    "step": 6.25,
                    "unit": "percent"
                }
            },
            {
                "code": "als",
                "states": "inherit",
                "amounts": {
                    "default": 100,
                    "min": 0,
                    "max": 100,
                    "step": 6.25,
                    "unit": "percent"
                }
            },
            {
                "code": "stroke",
                "states": "inherit",
                "amounts": {
                    "default": 100,
                    "min": 0,
                    "max": 100,
                    "step": 6.25,
                    "unit": "percent"
                }
            },
            {
                "code": "renal_failure",
                "states": "inherit",
                "amounts": {
                    "default": 100,
                    "min": 0,
                    "max": 100,
                    "step": 6.25,
                    "unit": "percent"
                }
            },
            {
                "code": "transplant",
                "states": "inherit",
                "amounts": {
                    "default": 100,
                    "min": 0,
                    "max": 100,
                    "step": 6.25,
                    "unit": "percent"
                }
            },
            {
                "code": "parkinsons",
                "states": "inherit",
                "amounts": {
                    "default": 100,
                    "min": 0,
                    "max": 100,
                    "step": 6.25,
                    "unit": "percent"
                }
            },
            {
                "code": "alzheimers",
                "states": "inherit",
                "amounts": {
                    "default": 100,
                    "min": 0,
                    "max": 100,
                    "step": 6.25,
                    "unit": "percent"
                }
            }
        ]
    },
    {
        "code": "accident",
        "text": "Accident",
        "variations": [
            {
                "value": "base"
            }
        ],
        "states": [
            {
                "code": "SC",
                "effectiveDate": "2020-01-01",
                "expiryDate": "9999-12-31"
            },
            {
                "code": "NC",
                "effectiveDate": "2021-07-01",
                "expiryDate": "9999-12-31"
            }
        ],
        "coverages": [
            {
                "code": "frac_disl",
                "mandatory": True,
                "editable": True
            },
            {
                "code": "hospitalization",
                "mandatory": True,
                "editable": False
            },
            {
                "code": "life_changing_events",
                "prohibited": True,
                "editable": False
            }
        ],
        "provisions": [
            {
                "code": "occ_class",
                "states": "inherit"
            },
            {
                "code": "ac_factor1",
                "states": "inherit"
            },
            {
                "code": "group_size",
                "states": [
                    {
                        "code": "SC",
                        "effectiveDate": "2020-01-01",
                        "expiryDate": "9999-12-31"
                    }
                ]
            }
        ],
        "benefits": [
            {
                "code": "frac_skull",
                "amounts": {
                    "default": 2000,
                    "min": 0,
                    "max": 5000,
                    "step": 25,
                    "unit": "dollar"
                },
                "states": "inherit"
            },
            {
                "code": "frac_ankle",
                "amounts": {
                    "default": 400,
                    "min": 0,
                    "max": 2500,
                    "step": 25,
                    "unit": "dollar"
                },
                "states": "inherit"
            },
            {
                "code": "frac_wrist",
                "amounts": {
                    "default": 300,
                    "min": 0,
                    "max": 2500,
                    "step": 25,
                    "unit": "dollar"
                },
                "states": "inherit"
            },
            {
                "code": "hosp_adm",
                "amounts": {
                    "default": 1000,
                    "min": 100,
                    "max": 5000,
                    "step": 50,
                    "unit": "dollar"
                },
                "states": "inherit"
            },
            {
                "code": "hosp_conf",
                "amounts": {
                    "default": 200,
                    "min": 50,
                    "max": 1000,
                    "step": 50,
                    "unit": "dollar"
                },
                "benefitFactors": [
                    {
                        "default": 30,
                        "code": "hosp_confinement_days",
                        "items": [
                            {"value": 30, "text": 30, "factor": 1},
                            {"value": 365, "text": 365, "factor": 1.47}
                        ]
                    }
                ],
                "states": "inherit"
            },
            {
                "code": "icu_conf",
                "amounts": {
                    "default": 100,
                    "min": 0,
                    "max": 500,
                    "step": 25,
                    "unit": "dollar"
                },
                "benefitFactors": [
                    {
                        "default": 10,
                        "code": "icu_confinement_days",
                        "items": [
                            {"value": 10, "text": 10, "factor": 1},
                            {"value": 30, "text": 30, "factor": 1.2}
                        ]
                    }
                ],
                "states": "inherit"
            },
            {
                "code": "quad",
                "amounts": {
                    "default": 5000,
                    "min": 0,
                    "max": 25000,
                    "step": 2500,
                    "unit": "dollar"
                },
                "states": "inherit"
            },
            {
                "code": "para",
                "amounts": {
                    "default": 2500,
                    "min": 0,
                    "max": 25000,
                    "step": 500,
                    "unit": "dollar"
                },
                "states": "inherit"
            }
        ]
    }
]
