<template>
  <button
    :class="{
      uppercase: true,
      'tracking-wide': true,
      'font-light': true,
      'rounded-md': true,
      'border-2': true,
      'px-8': true,
      'py-2': true,
      'hover:bg-opacity-80': true,
      'hover:scale-105': true,
      'ease-out': true,
      'duration-300': true,
      'bg-gray-300': $attrs.disabled,
      'text-gray-100': $attrs.disabled,
    }"
    v-bind="$attrs"
  >
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: "AppButton",
  props: {
    to: {
      required: false,
    },
  },
};
</script>

<style></style>
