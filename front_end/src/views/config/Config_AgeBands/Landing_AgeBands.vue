<template>
  <div>
    <div v-if="age_bands.length === 0" class="flex flex-col justify-center">
      <div class="w-1/2 h-2/3 mx-auto py-8 flex items-center">
        <shield-exclamation-icon class="w-24 h-24 text-gray-300 mr-4" />
        <div class="text-gray-400 uppercase tracking-wide">
          <p class="text-4xl font-extralight my-2">Uh oh!</p>
          <p class="font-light text-md">
            No age bands have been configured yet.
          </p>
        </div>
      </div>
      <div class="mx-auto mt-6">
        <app-button @click="clickHandler">Create New</app-button>
      </div>
    </div>
    <div v-else class="flex justify-center flex-col">
      <div class="grid grid-cols-2 gap-8 my-4">
        <div
          v-for="band in age_bands"
          :key="band.age_band_id"
          class="h-24 p-4 flex items-center rounded-md shadow-md text-gray-400 hover:bg-theme-primary hover:text-white hover:cursor-pointer"
          @click="selection = band"
        >
          <shield-exclamation-icon class="w-12 h-12 mr-4" />
          <div class="uppercase tracking-wide font-light">
            <p class="text-lg">Hello World!</p>
            <p class="text-sm">Hello World!</p>
          </div>
        </div>
      </div>
      <div class="mx-auto mt-12">
        <app-button @click="clickHandler">Edit</app-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LandingAgeBands",
  props: {
    age_bands: {
      required: true,
      type: Array,
    },
  },
  data() {
    return {
      selection: null,
    };
  },
  methods: {
    clickHandler() {
      this.$emit("click:edit", this.selection);
    },
  },
};
</script>

<style></style>
