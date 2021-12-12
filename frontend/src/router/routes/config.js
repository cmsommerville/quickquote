import ConfigProductList from "../../views/config/ConfigProductList";
import ConfigProduct from "../../views/config/ConfigProduct";
import ConfigProductStates from "../../views/config/ConfigProductStates.vue";
import ConfigProductVariations from "../../views/config/ConfigProductVariations.vue";
import ConfigProductVariationsList from "../../views/config/ConfigProductVariationsList.vue";
import ConfigCoverageList from "../../views/config/ConfigCoverageList.vue";
import ConfigCoverage from "../../views/config/ConfigCoverage.vue";
import ConfigProvision from "../../views/config/ConfigProvision.vue";
import ConfigProvisionList from "../../views/config/ConfigProvisionList.vue";
import ConfigProvisionStates from "../../views/config/ConfigProvisionStates.vue";
import ConfigProvisionFactors from "../../views/config/ConfigProvisionFactors.vue";
import ConfigBenefitList from "../../views/config/ConfigBenefitList.vue";
import ConfigBenefit from "../../views/config/ConfigBenefit.vue";
import ConfigBenefitDurations from "../../views/config/ConfigBenefitDurationList.vue";
import ConfigBenefitDuration from "../../views/config/ConfigBenefitDuration.vue";
import ConfigRateGroupList from "../../views/config/ConfigRateGroupList.vue";

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
];

const routesRateGroup = [
  {
    path: "/config/product/:product_id/rate-groups",
    name: "config-rate-group-list",
    component: ConfigRateGroupList,
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
    alias: "/config/product/:product_id/benefit/:benefit_id",
    props: true,
  },
  {
    path: "/config/product/:product_id/benefit/durations",
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
    path: "/config/product/:product_id/provision/:provision_id/states",
    name: "config-provision-states",
    component: ConfigProvisionStates,
    props: true,
  },
  {
    path: "/config/product/:product_id/provision/:provision_id/factors",
    name: "config-provision-factors",
    component: ConfigProvisionFactors,
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
