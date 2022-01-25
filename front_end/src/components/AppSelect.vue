<template>
  <label class="flex justify-end items-center text-right">
    <slot />
    <select
      v-bind="$attrs"
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
      class="ml-8 rounded-md border-2 py-1 mx-4 placeholder:text-inherit placeholder:font-extralight focus:border-0 focus:ring-2 focus:ring-theme-primary"
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
