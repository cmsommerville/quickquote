import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import RaterEntry from "../views/RaterEntry.vue";
import Group from "../views/Group.vue";
import Plan from "../views/Plan.vue";
import Provisions from "../views/Provisions.vue";
import Benefits from "../views/Benefits.vue";
import AgeBands from "../views/AgeBands.vue";
import Premium from "../views/Premium.vue";
import CreateTables from "../views/admin/CreateTables.vue";
import Session from "../views/Session.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
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
  {
    path: "/admin/create-tables",
    name: "create-tables",
    component: CreateTables,
  },
  {
    path: "/session",
    name: "session",
    component: Session,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
