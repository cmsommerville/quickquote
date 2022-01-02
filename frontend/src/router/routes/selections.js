import RaterEntry from "../../views/selections/RaterEntry.vue";
import Group from "../../views/selections/Group.vue";
import Plan from "../../views/selections/Plan.vue";
import Provisions from "../../views/selections/Provisions.vue";
import Benefits from "../../views/selections/Benefits.vue";
import AgeBands from "../../views/selections/AgeBands.vue";
import Premium from "../../views/selections/Premium.vue";

export default [
  {
    path: "/rater",
    name: "rater",
    component: RaterEntry,
  },
  {
    path: "/group",
    name: "group",
    component: Group,
  },
  {
    path: "/selections/plan",
    name: "selections-plan",
    component: Plan,
  },
  {
    path: "/selections/provisions",
    name: "selections-provisions",
    component: Provisions,
  },
  {
    path: "/selections/benefits/:plan_id",
    name: "selections-benefits",
    component: Benefits,
    props: true,
  },
  {
    path: "/selections/premium",
    name: "selections-premium",
    component: Premium,
  },
  {
    path: "/selections/age-bands",
    name: "selections-age-bands",
    component: AgeBands,
  },
];
