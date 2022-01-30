<template>
  <div class="mb-12 flex justify-between">
    <div>
      <h2 class="font-bold text-3xl">{{ title }}</h2>
      <h3 v-if="subtitle" class="font-normal text-md">{{ subtitle }}</h3>
    </div>
    <slot name="addl-info"></slot>
  </div>
</template>

<script>
export default {
  name: "AppFormHeader",
  props: {
    title: {
      type: String,
      required: true,
    },
    subtitle: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped></style>
