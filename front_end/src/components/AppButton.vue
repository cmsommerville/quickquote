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
      _base: "uppercase tracking-wide font-light ease-out duration-300",
      _rect: "rounded-md border-2 px-8 py-2",
      _round: "rounded-full",
      _flat:
        "px-1 py-1 rounded-none border-b-2 border-transparent bg-transparent text-them-primary hover:border-b-2 hover:border-theme-primary",
      _btn: "bg-theme-primary text-white hover:bg-opacity-90 hover:scale-105",
      _transparent:
        "border-2 bg-transparent border-theme-primary text-theme-primary hover:bg-theme-primary hover:text-white hover:bg-opacity-90 hover:scale-105",
      _fab: "text-white hover:bg-opacity-90 hover:scale-105",

      _disabled_flat: "disabled:text-gray-500",
      _disabled_btn:
        "disabled:bg-gray-200 disabled:text-gray-500 disabled:border-0",
    };
  },
  computed: {
    classPicker() {
      let classes = [this._base];

      // shape
      if (this.fab) {
        classes = [...classes, this._round];
      } else {
        classes = [...classes, this._rect];
      }

      // disabled
      if (this.$attrs.disabled) {
        classes = [
          ...classes,
          this.flat ? this._disabled_flat : this._disabled_btn,
        ];
        return classes.join(" ");
      }

      // flat
      if (this.flat) {
        classes = [...classes, this._flat];
        return classes.join(" ");
      }

      if (this.fab && this.transparent) {
        classes = [
          ...classes,
          this.fab ? this._fab : "",
          this.transparent ? this._transparent : "",
        ];
        return classes.join(" ");
      }

      classes = [...classes, this._btn];
      return classes.join(" ");
    },
  },
};
</script>

<style></style>
