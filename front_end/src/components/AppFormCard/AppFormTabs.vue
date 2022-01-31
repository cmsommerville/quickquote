<template>
  <div>
    <div v-if="stages.length === 1" class="w-1/2 grid grid-cols-1">
      <span
        v-for="(stage, i) in stages"
        :key="stage.id"
        :class="{
          ...stageBaseClasses,
          'border-b-4': true,
          'border-b-theme-primary': true,
          'text-theme-primary': true,
          'cursor-pointer': !stage.disabled,
        }"
        @click="toggleHandler(stage)"
        >{{ stage.label }}
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
          'hover:text-theme-primary': !stage.disabled,
          'hover:font-medium': !stage.disabled,
          'cursor-pointer': !stage.disabled,
        }"
        @click="toggleHandler(stage)"
        >{{ stage.label }}</span
      >
    </div>
  </div>
</template>

<script>
export default {
  name: "AppFormTabs",
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
  methods: {
    toggleHandler(stg) {
      if (!stg.disabled) {
        this.$emit("toggle:stage", stg);
      }
    },
  },
};
</script>

<style scoped></style>
