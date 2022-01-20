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
      'hover:rotate-2': true,
      'hover:cursor-pointer': true,
      'hover:scale-105': true,
      'ease-out': true,
      'duration-300': true,
      'ring-4': selected,
      'ring-red-500': selected,
    }"
    @click="$emit('update:selection', !selected)"
  >
    <div
      :class="`w-full 
        h-2/3 
        rounded-t-2xl 
        flex
        justify-center
        items-center
        bg-cover
        bg-center
        ${background}
      `"
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
  props: {
    text: {
      required: true,
    },
    background: {
      required: true,
    },
    selected: {
      required: true,
      type: Boolean,
    },
  },
};
</script>

<style></style>
