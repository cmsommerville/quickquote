<template>
  <div v-if="loaded">
    <app-form-card
      :stages="stages"
      :title="title"
      :subtitle="subtitle"
      @toggle:stage="toggleHandler"
    >
      <template #content>
        <div class="grid grid-cols-4 pt-6">
          <div class="flex flex-col items-center col-start-2">
            <div class="mb-12">
              <app-input v-model="coverage.coverage_code"
                >Coverage Code</app-input
              >
            </div>
            <div>
              <app-input v-model="coverage.coverage_label"
                >Coverage Name</app-input
              >
            </div>
          </div>
          <div class="flex flex-col items-center col-start-3">
            <div class="mb-12">
              <app-input v-model="coverage.section_code"
                >Section Code</app-input
              >
            </div>
            <div>
              <app-input v-model="coverage.sort_order"
                >Coverage Sort Order</app-input
              >
            </div>
          </div>
        </div>
      </template>

      <template #actions>
        <div class="flex justify-center">
          <app-button class="mx-3" :disabled="!validate" @click="save"
            >Save</app-button
          >
        </div>
      </template>
    </app-form-card>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import { Model_ConfigCoverage } from "@/models/Model_ConfigCoverage.js";

export default {
  name: "Config_Coverage",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    coverage_id: {
      default: null,
      type: [Number, String, null],
    },
  },
  async mounted() {
    this.loaded = false;
    if (this.coverage_id) {
      const coverage = await axios.get(`/config/coverage/${this.coverage_id}`);
      this.coverage = { ...coverage.data };
    }
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      title: "Setup This Coverage",
      subtitle: "",
      active_stage: "configure",
      _stages: [
        {
          label: "All Coverages",
          id: "landing",
          to: "config-coverages",
        },
        {
          label: "Configure",
          id: "configure",
          disabled: true,
        },
      ],
      coverage: {},
    };
  },
  computed: {
    stages() {
      return this._stages.map((item) => ({
        ...item,
        active: item.id === this.active_stage,
      }));
    },
    output() {
      const coverage = new Model_ConfigCoverage(
        this.product_id,
        this.coverage.coverage_code,
        this.coverage.coverage_label,
        this.coverage.section_code
      );

      if (this.coverage.coverage_id)
        coverage.set_coverage_id(this.coverage.coverage_id);

      return coverage;
    },
    validate() {
      const coverage = new Model_ConfigCoverage(
        this.product_id,
        this.coverage.coverage_code,
        this.coverage.coverage_label,
        this.coverage.section_code
      );

      return coverage.validate();
    },
  },
  methods: {
    routeTo(route_name, query = {}) {
      this.$router.push({
        name: route_name,
        params: { product_id: this.product_id },
        query: { ...query },
      });
    },
    toggleHandler(stage) {
      this.routeTo(stage.to);
    },
    async save() {
      try {
        let msg;
        if (this.output.coverage_id) {
          await axios.put(
            `/config/coverage/${this.output.coverage_id}`,
            this.output
          );
          msg = "Coverage updated in database";
        } else {
          await axios.post("/config/coverage", this.output);
          msg = "Coverage saved to database";
        }
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", msg);
        this.routeTo("config-coverages");
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
  },
};
</script>
