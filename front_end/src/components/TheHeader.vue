<template>
  <nav class="bg-white w-screen h-12 flex items-center px-1 justify-between">
    <div class="flex items-center">
      <menu-icon class="h-8 w-8 cursor-pointer" />
      <the-logo class="mx-4" />
    </div>
    <app-input
      class="bg-transparent w-96 opacity-50"
      label="Search"
      placeholder="Input Plan Number"
      v-model="inputValue"
    >
      <search-icon class="h-6 w-6 inline-block opacity-50" />
    </app-input>
    <app-button
      class="bg-theme-primary text-white text-sm flex items-center px-6 py-1"
      @click="routeTo('selections-plan')"
    >
      <plus-icon class="inline-block h-4 w-4" />
      <span class="ml-1">New Quote</span>
    </app-button>
  </nav>
</template>

<script>
import { MenuIcon, PlusIcon, SearchIcon } from "@heroicons/vue/outline";
import TheLogo from "./TheLogo.vue";
import AppInput from "./AppInput.vue";

export default {
  name: "TheHeader",
  components: { MenuIcon, PlusIcon, SearchIcon, TheLogo, AppInput },
  data() {
    return {
      inputValue: null,
    };
  },
  methods: {
    routeTo(route_name, params = {}) {
      this.$router.push({ name: route_name, params: { ...params } });
    },
  },
};
</script>

<style></style>
