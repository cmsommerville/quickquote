from app.shared import CRUD_ResourceFactory
from ..models import *
from ..schemas import *
from ..resources import *



product_routes = [
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_Config_Product', 
            model=Model_ConfigProduct, 
            schema=Schema_ConfigProduct,
            primary_key='product_id'
        ).generate_class(), 
        "endpoints": ['/config/product/<int:id>', '/config/product']
    },
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_Config_ProductStateAvailability', 
            model=Model_ConfigProductStateAvailability, 
            schema=Schema_ConfigProductStateAvailability,
            primary_key='product_state_id'
        ).generate_class(), 
        "endpoints": ['/config/product/state/<int:id>', '/config/product/state']
    }, 
]

product_variations_routes = [
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_Config_AgeBandSet', 
            model=Model_ConfigAgeBandSet, 
            schema=Schema_ConfigAgeBandSet, 
            primary_key='age_band_set_id'
        ).generate_class(), 
        "endpoints": ['/config/age-band-set/<int:id>', '/config/age-band-set']
    }, 
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_Config_AgeBand', 
            model=Model_ConfigAgeBand,
            schema=Schema_ConfigAgeBand, 
            primary_key='age_band_id'
        ).generate_class(), 
        "endpoints": ['/config/age-band/<int:id>', '/config/age-band']
    }, 
]

rate_group_routes = [
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_RateGroupConfig', 
            model=Model_ConfigRateGroup, 
            schema=Schema_ConfigRateGroup, 
            primary_key='rate_group_id'
        ).generate_class(), 
        "endpoints": ['/config/rate-group/<int:id>', '/config/rate-group']
    }, 
]

coverage_routes = [
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_CoverageConfig', 
            model=Model_ConfigCoverage, 
            schema=Schema_ConfigCoverage, 
            primary_key='coverage_id'
        ).generate_class(), 
        "endpoints": ['/config/coverage/<int:id>', '/config/coverage']
    }, 
]

benefit_routes = [
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_BenefitConfig', 
            model=Model_ConfigBenefit, 
            schema=Schema_ConfigBenefit, 
            primary_key='benefit_id'
        ).generate_class(), 
        "endpoints": ['/config/benefit/<int:id>', '/config/benefit']
    }, 
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_BenefitProvisionConfig', 
            model=Model_ConfigBenefitProvision, 
            schema=Schema_ConfigBenefitProvision,
            primary_key='benefit_provision_id'
        ).generate_class(), 
        "endpoints": ['/config/benefit-provisions']
    }, 
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_BenefitDurationConfig', 
            model=Model_ConfigBenefitDuration, 
            schema=Schema_ConfigBenefitDuration,
            primary_key='benefit_duration_id'
        ).generate_class(), 
        "endpoints": ['/config/benefit-duration/<int:id>', '/config/benefit-duration']
    }, 
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_BenefitDurationItemConfig', 
            model=Model_ConfigBenefitDurationItem, 
            schema=Schema_ConfigBenefitDurationItem,
            primary_key='benefit_duration_item_id'
        ).generate_class(), 
        "endpoints": ['/config/benefit-duration-item/<int:id>', '/config/benefit-duration-item']
    }, 
]

provision_routes = [
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_ProvisionConfig', 
            model=Model_ConfigProvision,
            schema=Schema_ConfigProvision, 
            primary_key='provision_id'
        ).generate_class(), 
        "endpoints": ['/config/provision/<int:id>', '/config/provision']
    }, 
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_ProvisionStateAvailabilityConfig', 
            model=Model_ConfigProvisionStateAvailability,
            schema=Schema_ConfigProvisionStateAvailability, 
            primary_key='provision_state_id'
        ).generate_class(), 
        "endpoints": ['/config/provision/state/<int:id>', '/config/provision/state']
    }, 
]

factor_routes = [
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_FactorConfig', 
            model=Model_ConfigFactor,
            schema=Schema_ConfigFactor, 
            primary_key='factor_id'
        ).generate_class(), 
        "endpoints": ['/config/factor/<int:id>', '/config/factor']
    }, 
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_FactorRuleConfig', 
            model=Model_ConfigFactorRule,
            schema=Schema_ConfigFactorRule, 
            primary_key='factor_rule_id'
        ).generate_class(), 
        "endpoints": ['/config/factor-rule/<int:id>', '/config/factor-rule']
    }, 
]

