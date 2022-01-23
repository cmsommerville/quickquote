export const storeSidebar = {
  state: () => ({
    isNavOpen: false,
  }),
  getters: {
    getIsNavOpen(state) {
      return state.isNavOpen;
    },
  },
  mutations: {
    toggleNav(state) {
      state.isNavOpen = !state.isNavOpen;
    },
  },
  actions: {},
};
