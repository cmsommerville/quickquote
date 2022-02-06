<template>
  <button :class="classPicker" v-bind="$attrs">
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
    flat: {
      default: false,
    },
  },
  data() {
    return {
      classes_base: {
        uppercase: true,
        "tracking-wide": true,
        "font-light": true,
        "ease-out": true,
        "duration-300": true,
        "rounded-md": true,
      },
      classes_btn: {
        "border-2": true,
        "px-8": true,
        "py-2": true,
        "bg-theme-primary": true,
        "text-white": true,
        "hover:bg-opacity-90": true,
        "hover:scale-105": true,
      },
      classes_disabled: {
        "border-2": true,
        "px-8": true,
        "py-2": true,
        "bg-gray-200": true,
        "text-gray-500": true,
      },
      classes_flat: {
        "px-1": true,
        "py-1": true,
        "rounded-none": true,
        "border-b-2": true,
        "border-transparent": true,
        "bg-transparent": true,
        "text-theme-primary": true,
        "hover:border-b-2": true,
        "hover:border-theme-primary": true,
      },
      classes_transparent: {
        "border-2": true,
        "px-8": true,
        "py-2": true,
        "bg-transparent": true,
        "border-theme-primary": true,
        "text-theme-primary": true,
        "hover:bg-theme-primary": true,
        "hover:text-white": true,
        "hover:bg-opacity-70": true,
        "hover:scale-105": true,
      },
      classes_fab: {
        "rounded-full": true,
        "bg-theme-primary": true,
        "text-white": true,
        "hover:bg-opacity-90": true,
        "hover:scale-105": true,
      },
    };
  },
  computed: {
    classPicker() {
      if (this.$attrs.disabled)
        return { ...this.classes_base, ...this.classes_disabled };
      if (this.flat) return { ...this.classes_base, ...this.classes_flat };
      if (this.transparent)
        return { ...this.classes_base, ...this.classes_transparent };
      if (this.fab) return { ...this.classes_base, ...this.classes_fab };
      return { ...this.classes_base, ...this.classes_btn };
    },
  },
};
</script>

<style></style>
