<template>
  <label class="flex justify-end items-center text-right">
    <slot></slot>
    <input
      class="ml-8 rounded-md focus:border-0 focus:ring-2 focus:ring-theme-primary border-2 py-1 px-4 mx-4 placeholder:text-inherit placeholder:font-extralight"
      v-bind="$attrs"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </label>
</template>

<script>
export default {
  name: "AppInput",
  inheritAttrs: false,
  props: {
    modelValue: {
      required: true,
    },
  },
};
</script>

<style></style>
