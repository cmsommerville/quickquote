<template>
  <label class="flex justify-end items-center text-right">
    <slot></slot>
    <input
      class="ml-8 rounded-sm text-theme-primary hover:outline hover:outline-offset-2 hover:outline-2 hover:outline-theme-primary focus:outline focus:outline-2 focus:outline-theme-primary"
      type="checkbox"
      v-bind="$attrs"
      :value="modelValue"
      :checked="modelValue"
      @input="$emit('update:modelValue', $event.target.checked)"
    />
  </label>
</template>

<script>
export default {
  name: "AppCheckbox",
  inheritAttrs: false,
  props: {
    modelValue: {
      required: true,
      type: Boolean,
    },
  },
};
</script>

<style></style>
