<template>
  <button
    :class="{
      uppercase: true,
      'tracking-wide': true,
      'font-light': true,
      'rounded-md': !fab,
      'rounded-full': fab,
      'border-2': true,
      'px-8': !fab,
      'py-2': !fab,
      'hover:bg-opacity-90': !transparent,
      'hover:bg-theme-primary': transparent,
      'hover:text-white': transparent,
      'hover:bg-opacity-60': transparent,
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
    transparent: {
      default: false,
    },
    fab: {
      default: false,
    },
  },
};
</script>

<style></style>
