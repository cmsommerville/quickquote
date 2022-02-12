import Config_BenefitList from "./Config_BenefitList.vue";
import Config_Benefit from "./Config_Benefit.vue";
import Config_BenefitStatesList from "./Config_BenefitStatesList.vue";

export default [
  {
    path: "/config/product/:product_id/benefits",
    name: "config-benefits",
    component: Config_BenefitList,
    props: true,
  },
  {
    path: "/config/product/:product_id/benefit",
    name: "config-benefit",
    component: Config_Benefit,
    props: (route) => ({ ...route.params, ...route.query }),
  },
  {
    path: "/config/product/:product_id/benefit/:benefit_id/states",
    name: "config-benefit-states",
    component: Config_BenefitStatesList,
    props: (route) => ({ ...route.params, ...route.query }),
  },
  // {
  //   path: "/config/product/:product_id/benefit/states",
  //   name: "config-benefit-states",
  //   component: Config_BenefitStates,
  //   props: (route) => ({ ...route.params, ...route.query }),
  //   beforeEnter(to, from, next) {
  //     if (from.name === "config-benefit" || to.query.benefit_id) next();
  //     else
  //       next({
  //         name: "config-benefits",
  //         params: { product_id: to.params.product_id },
  //       });
  //   },
  // },
];
