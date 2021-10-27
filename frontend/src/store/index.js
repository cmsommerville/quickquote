import Vue from "vue";
import Vuex from "vuex";
import axios from "../services/axios";
import {
  SET_FACTOR_CONFIG,
  SET_BASE_CONFIG,
  SET_PROVISION_CONFIG,
} from "./mutation-types";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    baseProductConfig: {},
    config_provisions: [],
    factorConfig: {},
  },
  getters: {
    isConfigEmpty(state) {
      return Object.keys(state.baseProductConfig).length === 0;
    },
    getBaseProductConfig(state) {
      return state.baseProductConfig;
    },
    getProvisionConfig(state) {
      return state.config_provisions;
    },
  },
  mutations: {
    [SET_BASE_CONFIG](state, payload) {
      state.baseProductConfig = { ...payload };
    },
    [SET_PROVISION_CONFIG](state, payload) {
      const payload_names = payload.map((item) => item.name);

      state.config_provisions = [
        ...state.config_provisions.filter(
          (item) => !payload_names.includes(item.name)
        ),
        ...payload,
      ];
    },
    [SET_FACTOR_CONFIG](state, payload) {
      state.config_provisions = [
        ...state.config_provisions.filter(
          (item) => item.name !== payload.factor_code
        ),
        {
          ...state.config_provisions.find(
            (item) => item.name === payload.factor_code
          ),
          factor: {
            default_factor_value: payload.default_factor_value,
            variability: payload.variability,
          },
        },
      ];
    },
  },
  actions: {
    async initializeBaseProductConfig({ commit }, productUUID) {
      const res = await axios.get(`/config/plan/${productUUID}`);
      commit(SET_BASE_CONFIG, { ...res.data[0] });
      commit(SET_PROVISION_CONFIG, [...res.data[0].provisions]);
    },
    setFactorConfig({ commit }, factorConfig) {
      commit(SET_FACTOR_CONFIG, factorConfig);
    },
  },
  modules: {},
});
