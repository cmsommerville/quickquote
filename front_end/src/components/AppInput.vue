<template>
  <label
    class="font-extralight uppercase text-white opacity-50 flex items-center"
  >
    <slot></slot>
    <input
      class="
        rounded-md
        border
        py-1
        px-4
        mx-4
        placeholder:text-inherit placeholder:font-extralight
      "
      v-bind="$attrs"
      v-on="$listeners"
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
