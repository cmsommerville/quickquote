<template>
  <div class="flex items-center text-right relative">
    <label
      :class="{
        'mr-8': !top,
        absolute: top,
        '-top-5': top,
        'left-0': top,
        'text-sm': top,
      }"
      :for="htmlFor"
    >
      <slot></slot>
    </label>
    <div
      :class="{
        'overflow-hidden': true,
        'rounded-md': true,
        'focus-within:border-transparent': true,
        'focus-within:ring-2': true,
        'focus-within:ring-theme-primary': true,
        'border-2': true,
        'py-1': true,
        'px-4': true,
        'bg-gray-100': $attrs.disabled,
        'text-gray-400': $attrs.disabled,
      }"
    >
      <span v-if="prefix" class="text-gray-300">{{ prefix }}</span>
      <input
        :id="htmlFor"
        :name="htmlFor"
        :class="{
          'border-0': true,
          'outline-0': true,
          'placeholder:text-inherit': true,
          'placeholder:font-extralight': true,
          'w-full': true,
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
  </div>
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
    top: {
      default: true,
    },
  },
  mounted() {
    this.htmlFor = (Math.random() + 1).toString(36).substring(4);
  },
  data() {
    return {
      htmlFor: "",
    };
  },
};
</script>

<style scoped>
input:focus {
  outline: none !important;
  box-shadow: none !important;
}
</style>
