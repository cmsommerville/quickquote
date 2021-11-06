import axios from "../../services/axios";

export const config = {
  state: () => ({
    config: {},
    provisions: [],
    benefits: [],
    new_provision: {},
    new_benefit: {},
  }),
  mutations: {
    SET_CONFIG(state, payload) {
      state.config = { ...payload };
    },
    RESET_CONFIG(state) {
      state.config = {};
    },

    APPEND_ALL_PROVISIONS(state) {
      state.config = {
        ...state.config,
        provisions: [...state.provisions],
      };
    },
    SET_PROVISIONS(state, payload) {
      state.provisions = [...payload];
    },
    RESET_PROVISIONS(state) {
      state.provisions = [];
    },

    SET_NEW_PROVISION(state, payload) {
      state.new_provision = { ...payload };
    },
    APPEND_NEW_PROVISION(state) {
      state.provisions = [
        ...state.provisions.filter(
          (item) => item.name !== state.new_provision.name
        ),
        { ...state.new_provision },
      ];
    },
    RESET_NEW_PROVISION(state) {
      state.new_provision = {};
    },

    SET_PROVISION_STATES(state, state_applicability) {
      state.new_provision = {
        ...state.new_provision,
        states: state_applicability,
      };
    },
    SET_PROVISION_FACTORS(state, payload) {
      state.new_provision = {
        ...state.new_provision,
        factor: { ...payload },
      };
    },

    SET_BENEFITS(state, payload) {
      state.benefits = [...payload];
    },
    RESET_BENEFITS(state) {
      state.benefits = [];
    },

    SET_NEW_BENEFIT(state, payload) {
      state.new_benefit = { ...payload };
    },
    APPEND_NEW_BENEFIT(state) {
      state.benefits = [
        ...state.benefits.filter(
          (item) => item.name !== state.new_benefit.name
        ),
        { ...state.new_benefit },
      ];
    },
    RESET_NEW_BENEFIT(state) {
      state.new_benefit = {};
    },
  },
  actions: {
    async initializeConfig({ commit }, productId) {
      const res = await axios.get(`/config/plan/${productId}`);
      commit("RESET_CONFIG");
      commit("SET_CONFIG", { ...res.data[0] });
      commit("SET_PROVISIONS", [...res.data[0].provisions]);
      commit("SET_BENEFITS", [...res.data[0].benefits]);
    },
    addNewProvisionToList({ commit }) {
      commit("APPEND_NEW_PROVISION");
      commit("RESET_NEW_PROVISION");
    },
  },
  getters: {
    isConfigEmpty(state) {
      return Object.keys(state.config).length === 0;
    },
    getConfig(state) {
      return state.config;
    },
    getProvisionConfigList(state) {
      return state.provisions;
    },
    getProvisionConfig(state) {
      return state.new_provision;
    },
    getBenefitConfigList(state) {
      return state.benefits;
    },
  },
};
