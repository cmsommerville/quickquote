<template>
  <div>
    <header
      class="bg-white w-screen h-12 flex items-center px-1 justify-between"
    >
      <div class="flex items-center">
        <hamburger-button />
        <router-link :to="{ name: 'home' }"
          ><the-logo class="mx-4"
        /></router-link>
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
        :transparent="true"
        class="text-sm flex items-center px-6 py-1 mx-4"
        @click="routeTo('selections-plan')"
      >
        <plus-icon class="inline-block h-4 w-4" />
        <span class="ml-1">New Quote</span>
      </app-button>
    </header>
    <the-sidebar
      class="flex flex-col items-center py-2"
      @click="$store.commit('toggleNav')"
    >
      <router-link :to="{ name: 'home' }"><the-logo /></router-link>
      <ul class="mt-6 w-full">
        <li
          v-for="route in navLinks"
          :key="route.route_name"
          class="text-gray-500 py-3 flex items-center justify-center"
        >
          <router-link
            :to="{ name: route.route_name }"
            class="flex items-center"
          >
            <span class="inline-block mr-2">{{ route.label }}</span>
            <component :is="route.icon" class="inline-block w-6 h-6" />
          </router-link>
        </li>
      </ul>
    </the-sidebar>
  </div>
</template>

<script>
import { PlusIcon, SearchIcon } from "@heroicons/vue/outline";
import TheLogo from "./TheLogo.vue";
import TheSidebar from "./TheSidebar/TheSidebar.vue";
import HamburgerButton from "./TheSidebar/HamburgerButton.vue";

export default {
  name: "TheHeader",
  components: { PlusIcon, SearchIcon, TheLogo, TheSidebar, HamburgerButton },
  data() {
    return {
      inputValue: null,
      navLinks: [
        {
          route_name: "selections-plan",
          icon: "plus-icon",
          label: "New Quotes",
        },
      ],
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
