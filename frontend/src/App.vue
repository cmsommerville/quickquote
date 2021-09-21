<template>
  <v-app>
    <the-header />
    <the-sidebar />
    <v-main>
      <router-view />
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
};
</script>

<style lang="scss">
@import "../node_modules/ag-grid-community/dist/styles/ag-grid.css";
@import "../node_modules/ag-grid-community/dist/styles/ag-theme-alpine.css";
@import "../node_modules/ag-grid-community/dist/styles/ag-theme-material.css";

.container {
  display: flex;
}
</style>
