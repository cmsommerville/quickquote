<template>
  <div class="w-full bg-white shadow-xl rounded-md min-h-96 p-8">
    <h2 class="font-bold text-3xl">
      <slot name="title"></slot>
    </h2>
    <h3 class="font-normal text-md mb-6">
      <slot name="subtitle"></slot>
    </h3>

    <div :class="'grid grid-cols-' + stages.length">
      <span
        v-for="(stage, i) in stages"
        :key="stage.id"
        :class="{
          ...stageBaseClasses,
          'border-r': i === (stages.length ?? -1),
          'border-gray-300': i === (stages.length ?? -1),
          'border-b-4': stage.active,
          'border-b-red-500': stage.active,
          'text-red-500': stage.active,
        }"
        >{{ stage.label }}</span
      >
    </div>

    <slot name="content"></slot>
    <slot name="actions">
      <div class="flex justify-center my-8">
        <app-button
          class="mx-3 border-red-500 bg-red-500 text-white"
          to="/about"
          >Next</app-button
        >
      </div>
    </slot>
  </div>
</template>

<script>
export default {
  name: "AppFormCard",
  props: {
    stages: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      stageBaseClasses: {
        "text-center": true,
        "bg-gray-200": true,
        "p-2": true,
        "text-uppercase": true,
        uppercase: true,
        "tracking-wide": true,
        "text-sm": true,
      },
    };
  },
};
</script>

<style scoped></style>
