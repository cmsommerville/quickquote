<template>
  <app-form-tabs :stages="stages" @toggle:stage="toggleHandler" />
</template>

<script>
import AppFormTabs from "@/components/AppFormCard/AppFormTabs.vue";
export default {
  name: "ProductVariationTabs",
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
          label: "Basic Info",
          id: "product_variations",
          tab: true,
        },
        {
          label: "Rating",
          id: "product_variation_rating",
          tab: true,
        },
        {
          label: "Distributions",
          id: "product_variation_distributions",
          tab: true,
        },
        {
          label: "Age Bands",
          id: "age_bands",
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
