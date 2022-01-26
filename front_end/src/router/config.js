import Config_ProductList from "@/views/config/Config_Product/Config_ProductList.vue";
import Config_Product from "@/views/config/Config_Product/Config_Product.vue";
import Config_ProductStates from "@/views/config/Config_Product/Config_ProductStates.vue";

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
];
