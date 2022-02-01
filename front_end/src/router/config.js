import Config_ProductList from "@/views/config/Config_Product/Config_ProductList.vue";
import Config_Product from "@/views/config/Config_Product/Config_Product.vue";
import Config_ProductStates from "@/views/config/Config_Product/Config_ProductStates.vue";
import Config_ProductVariations from "@/views/config/Config_ProductVariations/Config_ProductVariations.vue";
import Config_AgeBands from "@/views/config/Config_AgeBands/Config_AgeBands.vue";

export default [
  {
    path: "/config/products",
    name: "config-product-list",
    component: Config_ProductList,
    props: true,
  },
  {
    path: "/config/product/:product_id?",
    name: "config-product",
    component: Config_Product,
    props: true,
  },
  {
    path: "/config/product/:product_id/states",
    name: "config-product-states",
    component: Config_ProductStates,
    props: true,
  },
  {
    path: "/config/product/:product_id/variations",
    name: "config-product-variations",
    component: Config_ProductVariations,
    props: true,
  },
  {
    path: "/config/product/:product_id/age-bands",
    name: "config-age-bands",
    component: Config_AgeBands,
    props: true,
  },
];
