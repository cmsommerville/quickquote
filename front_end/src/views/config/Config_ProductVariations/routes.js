import Config_ProductVariationsList from "./Config_ProductVariationsList.vue";
import Config_ProductVariation from "./Config_ProductVariation.vue";

export default [
  {
    path: "/config/product/:product_id/variations",
    name: "config-product-variations",
    component: Config_ProductVariationsList,
    props: true,
  },
  {
    path: "/config/product/:product_id/variation/:product_variation_id?",
    name: "config-product-variation",
    component: Config_ProductVariation,
    props: true,
  },
];
