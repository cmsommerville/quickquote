<template>
  <div>
    <v-app-bar color="primary" dark>
      <v-app-bar-nav-icon
        @click.stop="$emit('click-hamburger')"
      ></v-app-bar-nav-icon>

      <v-toolbar-title>
        <router-link to="/">
          <the-logo dark />
        </router-link>
      </v-toolbar-title>

      <v-spacer></v-spacer>
      <plan-search-bar class="mt-6" @search:selected="searchHandler" />

      <v-spacer></v-spacer>
      <div>
        <v-btn plain :to="{ name: 'rater' }"> New Quote </v-btn>
      </div>
    </v-app-bar>
  </div>
</template>

<script>
// import axios from "../services/axios.js";
import TheLogo from "./TheLogo";
import PlanSearchBar from "./PlanSearchBar.vue";

export default {
  name: "TheHeader",
  components: { TheLogo, PlanSearchBar },
  data() {
    return {};
  },
  methods: {
    searchHandler(model) {
      // handle input event for search bar
      this.$router.push({
        name: "plan",
        query: {
          plan_id: model.plan_id,
          plan_config_id: model.plan_config_id,
        },
      });
    },
  },
};
</script>

<style scoped>
.header {
  width: 100%;
}
</style>
