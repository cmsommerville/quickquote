export const storeConfig = {
  state: () => ({
    selections_obj: null,
    selections_array: null,
  }),
  getters: {
    get_selections_object(state) {
      return state.selections_obj;
    },
    get_selections_array(state) {
      return state.selections_array;
    },
  },
  mutations: {
    SET_SELECTIONS_OBJECT(state, payload) {
      state.selections_obj = { ...payload };
    },
    SET_SELECTIONS_ARRAY(state, payload) {
      state.selections_array = [...payload];
    },
  },
  actions: {},
};
