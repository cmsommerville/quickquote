<template>
  <label>
    <input
      class="mr-8 rounded-sm"
      type="checkbox"
      v-bind="$attrs"
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
    />
    <slot></slot>
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
