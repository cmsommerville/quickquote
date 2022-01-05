export default {
  state: () => ({
    snackbar: false,
    snackbar_message: "",
  }),
  mutations: {
    SHOW_SNACKBAR(state, message) {
      state.snackbar = true;
      state.snackbar_message = message;
    },
    INITIALIZE_SNACKBAR(state) {
      state.snackbar = false;
      state.snackbar_message = "";
    },
  },
  actions: {},
  getters: {
    get_snackbar_message(state) {
      return state.snackbar_message;
    },
    get_snackbar(state) {
      return state.snackbar;
    },
  },
};
