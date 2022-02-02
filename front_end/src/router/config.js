import Config_ProductList from "@/views/config/Config_Product/Config_ProductList.vue";
import Config_Product from "@/views/config/Config_Product/Config_Product.vue";
import Config_ProductStates from "@/views/config/Config_Product/Config_ProductStates.vue";
import Config_ProductVariations from "@/views/config/Config_ProductVariations/Config_ProductVariations.vue";
import AgeBandsLanding from "@/views/config/Config_AgeBands/AgeBandsLanding.vue";
import AgeBandsConfig from "@/views/config/Config_AgeBands/AgeBandsConfig.vue";
import AgeBandsStates from "@/views/config/Config_AgeBands/AgeBandsStates.vue";

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
    component: AgeBandsLanding,
    props: true,
  },
  {
    path: "/config/product/:product_id/age-band",
    name: "config-age-band",
    component: AgeBandsConfig,
    props: (route) => ({ ...route.params, ...route.query }),
    beforeEnter(to, from, next) {
      if (["config-age-bands", "config-age-band-states"].includes(from.name))
        next();
      else next({ name: "config-age-bands", params: { ...to.params } });
    },
  },
  {
    path: "/config/product/:product_id/age-band-states",
    name: "config-age-band-states",
    component: AgeBandsStates,
    props: (route) => ({ ...route.params, ...route.query }),
    beforeEnter(to, from, next) {
      if (from.name === "config-age-band") next();
      else next({ name: "config-age-bands", params: { ...to.params } });
    },
  },
];
