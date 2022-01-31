<template>
  <label class="flex justify-end items-center text-right">
    <slot />
    <select
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
      :class="{
        'ml-8': true,
        'rounded-md': true,
        'border-2': true,
        'border-gray-300': true,
        'py-1': true,
        'pl-2': true,
        'pr-10': true,
        'mx-4': true,

        'placeholder:text-inherit': true,
        'placeholder:font-extralight': true,
        'focus:border-transparent': true,
        'focus:ring-2': true,
        'focus:ring-theme-primary': true,
      }"
      v-bind="$attrs"
    >
      <option
        v-for="item in items"
        :key="item[item_value]"
        :value="item[item_value]"
      >
        {{ item[item_text] }}
      </option>
    </select>
  </label>
</template>

<script>
export default {
  name: "AppSelect",
  inheritAttrs: false,
  props: {
    modelValue: {
      required: true,
    },
    items: {
      required: true,
      type: Array,
    },
    item_text: {
      default: "label",
    },
    item_value: {
      default: "code",
    },
  },
};
</script>

<style scoped></style>
