import Vue from "vue";
import Vuex from "vuex";
import module_ui from "./modules/ui";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: { module_ui },
});
