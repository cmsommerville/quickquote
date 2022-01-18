<template>
  <v-app>
    <the-header @click-hamburger="drawer = !drawer" />
    <the-sidebar :drawer="drawer" @toggle="toggleDrawer" />
    <v-main class="app-container bg-gradient-to-br from-red-500 to-red-400">
      <router-view
        :key="$route.fullPath"
        class="app-content flex justify-center"
      />
      <the-snackbar
        :snackbar="$store.getters.get_snackbar"
        :snackbar_message="$store.getters.get_snackbar_message"
      />
    </v-main>
  </v-app>
</template>

<script>
import TheSidebar from "./components/TheSidebar.vue";
import TheHeader from "./components/TheHeader.vue";
import TheSnackbar from "./components/TheSnackbar.vue";

export default {
  name: "App",
  components: {
    TheSidebar,
    TheHeader,
    TheSnackbar,
  },
  data() {
    return {
      drawer: false,
    };
  },
  methods: {
    toggleDrawer(payload) {
      this.drawer = payload;
    },
  },
};
</script>

<style lang="scss">
@import "../node_modules/ag-grid-community/dist/styles/ag-grid.css";
@import "../node_modules/ag-grid-community/dist/styles/ag-theme-alpine.css";
@import "../node_modules/ag-grid-community/dist/styles/ag-theme-material.css";

.app-container {
  display: flex;
  background-image: linear-gradient(
    to bottom right,
    hsl(352, 80%, 60%),
    hsl(5, 80%, 60%)
  );
}

// .app-content {
//   min-width: 60%;
//   max-width: 90%;
//   border: 1px solid #ddd;
//   padding: 2rem;
//   margin: 1rem auto;
// }
</style>
