policy = {
    "name": "accident",
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
            "name": "frac_disl",
            "mandatory": True,
            "editable": True
        },
        {
            "name": "hospitalization",
            "mandatory": True,
            "editable": False
        },
        {
            "name": "life_changing_events",
            "prohibited": True,
            "editable": False
        }
    ],
    "provisions": [
        {
            "name": "occ_class",
            "states": "inherit"
        },
        {
            "name": "ac_factor1",
            "states": "inherit"
        },
        {
            "name": "group_size",
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
            "name": "frac_skull",
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
            "name": "frac_ankle",
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
            "name": "frac_wrist",
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
            "name": "hosp_adm",
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
            "name": "hosp_conf",
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
                    "name": "hosp_confinement_days",
                    "items": [
                        {"value": 30, "text": 30, "factor": 1},
                        {"value": 365, "text": 365, "factor": 1.47}
                    ]
                }
            ],
            "states": "inherit"
        },
        {
            "name": "icu_conf",
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
                    "name": "icu_confinement_days",
                    "items": [
                        {"value": 10, "text": 10, "factor": 1},
                        {"value": 30, "text": 30, "factor": 1.2}
                    ]
                }
            ],
            "states": "inherit"
        },
        {
            "name": "quad",
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
            "name": "para",
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
