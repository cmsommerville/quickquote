import AgeBandsLanding from "./AgeBandsLanding.vue";
import AgeBandsConfig from "./AgeBandsConfig.vue";
import AgeBandsStates from "./AgeBandsStates.vue";

export default [
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
    // beforeEnter(to, from, next) {
    //   if (["config-age-bands", "config-age-band-states"].includes(from.name))
    //     next();
    //   else next({ name: "config-age-bands", params: { ...to.params } });
    // },
  },
  {
    path: "/config/product/:product_id/age-band-states",
    name: "config-age-band-states",
    component: AgeBandsStates,
    props: (route) => ({ ...route.params, ...route.query }),
    // beforeEnter(to, from, next) {
    //   if (from.name === "config-age-band") next();
    //   else next({ name: "config-age-bands", params: { ...to.params } });
    // },
  },
];
