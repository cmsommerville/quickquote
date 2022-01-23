<template>
  <li
    class="text-gray-500 w-full py-3 flex items-center justify-center tracking-wide uppercase hover:text-theme-primary"
  >
    <slot>
      <router-link
        :to="{ name: route.route_name }"
        class="flex justify-end items-center w-full px-4"
      >
        <span class="inline-block mr-2">{{ route.label }}</span>
        <component :is="route.icon" class="inline-block w-6 h-6" />
      </router-link>
    </slot>
  </li>
</template>

<script>
import { PlusIcon, PuzzleIcon, CogIcon } from "@heroicons/vue/outline";

export default {
  name: "SidebarListItem",
  components: { PlusIcon, PuzzleIcon, CogIcon },
  props: {
    route: {
      type: Object,
      required: false,
    },
  },
};
</script>

<style></style>
