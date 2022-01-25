import Config_ProductList from "@/views/config/Config_Product/Config_ProductList.vue";
import Config_Product from "@/views/config/Config_Product/Config_Product.vue";

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
];
