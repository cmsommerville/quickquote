import { createStore } from "vuex";
import { storeSidebar } from "./sidebar";
import { storeConfigUI } from "./config-ui";
import { storeConfig } from "./config";

export const store = createStore({
  state() {
    return {};
  },
  modules: {
    sidebar: storeSidebar,
    config_ui: storeConfigUI,
    config: storeConfig,
  },
});
