export const storeConfigUI = {
  state: () => ({
    ref_states: [],
    selected_states: [],
  }),
  getters: {
    get_ref_states(state) {
      return state.ref_states;
    },
    get_selected_states(state) {
      return state.selected_states;
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
      if (state.selected_states.includes(val)) {
        state.selected_states = [
          ...state.selected_states.filter((st) => st !== val),
        ];
      } else {
        state.selected_states = [...state.selected_states, val];
      }
    },
    toggle_all_states(state) {
      if (state.selected_states.length > 0) {
        state.selected_states = [];
      } else {
        state.selected_states = state.ref_states.map((s) => s.state_code);
      }
    },
  },
  actions: {},
};
