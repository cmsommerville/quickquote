<template>
  <div class="flex w-full justify-end items-center">
    <div class="cursor-pointer mr-4" @click="clickHandler">
      <slot />
    </div>
    <label class="relative inline-block w-14 h-8 flex" :for="htmlFor">
      <input
        type="checkbox"
        ref="input"
        :id="htmlFor"
        :name="htmlFor"
        class="opacity-0 w-0 h-0"
        v-bind="$attrs"
        :value="modelValue"
        :checked="modelValue"
        @input="$emit('update:modelValue', $event.target.checked)"
      />

      <span
        class="slider rounded-full absolute cursor-pointer top-0 left-0 right-0 bottom-0 bg-gray-300 transition duration-500 before:absolute before:content-[''] before:h-6 before:w-6 before:left-1 before:bottom-1 before:bg-white before:transition before:duration-500 before:rounded-full"
      ></span>
    </label>
  </div>
</template>

<script>
export default {
  name: "AppSwitch",
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
  methods: {
    clickHandler() {
      if (!this.$attrs.disabled) {
        this.$refs.input.checked = !this.$refs.input.checked;
      }
    },
  },
};
</script>

<style scoped>
input:checked + .slider {
  background-color: var(--theme-500);
}

input:focus + .slider {
  box-shadow: 0 0 1px var(--theme-500);
}

input:checked + .slider:before {
  -webkit-transform: translateX(1.5rem);
  -ms-transform: translateX(1.5rem);
  transform: translateX(1.5rem);
}
</style>
