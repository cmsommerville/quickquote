<template>
  <div class="w-full bg-white shadow-xl rounded-md min-h-96 p-8">
    <div class="mb-12">
      <h2 class="font-bold text-3xl">{{ title }}</h2>
      <h3 class="font-normal text-md">{{ subtitle }}</h3>
    </div>
    <div v-if="stages.length === 1" class="w-1/2 grid grid-cols-1">
      <span
        v-for="(stage, i) in stages"
        :key="stage.id"
        :class="{
          ...stageBaseClasses,
          'border-b-4': true,
          'border-b-theme-primary': true,
          'text-theme-primary': true,
        }"
      >
        <router-link v-if="!!stage.to" :to="{ name: stage.to }">{{
          stage.label
        }}</router-link>
        <span v-else>{{ stage.label }}</span>
      </span>
    </div>
    <div v-if="stages.length > 1" :class="'grid grid-cols-' + stages.length">
      <span
        v-for="(stage, i) in stages"
        :key="stage.id"
        :class="{
          ...stageBaseClasses,
          'border-r': i !== (stages.length - 1 ?? -1),
          'border-gray-300': i !== (stages.length - 1 ?? -1),
          'border-b-4': stage.active,
          'border-b-theme-primary': stage.active,
          'text-theme-primary': stage.active,
        }"
      >
        <router-link v-if="!!stage.to" :to="{ name: stage.to }">{{
          stage.label
        }}</router-link>
        <span v-else>{{ stage.label }}</span></span
      >
    </div>
    <div class="my-12">
      <slot name="content"></slot>
    </div>
    <div class="my-8">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppFormCard",
  props: {
    title: {
      type: String,
      required: true,
    },
    subtitle: {
      type: String,
      required: true,
    },
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
