<template>
  <div class="w-full bg-white shadow-xl rounded-md min-h-96 p-8">
    <app-form-header :title="title" :subtitle="subtitle" />
    <app-form-tabs :stages="stages" @toggle:stage="toggleHandler" />
    <div class="my-12">
      <slot name="content"></slot>
    </div>
    <div class="my-8">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script>
import AppFormTabs from "./AppFormTabs.vue";
import AppFormHeader from "./AppFormHeader.vue";

export default {
  name: "AppFormCard",
  components: { AppFormTabs, AppFormHeader },
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
  methods: {
    toggleHandler(stg) {
      this.$emit("toggle:stage", stg);
    },
    handleInput(data) {
      this.$emit("input:data", data);
    },
  },
};
</script>

<style scoped></style>
