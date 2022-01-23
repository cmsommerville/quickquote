<template>
  <li
    class="text-gray-500 w-full py-3 flex items-center justify-center tracking-wide uppercasee"
  >
    <slot>
      <router-link
        :to="{ name: route.route_name }"
        class="flex justify-center items-center w-full"
      >
        <span class="inline-block mr-2">{{ route.label }}</span>
        <component :is="route.icon" class="inline-block w-6 h-6" />
      </router-link>
    </slot>
  </li>
</template>

<script>
import { PlusIcon } from "@heroicons/vue/outline";

export default {
  name: "SidebarListItem",
  components: { ...PlusIcon },
  props: {
    route: {
      type: Object,
      required: false,
    },
  },
};
</script>

<style></style>
