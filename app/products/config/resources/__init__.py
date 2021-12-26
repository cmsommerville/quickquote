from .Config_Coverage import *
from .Config_Product import *
from .Config_ProductVariations import *
from .Config_Provision import *
from .Config_RefTables import *
from .Config_RateGroup import *
from .Config_Benefit import *
from .Config_Factor import *
from .Query_Product import *
from .Query_Coverage import *
from .Query_Benefit import *
from .Query_Provision import *
from .Query_AgeBands import *
from .Query_ProductVariations import *
from .Query_RateGroup import *
from .Query_Factor import *

# from ..models.models.Ref_Benefit import RF_Ref_Benefit

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
        "class": CRUD_RateGroupConfig, 
        "endpoints": ['/config/rate-group/<int:id>', '/config/rate-group']
    }, 
    {
        "class": CRUD_CoverageConfig, 
        "endpoints": ['/config/coverage/<int:id>', '/config/coverage']
    }, 

    {
        "class": CRUD_BenefitConfig, 
        "endpoints": ['/config/benefit/<int:id>', '/config/benefit']
    }, 
    {
        "class": CRUD_BenefitStateAvailabilityConfig, 
        "endpoints": ['/config/benefit-state/<int:id>']
    }, 
    {
        "class": CRUD_BenefitProductVariationConfig, 
        "endpoints": ['/config/benefit-product-variations']
    }, 
    {
        "class": CRUD_BenefitProvisionConfig, 
        "endpoints": ['/config/benefit-provisions']
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
        "class": CRUD_ProvisionUIComponent_TextFieldConfig, 
        "endpoints": ['/config/provision-ui-component-text-field/<int:id>', '/config/provision-ui-component-text-field']
    }, 
    {
        "class": CRUD_ProvisionUIComponent_SelectItemConfig, 
        "endpoints": ['/config/provision-ui-component-select-item-field/<int:id>', '/config/provision-ui-component-select-item-field']
    }, 
    


    {
        "class": CRUD_FactorConfig, 
        "endpoints": ['/config/factor/<int:id>', '/config/factor']
    }, 
    {
        "class": CRUD_FactorRuleConfig, 
        "endpoints": ['/config/factor-rule/<int:id>', '/config/factor-rule']
    }, 


    {
        "class": CRUD_RefStates, 
        "endpoints": ['/config/ref-states/<string:code>', '/config/ref-states']
    }, 
    # {
    #     "class": RF_Ref_Benefit.generate_class(), 
    #     "endpoints": ['/config/ref-benefit/<id>', '/config/ref-benefit']
    # }, 
    {
        "class": CRUD_RefRatingAlgorithm, 
        "endpoints": ['/config/ref-rating-algorithm/<string:code>', '/config/ref-rating-algorithm']
    }, 
    {
        "class": CRUD_RefUnitCode, 
        "endpoints": ['/config/ref-unit-code/<string:code>', '/config/ref-unit-code']
    }, 
    {
        "class": CRUD_RefComponentTypes, 
        "endpoints": ['/config/ref-component-types']
    }, 
    {
        "class": CRUD_RefTextFieldTypes, 
        "endpoints": ['/config/ref-text-field-types']
    }, 
    {
        "class": CRUD_RefComparisonOperator, 
        "endpoints": ['/config/ref-comparison-operator/<string:code>', '/config/ref-comparison-operator']
    }, 
    {
        "class": CRUD_RefInterpolationRule, 
        "endpoints": ['/config/ref-interpolation-rule/<string:code>', '/config/ref-interpolation-rule']
    }, 
    

    {
        "class": Query_ProductStateConfig, 
        "endpoints": ['/qry-config/product-state']
    }, 
    {
        "class": Query_AllProducts, 
        "endpoints": ['/qry-config/all-products']
    }, 
    {
        "class": Query_AllProductVariations, 
        "endpoints": ['/qry-config/all-product-variations']
    }, 
    {
        "class": Query_AllAgeBands, 
        "endpoints": ['/qry-config/all-age-bands']
    }, 
    {
        "class": Query_AllCoverages,  
        "endpoints": ['/qry-config/all-coverages']
    }, 
    {
        "class": Query_AllBenefits,  
        "endpoints": ['/qry-config/all-benefits']
    }, 
    {
        "class": Query_AllBenefitDurations,  
        "endpoints": ['/qry-config/all-benefit-durations']
    }, 
    {
        "class": Query_AllProvisions, 
        "endpoints": ['/qry-config/all-provisions']
    }, 
    {
        "class": Query_AllProvisionStates, 
        "endpoints": ['/qry-config/all-provision-states']
    }, 
    {
        "class": Query_AllUIComponents, 
        "endpoints": ['/qry-config/all-ui-components']
    }, 
    {
        "class": Query_AllRateGroups, 
        "endpoints": ['/qry-config/all-rate-groups']
    }, 
    {
        "class": Query_CoverageStateConfig, 
        "endpoints": ['/qry-config/coverage-state']
    }, 
    {
        "class": Query_ProvisionStateConfig, 
        "endpoints": ['/qry-config/provision-state']
    }, 
    {
        "class": Query_AgeBandsStateConfig, 
        "endpoints": ['/qry-config/age-bands']
    }, 
    {
        "class": Query_AllFactors, 
        "endpoints": ['/qry-config/factors']
    }, 
    
]
