from .Config_Coverage import *
from .Config_Product import *
from .Config_ProductVariations import *
from .Config_Provision import *
from .Config_RefTables import *
from .Config_Benefit import *
from .Query_Product import *
from .Query_Coverage import *
from .Query_Provision import *
from .Query_AgeBands import *

routes = [
    {
        "class": CRUD_ProductConfig, 
        "endpoints": ['/config/product/<int:id>', '/config/product']
    }, 
    {
        "class": CRUD_ProductStateAvailabilityConfig, 
        "endpoints": ['/config/product/state/<int:id>', '/config/product/state']
    }, 
    {
        "class": CRUD_ProductVariationsConfig, 
        "endpoints": ['/config/product-variations/<int:id>', '/config/product-variations']
    }, 
    {
        "class": CRUD_AgeBandsSetConfig, 
        "endpoints": ['/config/age-band-set/<int:id>', '/config/age-band-set']
    }, 
    {
        "class": CRUD_AgeBandsConfig, 
        "endpoints": ['/config/age-band/<int:id>', '/config/age-band']
    }, 

    {
        "class": CRUD_CoverageConfig, 
        "endpoints": ['/config/coverage/<int:id>', '/config/coverage']
    }, 
    {
        "class": CRUD_CoverageStateAvailabilityConfig, 
        "endpoints": ['/config/coverage/state/<int:id>', '/config/coverage/state']
    }, 

    {
        "class": CRUD_BenefitConfig, 
        "endpoints": ['/config/benefit/<int:id>', '/config/benefit']
    }, 
    {
        "class": CRUD_BenefitStateAvailabilityConfig, 
        "endpoints": ['/config/benefit/state/<int:id>', '/config/benefit/state']
    }, 
    {
        "class": CRUD_BenefitDurationConfig, 
        "endpoints": ['/config/benefit-duration/<int:id>', '/config/benefit-duration']
    }, 
    {
        "class": CRUD_BenefitDurationItemsConfig, 
        "endpoints": ['/config/benefit-duration-item/<int:id>', '/config/benefit-duration-item']
    }, 

    {
        "class": CRUD_ProvisionConfig, 
        "endpoints": ['/config/provision/<int:id>', '/config/provision']
    }, 
    {
        "class": CRUD_ProvisionStateAvailabilityConfig, 
        "endpoints": ['/config/provision/state/<int:id>', '/config/provision/state']
    }, 
    {
        "class": CRUD_ProvisionUIComponentConfig, 
        "endpoints": ['/config/provision-ui-component/<int:id>', '/config/provision-ui-component']
    }, 

    {
        "class": CRUD_RefStates, 
        "endpoints": ['/config/ref-states/<string:code>', '/config/ref-states']
    }, 

    {
        "class": Query_ProductStateConfig, 
        "endpoints": ['/qry-config/product']
    }, 
    {
        "class": Query_CoverageStateConfig, 
        "endpoints": ['/qry-config/coverage']
    }, 
    {
        "class": Query_ProvisionStateConfig, 
        "endpoints": ['/qry-config/provision']
    }, 
    {
        "class": Query_AgeBandsStateConfig, 
        "endpoints": ['/qry-config/age-bands']
    }, 
    
]
