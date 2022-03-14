import Config_ProductVariationsList from "./Config_ProductVariationsList.vue";
import Config_ProductVariationLanding from "./Config_ProductVariationLanding.vue";
import Config_ProductVariation from "./Config_ProductVariation.vue";
import Config_ProductVariationAgeBandsList from "./Config_ProductVariationAgeBandsList.vue";
import Config_ProductVariationAgeBands from "./Config_ProductVariationAgeBands.vue";

export default [
  {
    path: "/config/product/:product_id/variations",
    name: "config-product-variations",
    component: Config_ProductVariationsList,
    props: true,
  },
  {
    path: "/config/product/:product_id/variations/:product_variation_id?",
    name: "config-product-variation-landing",
    component: Config_ProductVariationLanding,
    props: true,
  },
  {
    path: "/config/product/:product_id/variation/:product_variation_id?/basic-info",
    name: "config-product-variation",
    component: Config_ProductVariation,
    props: true,
  },
  {
    path: "/config/product/:product_id/variation/:product_variation_id/age-bands",
    name: "config-age-bands-list",
    component: Config_ProductVariationAgeBandsList,
    props: (route) => ({ ...route.params, ...route.query }),
  },
  {
    path: "/config/product/:product_id/variation/:product_variation_id/age-band",
    name: "config-age-band",
    component: Config_ProductVariationAgeBands,
    props: (route) => ({ ...route.params, ...route.query }),
  },
];
