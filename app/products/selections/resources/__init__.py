# expose all selections resources
from .Selections_Plan import PlanSelections
from .Selections_CoverageBenefit import CoverageBenefitSelections
from .Selections_Provision import ProvisionSelections
from .Selections_AgeBands import AgeBandsSelections
from .Calculator_Rating import RatingCalculatorResource
from .Config_RateTable import RateTableList
from .Search_Plan import PlanSearch


routes = [
    {
        "class": PlanSelections, 
        "endpoints": ['/selections/plan']
    },
    {
        "class": AgeBandsSelections, 
        "endpoints": ['/selections/age-bands']
    },
    {
        "class": CoverageBenefitSelections, 
        "endpoints": ['/selections/benefits']
    },
    {
        "class": ProvisionSelections, 
        "endpoints": ['/selections/provisions']
    },
    {
        "class": RatingCalculatorResource, 
        "endpoints": ['/selections/rating-calculator']
    },
    {
        "class": PlanSearch, 
        "endpoints": ['/search/plan']
    },
]
