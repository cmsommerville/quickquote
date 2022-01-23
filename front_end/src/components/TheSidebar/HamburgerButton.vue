<template>
  <div id="burger" :class="{ active: isBurgerActive }" @click.prevent="toggle">
    <slot>
      <button
        type="button"
        :class="{
          'burger-button': true,
          'relative h-8 w-8 block border-0 bg-transparent focus:outline-0 cursor-pointer': true,
          '-rotate-180': isBurgerActive,
        }"
        title="Menu"
      >
        <menu-icon />
      </button>
    </slot>
  </div>
</template>

<script>
import { MenuIcon } from "@heroicons/vue/outline";
export default {
  name: "HamburgerButton",
  components: { MenuIcon },
  computed: {
    isBurgerActive() {
      return this.$store.getters.getIsNavOpen;
    },
  },
  methods: {
    toggle() {
      this.$store.commit("toggleNav");
    },
  },
};
</script>

<style scoped>
.burger-button {
  pointer-events: all;
  transition: transform 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
}
</style>
