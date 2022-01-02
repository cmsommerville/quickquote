# expose all selections resources
from .Resource_SelectionPlan import *
from .Resource_BenefitProductVariation import *
# from .Selections_Provision import ProvisionSelections
# from .Selections_AgeBands import AgeBandsSelections
# from .Calculator_Rating import RatingCalculatorResource
# from .Config_RateTable import RateTableList
# from .Search_Plan import PlanSearch


routes = [
    {
        "class": Resource_SelectionPlan, 
        "endpoints": ['/selections/plan/<int:plan_id>', '/selections/plan']
    },
    {
        "class": Query_AllBenefitProductVariations, 
        "endpoints": ['/selections/plan/<int:plan_id>/benefit-product-variations']
    }, 
    # {
    #     "class": AgeBandsSelections, 
    #     "endpoints": ['/selections/age-bands']
    # },
    # {
    #     "class": ProvisionSelections, 
    #     "endpoints": ['/selections/provisions']
    # },
    # {
    #     "class": RatingCalculatorResource, 
    #     "endpoints": ['/selections/rating-calculator']
    # },
    # {
    #     "class": PlanSearch, 
    #     "endpoints": ['/search/plan']
    # },
]
