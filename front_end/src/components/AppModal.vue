<template>
  <div
    v-if="open"
    class="fixed top-0 left-0 z-40 bg-black bg-opacity-50 w-screen h-screen flex justify-center items-center"
    @click="open = false"
  >
    <div
      class="min-w-2/3 min-h-5/6 z-50 bg-gray-100 rounded-md overflow-hidden"
      @click.stop
    >
      <div class="w-full h-24 bg-gray-300 px-12 py-2 relative">
        <div>
          <slot name="header" />
        </div>
        <x-icon
          class="absolute top-2 right-2 w-6 h-6 cursor-pointer"
          @click="open = false"
        />
      </div>
      <div class="px-16 py-8">
        <slot name="content" />
      </div>
    </div>
  </div>
  <app-button @click="open = true" v-bind="$attrs"
    ><slot name="default">Open Modal</slot></app-button
  >
</template>

<script>
export default {
  name: "AppModal",
  inheritAttrs: false,
  data() {
    return {
      open: false,
    };
  },
};
</script>

<style></style>
