export const storeConfigUI = {
  state: () => ({
    ref_states: [],
    selected_states: [],
    snackbar_message: null,
  }),
  getters: {
    get_ref_states(state) {
      return state.ref_states;
    },
    get_selected_states(state) {
      return state.selected_states;
    },
    get_snackbar_message(state) {
      return state.snackbar_message;
    },
  },
  mutations: {
    initialize_ref_states(state, val) {
      state.ref_states = [...val];
    },
    initialize_selected_states(state) {
      state.selected_states = [];
    },
    toggle_selected_state(state, val) {
      if (
        state.selected_states.findIndex(
          (st) => st.state_code === val.state_code
        ) >= 0
      ) {
        state.selected_states = [
          ...state.selected_states.filter(
            (st) => st.state_code !== val.state_code
          ),
        ];
      } else {
        state.selected_states = [...state.selected_states, val];
      }
    },
    toggle_all_states(state) {
      if (state.selected_states.length > 0) {
        state.selected_states = [];
      } else {
        state.selected_states = [...state.ref_states];
      }
    },
    set_snackbar_message(state, msg) {
      state.snackbar_message = msg;
    },
  },
  actions: {
    SET_SNACKBAR_MESSAGE({ commit }, msg) {
      commit("set_snackbar_message", msg);
      setTimeout(() => {
        commit("set_snackbar_message", null);
      }, 5000);
    },
  },
};
