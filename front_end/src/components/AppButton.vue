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
      'bg-theme-primary': !$attrs.disabled && !transparent,
      'text-white': !$attrs.disabled && !transparent,
      'hover:bg-opacity-90': !$attrs.disabled && !transparent,

      'bg-transparent': !$attrs.disabled && transparent,
      'border-theme-primary': !$attrs.disabled && transparent,
      'text-theme-primary': !$attrs.disabled && transparent,
      'hover:bg-theme-primary': !$attrs.disabled && transparent,
      'hover:text-white': !$attrs.disabled && transparent,
      'hover:bg-opacity-70': !$attrs.disabled && transparent,

      'hover:scale-105': !$attrs.disabled,
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
