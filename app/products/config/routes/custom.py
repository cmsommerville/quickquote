from ..resources import *


custom_routes = [
    {
        "class": Query_AllProductStates, 
        "endpoints": ['/qry-config/all-product-states']
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
        "class": Query_AllAgeBandsByProduct, 
        "endpoints": ['/qry-config/product/<int:product_id>/all-age-bands']
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
    {
        "class": Query_AttrDistributionSets, 
        "endpoints": ['/qry-config/attr-distribution-sets']
    }, 
    {
        "class": Query_AgeDistributionSets, 
        "endpoints": ['/qry-config/age-distribution-sets']
    }, 
]