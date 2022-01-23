<template>
  <div class="sidebar">
    <div
      class="w-screen h-screen fixed top-0 left-0 cursor-pointer bg-black bg-opacity-50"
      @click="closeSidebarPanel"
      v-if="isPanelOpen"
    ></div>
    <transition name="slide">
      <nav
        v-if="isPanelOpen"
        class="w-64 h-screen fixed top-0 left-0 z-50 bg-white overflow-y-auto flex flex-col items-center"
      >
        <slot name="header">
          <div class="w-full py-3 border-b border-gray-100 flex justify-center">
            <the-logo />
          </div>
        </slot>

        <div class="w-full" v-bind="$attrs">
          <slot name="main">
            <ul class="w-full">
              <sidebar-list-item
                v-for="route in navLinks"
                :key="route.route_name"
                :route="route"
              />
            </ul>
          </slot>
        </div>
      </nav>
    </transition>
  </div>
</template>

<script>
import TheLogo from "../TheLogo.vue";
import SidebarListItem from "./SidebarListItem.vue";

export default {
  name: "TheSidebar",
  inheritAttrs: false,
  components: { SidebarListItem, TheLogo },
  data() {
    return {
      navLinks: [
        {
          route_name: "selections-plan",
          icon: "plus-icon",
          label: "New Quote",
        },
        {
          route_name: "home",
          icon: "cog-icon",
          label: "Product Factory",
        },
      ],
    };
  },
  methods: {
    closeSidebarPanel() {
      this.$store.commit("toggleNav");
    },
  },
  computed: {
    isPanelOpen() {
      return this.$store.getters.getIsNavOpen;
    },
  },
};
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.2s ease;
}

.slide-enter,
.slide-leave-to {
  transform: translateX(-100%);
  transition: all 150ms ease-in 0s;
}
</style>
