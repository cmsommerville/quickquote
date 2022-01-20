<template>
  <label class="flex justify-end items-center text-right">
    <slot></slot>
    <input
      class="ml-8 rounded-sm"
      type="checkbox"
      v-bind="$attrs"
      :value="modelValue"
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
