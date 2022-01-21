// import RaterEntry from "../../views/selections/RaterEntry.vue";
// import Group from "../../views/selections/Group.vue";
import SelectionPlan from "../views/selections/Selection_Plan.vue";
import SelectionPlanConfig from "../views/selections/Selection_PlanConfig.vue";
// import Provisions from "../../views/selections/Provisions.vue";
import Selection_Benefits from "../views/selections/Selection_Benefits.vue";
// import AgeBands from "../../views/selections/AgeBands.vue";
// import Premium from "../../views/selections/Premium.vue";

export default [
  //   {
  //     path: "/rater",
  //     name: "rater",
  //     component: RaterEntry,
  //   },
  //   {
  //     path: "/group",
  //     name: "group",
  //     component: Group,
  //   },
  {
    path: "/selections/plan",
    name: "selections-plan",
    component: SelectionPlan,
    props: true,
  },
  {
    path: "/selections/plan/config",
    name: "selections-plan-config",
    component: SelectionPlanConfig,
    props: (route) => ({ product_id: route.query.product_id }),
  },
  //   {
  //     path: "/selections/provisions/:plan_id",
  //     name: "selections-provisions",
  //     component: Provisions,
  //     props: true,
  //   },
  {
    path: "/selections/plan/:plan_id/benefits",
    name: "selections-benefits",
    component: Selection_Benefits,
    props: true,
  },
  //   {
  //     path: "/selections/premium/:plan_id",
  //     name: "rating-premium",
  //     component: Premium,
  //     props: true,
  //   },
  //   {
  //     path: "/selections/age-bands/:plan_id",
  //     name: "selections-age-bands",
  //     component: AgeBands,
  //     props: true,
  //   },
];
