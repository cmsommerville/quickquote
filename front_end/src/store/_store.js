import { createStore } from "vuex";
import { storeSidebar } from "./sidebar";
import { storeConfigUI } from "./config-ui";

export const store = createStore({
  state() {
    return {};
  },
  modules: {
    sidebar: storeSidebar,
    config_ui: storeConfigUI,
  },
});
