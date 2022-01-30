<template>
  <label class="flex justify-end items-center text-right">
    <slot></slot>
    <div
      :class="{
        'overflow-hidden': true,
        'ml-8': true,
        'rounded-md': true,
        'focus-within:border-transparent': true,
        'focus-within:ring-2': true,
        'focus-within:ring-theme-primary': true,
        'border-2': true,
        'py-1': true,
        'px-4': true,
        'mx-4': true,
        'bg-gray-100': $attrs.disabled,
        'text-gray-400': $attrs.disabled,
      }"
    >
      <span v-if="prefix" class="text-gray-300">{{ prefix }}</span>
      <input
        :class="{
          'border-0': true,
          'outline-0': true,
          'placeholder:text-inherit': true,
          'placeholder:font-extralight': true,
          'bg-gray-100': $attrs.disabled,
          'text-gray-400': $attrs.disabled,
          'p-0': true,
        }"
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

<style scoped>
input:focus {
  outline: none !important;
  box-shadow: none !important;
}
</style>
