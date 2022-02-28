<template>
  <div
    :class="{
      flex: true,
      'items-center': true,
      relative: true,
    }"
  >
    <label
      :class="{
        'text-right': true,
        'mr-8': !top,
        absolute: top,
        '-top-5': top,
        'left-0': top,
        'text-sm': top,
      }"
      :for="htmlFor"
    >
      <slot />
    </label>
    <select
      :id="htmlFor"
      :name="htmlFor"
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
      :class="{
        'rounded-md': true,
        'border-2': true,
        'border-gray-300': true,
        'py-1': true,
        'pl-2': true,
        'pr-10': true,
        'w-full': true,
        'bg-transparent': true,

        'placeholder:text-inherit': true,
        'placeholder:font-extralight': true,
        'focus:border-transparent': true,
        'focus:ring-2': true,
        'focus:ring-theme-primary': true,
      }"
      v-bind="$attrs"
    >
      <option
        v-for="(item, i) in _items"
        :key="item.code"
        :value="item.code"
        :hidden="item.hidden"
      >
        {{ item.label }}
      </option>
    </select>
  </div>
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
  computed: {
    _items() {
      return [
        // { label: "Select an option", code: null, hidden: true },
        ...this.items.map((item) => {
          return {
            label: item[this.item_text],
            code: item[this.item_value],
            hidden: false,
          };
        }),
      ];
    },
  },
};
</script>

<style scoped></style>
