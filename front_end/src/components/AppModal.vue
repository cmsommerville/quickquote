<template>
  <div
    v-if="open"
    class="fixed top-0 left-0 z-40 bg-black bg-opacity-50 w-screen h-screen flex justify-center items-center"
    @click="closeHandler"
  >
    <div
      class="min-w-1/3 min-h-1/2 z-50 bg-gray-100 rounded-md overflow-hidden"
      @click.stop
    >
      <div class="w-full h-16 bg-gray-300 px-8 py-2 relative flex items-center">
        <div class="text-3xl font-light">
          <slot name="header" />
        </div>
        <x-icon
          class="absolute top-2 right-2 w-6 h-6 cursor-pointer"
          @click="closeHandler"
        />
      </div>
      <div class="px-8 py-2">
        <slot name="content" :close="closeHandler" />
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
  emits: ["close:modal"],
  data() {
    return {
      open: false,
    };
  },
  methods: {
    openHandler() {
      this.open = true;
    },
    closeHandler() {
      this.$emit("close:modal");
      this.open = false;
    },
  },
};
</script>

<style></style>
