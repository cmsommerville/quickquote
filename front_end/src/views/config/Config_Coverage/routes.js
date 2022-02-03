import Config_CoveragesList from "./Config_CoveragesList.vue";
import Config_Coverage from "./Config_Coverage.vue";

export default [
  {
    path: "/config/product/:product_id/coverages",
    name: "config-coverages",
    component: Config_CoveragesList,
    props: true,
  },
  {
    path: "/config/product/:product_id/coverage",
    name: "config-coverage",
    component: Config_Coverage,
    props: (route) => ({ ...route.params, ...route.query }),
  },
];
