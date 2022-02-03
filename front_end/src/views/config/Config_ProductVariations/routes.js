import Config_ProductVariations from "./Config_ProductVariations.vue";

export default [
  {
    path: "/config/product/:product_id/variations",
    name: "config-product-variations",
    component: Config_ProductVariations,
    props: true,
  },
];
