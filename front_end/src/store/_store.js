import { createStore } from "vuex";
import { storeSidebar } from "./sidebar";

export const store = createStore({
  state() {
    return {
      count: 1,
    };
  },
  modules: {
    sidebar: storeSidebar,
  },
});
