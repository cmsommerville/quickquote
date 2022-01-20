<template>
  <label class="flex justify-end items-center text-right">
    <slot />
    <select
      v-bind="$attrs"
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
      class="ml-8 rounded-md border-2 py-1 mx-4 placeholder:text-inherit placeholder:font-extralight focus:border-0 focus:ring-2 focus:ring-red-500"
    >
      <option v-for="item in items" :key="item[value]" :value="item[value]">
        {{ item[label] }}
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
    label: {
      default: "label",
    },
    value: {
      default: "code",
    },
  },
};
</script>

<style scoped></style>
