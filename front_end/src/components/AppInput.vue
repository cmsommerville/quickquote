<template>
  <div class="flex items-center text-right relative">
    <div
      v-show="showTooltip"
      :id="`tooltip-${htmlFor}`"
      class="absolute z-50 max-w-48 bg-theme-primary text-white text-center py-2 px-4 text-xs rounded-md text-ellipsis"
      :style="{
        top: tooltip_Y + 'px',
        right: tooltip_X + 'px',
      }"
    >
      <slot name="tooltip" />
    </div>
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
      v-if="$slots.tooltip"
      class="h-4 w-4 absolute -top-4 right-3 bg-indigo-400 text-white rounded-full"
      @mouseenter="setMousePosition"
      @mouseover="displayTooltip"
      @mouseleave="showTooltip = false"
    >
      <question-mark-circle-icon />
    </div>
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
          'bg-transparent': true,
          'placeholder:text-inherit': true,
          'placeholder:font-extralight': true,
          'w-full': !suffix,
          'w-90%': suffix,
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
      showTooltip: false,
      tooltip_X: 0,
      tooltip_Y: 0,
    };
  },
  methods: {
    setMousePosition(ev) {
      const tt = document.getElementById(`tooltip-${this.htmlFor}`);
      this.tooltip_Y = ev.offsetY - tt.offsetHeight - 30;
      this.tooltip_X = ev.offsetX - tt.offsetWidth / 2;
    },
    displayTooltip(ev) {
      this.setMousePosition(ev);
      this.showTooltip = true;
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
