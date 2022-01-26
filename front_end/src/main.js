import { createApp } from "vue";
import { store } from "./store/_store.js";
import "./tailwind.css";
import App from "./App.vue";
import { routes } from "./routes.js";
import { createRouter, createWebHistory } from "vue-router";
import UIComponents from "@/plugins/ui-components.js";
import icons from "@/plugins/icons.js";

const app = createApp(App);

// router
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// global UI components
app.use(UIComponents);
app.use(icons);

app.use(router);
app.use(store);
app.mount("#app");
