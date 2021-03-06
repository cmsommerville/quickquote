import ConfigProductList from "../../views/config/ConfigProductList";
import ConfigProduct from "../../views/config/ConfigProduct";
import ConfigProductStates from "../../views/config/ConfigProductStates.vue";
import ConfigProductVariations from "../../views/config/ConfigProductVariations.vue";
import ConfigProductVariationsList from "../../views/config/ConfigProductVariationsList.vue";
import ConfigAgeBandsList from "../../views/config/ConfigAgeBandsList.vue";
import ConfigAgeBands from "../../views/config/ConfigAgeBands.vue";
import ConfigCoverageList from "../../views/config/ConfigCoverageList.vue";
import ConfigCoverage from "../../views/config/ConfigCoverage.vue";
import ConfigProvision from "../../views/config/ConfigProvision.vue";
import ConfigProvisionList from "../../views/config/ConfigProvisionList.vue";
import ConfigProvisionUI from "../../views/config/ConfigProvisionUI.vue";
import ConfigProvisionStates from "../../views/config/ConfigProvisionStates.vue";
import ConfigFactors from "../../views/config/ConfigFactors.vue";
import ConfigFactorRules from "../../views/config/ConfigFactorRules.vue";
import ConfigBenefitList from "../../views/config/ConfigBenefitList.vue";
import ConfigBenefit from "../../views/config/ConfigBenefit.vue";
import ConfigBenefitStates from "../../views/config/ConfigBenefitStates.vue";
import ConfigBenefitProductVariations from "../../views/config/ConfigBenefitProductVariations.vue";
import ConfigBenefitProvisions from "../../views/config/ConfigBenefitProvisions.vue";
import ConfigBenefitDurations from "../../views/config/ConfigBenefitDurationList.vue";
import ConfigBenefitDuration from "../../views/config/ConfigBenefitDuration.vue";
import ConfigRateGroupList from "../../views/config/ConfigRateGroupList.vue";
import ConfigRateGroup from "../../views/config/ConfigRateGroup.vue";

const routesProduct = [
  {
    path: "/config/products",
    name: "config-product-list",
    component: ConfigProductList,
  },
  {
    path: "/config/product",
    name: "config-product",
    component: ConfigProduct,
  },
  {
    path: "/config/product/:product_id/states",
    name: "config-product-states",
    component: ConfigProductStates,
    props: true,
  },
];

const routesProductVariation = [
  {
    path: "/config/product/:product_id/product-variations",
    name: "config-product-variation-list",
    component: ConfigProductVariationsList,
    props: true,
  },
  {
    path: "/config/product/:product_id/product-variation",
    name: "config-product-variation",
    component: ConfigProductVariations,
    props: true,
  },
  {
    path: "/config/product/:product_id/product-variation/:product_variation_id/age-bands-list",
    name: "config-age-bands-list",
    component: ConfigAgeBandsList,
    props: true,
  },
  {
    path: "/config/product/:product_id/product-variation/:product_variation_id/age-bands",
    name: "config-age-bands",
    component: ConfigAgeBands,
    props: true,
  },
];

const routesRateGroup = [
  {
    path: "/config/product/:product_id/rate-groups",
    name: "config-rate-group-list",
    component: ConfigRateGroupList,
    props: true,
  },
  {
    path: "/config/product/:product_id/rate-group",
    name: "config-rate-group",
    component: ConfigRateGroup,
    props: true,
  },
];

const routesBenefit = [
  {
    path: "/config/product/:product_id/benefits",
    name: "config-benefit-list",
    component: ConfigBenefitList,
    props: true,
  },
  {
    path: "/config/product/:product_id/benefit",
    name: "config-benefit",
    component: ConfigBenefit,
    props: true,
  },
  {
    path: "/config/product/:product_id/benefit/:benefit_id/states",
    name: "config-benefit-states",
    component: ConfigBenefitStates,
    props: true,
  },
  {
    path: "/config/product/:product_id/benefit/:benefit_id/product-variations",
    name: "config-benefit-product-variations",
    component: ConfigBenefitProductVariations,
    props: true,
  },
  {
    path: "/config/product/:product_id/benefit/:benefit_id/provisions",
    name: "config-benefit-provisions",
    component: ConfigBenefitProvisions,
    props: true,
  },
  {
    path: "/config/product/:product_id/benefit/:benefit_id/durations",
    name: "config-benefit-duration-list",
    component: ConfigBenefitDurations,
    props: true,
  },
  {
    path: "/config/product/:product_id/benefit/:benefit_id/duration",
    name: "config-benefit-duration",
    component: ConfigBenefitDuration,
    props: true,
  },
  {
    path: "/config/product/:product_id/coverages",
    name: "config-coverage-list",
    component: ConfigCoverageList,
    props: true,
  },
  {
    path: "/config/product/:product_id/coverage",
    name: "config-coverage",
    component: ConfigCoverage,
    props: true,
  },
];

const routesProvision = [
  {
    path: "/config/product/:product_id/provisions",
    name: "config-provision-list",
    component: ConfigProvisionList,
    props: true,
  },
  {
    path: "/config/product/:product_id/provision",
    name: "config-provision",
    component: ConfigProvision,
    props: true,
  },
  {
    path: "/config/product/:product_id/provision/:provision_id/ui",
    name: "config-provision-ui",
    component: ConfigProvisionUI,
    props: true,
  },
  {
    path: "/config/product/:product_id/provision/:provision_id/states",
    name: "config-provision-states",
    component: ConfigProvisionStates,
    props: true,
  },
  {
    path: "/config/product/:product_id/provision/:provision_id/factor",
    name: "config-provision-factors",
    component: ConfigFactors,
    props: true,
  },
  {
    path: "/config/product/:product_id/provision/:provision_id/factor-rules",
    name: "config-provision-factor-rules",
    component: ConfigFactorRules,
    props: true,
  },
];

export default [
  ...routesRateGroup,
  ...routesProduct,
  ...routesProductVariation,
  ...routesBenefit,
  ...routesProvision,
];
