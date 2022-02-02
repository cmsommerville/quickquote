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
  },
  data() {
    return {
      _stages: [
        { label: "Back to Product", id: "product", to: "config-product" },
        {
          label: "Age Bands",
          id: "landing",
          tab: true,
        },
        {
          label: "Edit",
          id: "configure",
          tab: true,
        },
        {
          label: "States",
          id: "states",
          tab: true,
        },
      ],
    };
  },
  computed: {
    stages() {
      const ix = this._stages.findIndex(
        (item) => item.id === this.active_stage
      );

      const lower = Math.min(Math.max(ix - 1, 0), this._stages.length - 4);
      const upper = lower + 4;

      return this._stages
        .map((item) => ({
          ...item,
          active: item.id === this.active_stage,
        }))
        .slice(lower, upper);
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
