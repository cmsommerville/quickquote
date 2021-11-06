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
    path: "/plan",
    name: "plan",
    component: Plan,
  },
  {
    path: "/provisions",
    name: "provisions",
    component: Provisions,
  },
  {
    path: "/benefits",
    name: "benefits",
    component: Benefits,
  },
  {
    path: "/premium",
    name: "premium",
    component: Premium,
  },
  {
    path: "/age-bands",
    name: "age-bands",
    component: AgeBands,
  },
];
