<template>
  <div class="sidebar">
    <div
      class="w-screen h-screen fixed top-0 left-0 cursor-pointer bg-black bg-opacity-50"
      @click="closeSidebarPanel"
      v-if="isPanelOpen"
    ></div>
    <transition name="slide">
      <div
        v-if="isPanelOpen"
        class="w-64 h-screen fixed top-0 left-0 z-50 bg-white overflow-y-auto px-2"
      >
        <div v-bind="$attrs">
          <slot></slot>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "TheSidebar",
  inheritAttrs: false,
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
