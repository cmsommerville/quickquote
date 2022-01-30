export const storeConfig = {
  state: () => ({
    product_variation: {},
  }),
  getters: {
    get_product_variation(state) {
      return state.product_variation;
    },
  },
  mutations: {
    set_product_variation(state, payload) {
      state.product_variation = { ...payload };
    },
  },
  actions: {},
};
