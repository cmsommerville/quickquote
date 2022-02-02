<template>
  <app-form-tabs :stages="stages" @toggle:stage="toggleHandler" />
</template>

<script>
import AppFormTabs from "@/components/AppFormCard/AppFormTabs.vue";
export default {
  name: "AgeBandsTabs",
  components: { AppFormTabs },
  props: {
    active_stage: {
      required: true,
      type: String,
    },
    disabled: {
      default: [],
    },
  },
  data() {
    return {
      _stages: [
        {
          label: "Age Bands",
          id: "landing",
          disabled: true,
        },
        {
          label: "Configure",
          id: "configure",
          disabled: true,
        },
        {
          label: "States",
          id: "states",
          disabled: true,
        },
      ],
    };
  },
  computed: {
    stages() {
      return this._stages.map((item) => ({
        ...item,
        active: item.id === this.active_stage,
      }));
    },
  },
  methods: {
    toggleHandler(stg) {
      this.$emit("toggle:stage", stg);
    },
  },
};
</script>

<style></style>