ref_data_routes = [
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_RefStates', 
            model=Model_RefStates,
            schema=Schema_RefStates, 
            primary_key='state_id'
        ).generate_class(), 
        "endpoints": ['/config/ref-state/<string:id>', '/config/ref-state']
    }, 
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_RefRatingAlgorithm', 
            model=Model_RefRatingAlgorithm,
            schema=Schema_RefRatingAlgorithm, 
            primary_key='rating_algorithm_code'
        ).generate_class(), 
        "endpoints": ['/config/ref-rating-algorithm/<string:id>', '/config/ref-rating-algorithm']
    }, 
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_RefUnitCode', 
            model=Model_RefUnitCode, 
            schema=Schema_RefUnitCode, 
            primary_key='unit_code'
        ).generate_class(), 
        "endpoints": ['/config/ref-unit-code/<string:id>', '/config/ref-unit-code']
    }, 
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_RefComponentTypes', 
            model=Model_RefComponentTypes,
            schema=Schema_RefComponentTypes, 
            primary_key='component_type_code'
        ).generate_class(), 
        "endpoints": ['/config/ref-component-type/<string:id>', '/config/ref-component-type']
    }, 
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_RefTextFieldTypes', 
            model=Model_RefTextFieldTypes,
            schema=Schema_RefTextFieldTypes, 
            primary_key='type_code'
        ).generate_class(), 
        "endpoints": ['/config/ref-text-field-type/<string:id>', '/config/ref-text-field-type']
    }, 
    { 
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_RefComparisonOperator', 
            model=Model_RefComparisonOperator,
            schema=Schema_RefComparisonOperator, 
            primary_key='comparison_operator_code'
        ).generate_class(), 
        "endpoints": ['/config/ref-comparison-operator/<string:id>', '/config/ref-comparison-operator']
    }, 
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_RefInterpolationRule', 
            model=Model_RefInterpolationRule,
            schema=Schema_RefInterpolationRule, 
            primary_key='interpolation_rule_code'
        ).generate_class(), 
        "endpoints": ['/config/ref-interpolation-rule/<string:id>', '/config/ref-interpolation-rule']
    }, 
]

rating_routes = [
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_ConfigAgeDistributionSet', 
            model=Model_ConfigAgeDistributionSet,
            schema=Schema_ConfigAgeDistributionSet, 
            primary_key='age_distribution_set_id'
        ).generate_class(), 
        "endpoints": ['/config/age-distribution-set/<int:id>', '/config/age-distribution-set']
    }, 
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_ConfigSmokerDistributionSet', 
            model=Model_ConfigAttributeDistributionSet,
            schema=Schema_ConfigAttributeDistributionSet, 
            primary_key='attr_distribution_set_id'
        ).generate_class(), 
        "endpoints": ['/config/attr-distribution-set/<int:id>', '/config/attr-distribution-set']
    }, 
]

custom_crud_routes = [
    {
        "class": CRUD_ProductVariation, 
        "endpoints": ['/config/product-variations/<int:id>', '/config/product-variations']
    }, 
    {
        "class": CRUD_ProvisionUIComponentConfig, 
        "endpoints": ['/config/provision-ui-component/<int:id>', '/config/provision-ui-component']
    }, 
    {
        "class": CRUD_BenefitStateAvailabilityConfig,
        "endpoints": ['/config/benefit-states/<int:id>']
    }, 
    {
        "class": CRUD_BenefitProductVariationConfig,
        "endpoints": ['/config/benefit-product-variations']
    }, 
]

product_list_routes = [
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_Config_ProductStateAvailability_List', 
            model=Model_ConfigProductStateAvailability, 
            schema=Schema_ConfigProductStateAvailability,
            primary_key='product_state_id'
        ).generate_list_class(), 
        "endpoints": ['/config/product/states/<int:id>', '/config/product/states']
    }, 
]

product_variation_list_routes = [
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_Config_AgeBandSet_List', 
            model=Model_ConfigAgeBandSet, 
            schema=Schema_ConfigAgeBandSet,
            primary_key='age_band_set_id'
        ).generate_list_class(), 
        "endpoints": ['/config/age-band-sets']
    }, 
]


benefit_list_routes = [
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_BenefitConfig_List', 
            model=Model_ConfigBenefit, 
            schema=Schema_ConfigBenefit, 
            primary_key='benefit_id'
        ).generate_list_class(), 
        "endpoints": ['/config/benefits']
    }, 
 ]

provision_list_routes = [
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_ProvisionStateAvailabilityConfig_List', 
            model=Model_ConfigProvisionStateAvailability,
            schema=Schema_ConfigProvisionStateAvailability, 
            primary_key='provision_state_id'
        ).generate_list_class(), 
        "endpoints": ['/config/provision/states']
    }, 
]

factor_list_routes = [
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_FactorConfig_List', 
            model=Model_ConfigFactor,
            schema=Schema_ConfigFactor, 
            primary_key='factor_id'
        ).generate_list_class(), 
        "endpoints": ['/config/factors']
    }, 
]

ref_data_list_routes = [
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_RefStates_List', 
            model=Model_RefStates,
            schema=Schema_RefStates, 
            primary_key='state_id'
        ).generate_list_class(), 
        "endpoints": ['/config/ref-states']
    }, 
    {
        "class": CRUD_ResourceFactory(
            resource_name='CRUD_RefUnitCode_List', 
            model=Model_RefUnitCode,
            schema=Schema_RefUnitCode, 
            primary_key='unit_code'
        ).generate_list_class(), 
        "endpoints": ['/config/ref-unit-codes']
    }, 
]
