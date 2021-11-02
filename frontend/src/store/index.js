import Vue from "vue";
import Vuex from "vuex";
import axios from "../services/axios";
import {
  SET_FACTOR_CONFIG,
  SET_BASE_CONFIG,
  SET_PROVISION_CONFIG,
  // SET_PROVISION_STATES,
} from "./mutation-types";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    baseProductConfig: {},
    config_provisions: [],
    new_provision: {
      name: null,
      label: null,
      states: null,
      ui: {},
      factor: {},
    },
    factorConfig: {},
  },
  getters: {
    isConfigEmpty(state) {
      return Object.keys(state.baseProductConfig).length === 0;
    },
    getBaseProductConfig(state) {
      return state.baseProductConfig;
    },
    getProvisionConfigList(state) {
      return state.config_provisions;
    },
    getProvisionConfig(state) {
      return state.new_provision;
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
    SET_NEW_PROVISION_CONFIG(state, provision) {
      state.new_provision = { ...provision };
    },
    SET_NEW_PROVISION_STATES(state, state_applicability) {
      state.new_provision = {
        ...state.new_provision,
        states: state_applicability,
      };
    },
    RESET_NEW_PROVISION(state) {
      state.new_provision = {
        name: null,
        label: null,
        states: null,
        ui: {},
        factor: {},
      };
    },
    COMMIT_NEW_PROVISION(state) {
      state.config_provisions = [
        ...state.config_provisions.filter(
          (item) => item.name !== state.new_provision.name
        ),
        { ...state.new_provision },
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
    addNewProvisionToList({ commit }) {
      commit("COMMIT_NEW_PROVISION");
      commit("RESET_NEW_PROVISION");
    },
    setFactorConfig({ commit }, factorConfig) {
      commit(SET_FACTOR_CONFIG, factorConfig);
    },
  },
  modules: {},
});
