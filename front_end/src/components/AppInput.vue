<template>
  <label class="flex justify-end items-center text-right">
    <slot></slot>
    <div
      class="overflow-hidden ml-8 rounded-md focus-within:border-transparent focus-within:ring-2 focus-within:ring-theme-primary border-2 py-1 px-4 mx-4"
    >
      <span v-if="prefix" class="text-gray-300">{{ prefix }}</span>
      <input
        class="border-0 outline-0 placeholder:text-inherit placeholder:font-extralight"
        v-bind="$attrs"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
      />
      <span v-if="suffix" class="text-gray-300">{{ suffix }}</span>
    </div>
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
    prefix: {
      default: "",
    },
    suffix: {
      default: "",
    },
  },
};
</script>

<style scoped></style>
