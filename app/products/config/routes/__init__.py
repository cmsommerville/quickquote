from .crud import *
from .custom import *

routes = [
    *product_routes, 
    *product_variations_routes, 
    *coverage_routes, 
    *rate_group_routes, 
    *benefit_routes, 
    *provision_routes, 
    *factor_routes, 
    *ref_data_routes,
    *rating_routes, 
    *custom_crud_routes,  

    *product_list_routes, 
    *benefit_list_routes, 
    *provision_list_routes,
    *factor_list_routes, 
    *ref_data_list_routes, 

    *custom_routes
]