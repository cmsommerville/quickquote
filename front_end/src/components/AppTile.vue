<template>
  <div
    :class="{
      'm-6': true,
      'h-48': true,
      'w-48': true,
      'shadow-2xl': true,
      'rounded-2xl': true,
      flex: true,
      'flex-col': true,
      'justify-center': true,
      'items-center': true,
      pulse: !disabled,
      'hover:rotate-2': !disabled,
      'hover:cursor-pointer': !disabled,
      'hover:scale-105': !disabled,
      'ease-out': true,
      'duration-300': true,
      'ring-4': !disabled && selected,
      'ring-theme-primary': !disabled && selected,
    }"
    @click="clickHandler"
  >
    <div
      :class="`w-full 
        h-2/3 
        rounded-t-2xl 
        flex
        justify-center
        items-center
        ${disabled ? 'bg-gray-500' : background}
      `"
      v-bind="$attrs"
    >
      <slot />
    </div>
    <div
      class="w-full h-1/3 bg-white rounded-b-2xl flex justify-center items-center font-bold text-gray-600 text-lg text-center tracking-wide"
    >
      {{ text }}
    </div>
  </div>
</template>

<script>
export default {
  name: "AppTile",
  inheritAttrs: false,
  props: {
    text: {
      required: true,
    },
    radio_group: {
      default: "radio_group",
    },
    background: {
      default: "",
    },
    selected: {
      required: true,
      type: Boolean,
    },
    disabled: {
      default: false,
      type: Boolean,
    },
  },
  methods: {
    clickHandler() {
      if (!this.disabled) this.$emit("update:selection", !this.selected);
    },
  },
};
</script>

<style scoped>
.pulse:focus-within {
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.97);
  }

  50% {
    transform: scale(1.03);
  }

  100% {
    transform: scale(0.97);
  }
}
</style>
