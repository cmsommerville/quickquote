import ConfigApplicabilitiesLanding from "./Config_ApplicabilitiesLanding.vue";
import ConfigBenefitProvision from "./Config_BenefitProvision.vue";
import ConfigBenefitProductVariation from "./Config_BenefitProductVariation.vue";

export default [
  {
    path: "/config/product/:product_id/applicabilities",
    name: "config-applicabilities",
    component: ConfigApplicabilitiesLanding,
    props: (route) => ({ ...route.params, ...route.query }),
  },
  {
    path: "/config/product/:product_id/benefit-provision",
    name: "config-benefit-provision",
    component: ConfigBenefitProvision,
    props: (route) => ({ ...route.params, ...route.query }),
  },
  {
    path: "/config/product/:product_id/benefit-variation",
    name: "config-benefit-variation",
    component: ConfigBenefitProductVariation,
    props: (route) => ({ ...route.params, ...route.query }),
  },
];
