<template>
  <v-app>
    <the-header @click-hamburger="drawer = !drawer" />
    <the-sidebar :drawer="drawer" @toggle="toggleDrawer" />
    <v-main class="app-container">
      <router-view :key="$route.fullPath" class="app-content" />
    </v-main>
  </v-app>
</template>

<script>
import TheSidebar from "./components/TheSidebar.vue";
import TheHeader from "./components/TheHeader.vue";

export default {
  name: "App",
  components: {
    TheSidebar,
    TheHeader,
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
}

.app-content {
  min-width: 60%;
  max-width: 90%;
  border: 1px solid #ddd;
  padding: 2rem;
  margin: 1rem auto;
}
</style>
