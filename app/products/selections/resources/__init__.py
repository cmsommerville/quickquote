# expose all selections resources
from .Resource_SelectionPlan import *
from .Resource_SelectionBenefit import *
from .Resource_SelectionAgeBands import * 
from .Resource_SelectionProvision import * 
from .Resource_SelectionFactors import *
from .Resource_SelectionDistribution import *
from .Resource_RatingMain import *
from .Config_RateTable import RateTableList
from .Search_Plan import PlanSearch


routes = [
    {
        "class": Resource_SelectionPlan, 
        "endpoints": ['/selections/plan/<int:plan_id>', '/selections/plan']
    },
    {
        "class": Resource_SelectionBenefit, 
        "endpoints": ['/selections/plan/<int:plan_id>/benefits']
    },
    {
        "class": Resource_SelectionAgeBands, 
        "endpoints": ['/selections/plan/<int:plan_id>/age-bands']
    },
    {
        "class": Resource_SelectionProvision, 
        "endpoints": ['/selections/plan/<int:plan_id>/provisions']
    },
    {
        "class": Resource_SelectionFactors, 
        "endpoints": ['/selections/plan/<int:plan_id>/factors']
    },
    {
        "class": RateTableList, 
        "endpoints": ['/config/rate-table']
    },
    {
        "class": Resource_SelectionDistribution, 
        "endpoints": ['/selections/plan/<int:plan_id>/dist']
    },
    {
        "class": Resource_SelectionRateGroupSummary, 
        "endpoints": ['/selections/plan/<int:plan_id>/rates']
    },
    {
        "class": PlanSearch, 
        "endpoints": ['/search/plan']
    },
]
