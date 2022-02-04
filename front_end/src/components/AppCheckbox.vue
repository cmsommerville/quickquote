<template>
  <div
    :class="{
      'justify-end': true,
      relative: true,
      flex: true,
      'items-center': true,
      'text-right': true,
    }"
  >
    <label :for="htmlFor">
      <slot></slot>
    </label>
    <input
      :id="htmlFor"
      :name="htmlFor"
      :class="{
        'ml-8': true,
        'rounded-sm': true,
        'text-theme-primary': true,
        'hover:outline': true,
        'hover:outline-offset-2': true,
        'hover:outline-2': true,
        'hover:outline-theme-primary': true,
        'focus:outline': true,
        'focus:outline-2': true,
        'focus:outline-theme-primary': true,
      }"
      type="checkbox"
      v-bind="$attrs"
      :value="modelValue"
      :checked="modelValue"
      @input="$emit('update:modelValue', $event.target.checked)"
    />
  </div>
</template>

<script>
export default {
  name: "AppCheckbox",
  inheritAttrs: false,
  props: {
    modelValue: {
      default: false,
      type: Boolean,
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
