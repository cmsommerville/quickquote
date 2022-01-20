import { createApp } from "vue";
import "./tailwind.css";
import App from "./App.vue";
import { routes } from "./routes.js";
import { createRouter, createWebHistory } from "vue-router";

import AppInput from "./components/AppInput.vue";
import AppSelect from "./components/AppSelect.vue";
import AppCheckbox from "./components/AppCheckbox.vue";
import AppButton from "./components/AppButton.vue";

const app = createApp(App);

// router
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// global components
app.component("app-input", AppInput);
app.component("app-select", AppSelect);
app.component("app-checkbox", AppCheckbox);
app.component("app-button", AppButton);

app.use(router);
app.mount("#app");
