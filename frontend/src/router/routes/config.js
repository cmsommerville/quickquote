import ConfigProductList from "../../views/config/ConfigProductList";
import ConfigProduct from "../../views/config/ConfigProduct";
import ConfigProvision from "../../views/config/ConfigProvision.vue";
import ConfigProvisionList from "../../views/config/ConfigProvisionList.vue";
import ConfigProvisionStates from "../../views/config/ConfigProvisionStates.vue";
import ConfigProvisionFactors from "../../views/config/ConfigProvisionFactors.vue";
import ConfigBenefitList from "../../views/config/ConfigBenefitList.vue";
import ConfigBenefit from "../../views/config/ConfigBenefit.vue";
import ConfigBenefitStates from "../../views/config/ConfigBenefitStates.vue";

export default [
  {
    path: "/config/products",
    name: "config-product-list",
    component: ConfigProductList,
  },
  {
    path: "/config/product/:productId",
    name: "config-product",
    component: ConfigProduct,
  },
  {
    path: "/config/product/:productId/provisions",
    name: "config-provision-list",
    component: ConfigProvisionList,
    props: true,
  },
  {
    path: "/config/product/:productId/provision",
    name: "config-provision",
    component: ConfigProvision,
    props: true,
  },
  {
    path: "/config/product/:productId/provision/states",
    name: "config-provision-states",
    component: ConfigProvisionStates,
    props: true,
  },
  {
    path: "/config/product/:productId/provision/factors",
    name: "config-provision-factors",
    component: ConfigProvisionFactors,
    props: true,
  },

  {
    path: "/config/product/:productId/benefits",
    name: "config-benefit-list",
    component: ConfigBenefitList,
    props: true,
  },
  {
    path: "/config/product/:productId/benefit",
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
];
