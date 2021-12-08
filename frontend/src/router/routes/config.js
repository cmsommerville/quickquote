import ConfigProductList from "../../views/config/ConfigProductList";
import ConfigProduct from "../../views/config/ConfigProduct";
import ConfigProductStates from "../../views/config/ConfigProductStates.vue";
import ConfigProductVariations from "../../views/config/ConfigProductVariations.vue";
import ConfigProductVariationsList from "../../views/config/ConfigProductVariationsList.vue";
import ConfigCoverageList from "../../views/config/ConfigCoverageList.vue";
import ConfigProvision from "../../views/config/ConfigProvision.vue";
import ConfigProvisionList from "../../views/config/ConfigProvisionList.vue";
import ConfigProvisionStates from "../../views/config/ConfigProvisionStates.vue";
import ConfigProvisionFactors from "../../views/config/ConfigProvisionFactors.vue";
import ConfigBenefitList from "../../views/config/ConfigBenefitList.vue";
import ConfigBenefit from "../../views/config/ConfigBenefit.vue";
import ConfigBenefitStates from "../../views/config/ConfigBenefitStates.vue";
import ConfigBenefitAmounts from "../../views/config/ConfigBenefitAmounts.vue";
import ConfigBenefitFactors from "../../views/config/ConfigBenefitFactors.vue";
import ConfigBenefitDurations from "../../views/config/ConfigBenefitDurations.vue";

export default [
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
    path: "/config/product-variations",
    name: "config-product-variation-list",
    component: ConfigProductVariationsList,
  },
  {
    path: "/config/product-variation",
    name: "config-product-variation",
    component: ConfigProductVariations,
  },
  {
    path: "/config/coverages",
    name: "config-coverage-list",
    component: ConfigCoverageList,
  },
  {
    path: "/config/product/provisions",
    name: "config-provision-list",
    component: ConfigProvisionList,
    props: true,
  },
  {
    path: "/config/product/states",
    name: "config-product-states",
    component: ConfigProductStates,
    props: true,
  },
  {
    path: "/config/product/provision",
    name: "config-provision",
    component: ConfigProvision,
    props: true,
  },
  {
    path: "/config/product/provision/states",
    name: "config-provision-states",
    component: ConfigProvisionStates,
    props: true,
  },
  {
    path: "/config/product/provision/factors",
    name: "config-provision-factors",
    component: ConfigProvisionFactors,
    props: true,
  },

  {
    path: "/config/product/benefits",
    name: "config-benefit-list",
    component: ConfigBenefitList,
    props: true,
  },
  {
    path: "/config/product/benefit",
    name: "config-benefit",
    component: ConfigBenefit,
    props: true,
  },
  {
    path: "/config/product/:productId/benefit/states",
    name: "config-benefit-states",
    component: ConfigBenefitStates,
    props: true,
  },
  {
    path: "/config/product/:productId/benefit/amounts",
    name: "config-benefit-amounts",
    component: ConfigBenefitAmounts,
    props: true,
  },
  {
    path: "/config/product/:productId/benefit/factors",
    name: "config-benefit-factors",
    component: ConfigBenefitFactors,
    props: true,
  },
  {
    path: "/config/product/:productId/benefit/durations",
    name: "config-benefit-durations",
    component: ConfigBenefitDurations,
    props: true,
  },
];
