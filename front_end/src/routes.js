import Home from "./views/Home.vue";
import About from "./views/About.vue";
import NotFound from "./views/NotFound.vue";

import selectionRoutes from "./router/selections";
import configRoutes from "./router/config";

/** @type {import('vue-router').RouterOptions['routes']} */
export const routes = [
  { path: "/", component: Home, name: "home", meta: { title: "Home" } },
  {
    path: "/about",
    meta: { title: "About" },
    component: About,
  },
  ...configRoutes,
  ...selectionRoutes,
  { path: "/:path(.*)", component: NotFound },
];
