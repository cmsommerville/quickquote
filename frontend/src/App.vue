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
  data: () => ({
    //
  }),
};
</script>

<style scoped>
.container {
  display: flex;
}
</style>
