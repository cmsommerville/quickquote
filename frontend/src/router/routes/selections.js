import RaterEntry from "../../views/RaterEntry.vue";
import Group from "../../views/Group.vue";
import Plan from "../../views/Plan.vue";
import Provisions from "../../views/Provisions.vue";
import Benefits from "../../views/Benefits.vue";
import AgeBands from "../../views/AgeBands.vue";
import Premium from "../../views/Premium.vue";

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
