<template>
  <div v-if="loaded">
    <app-form-card
      :stages="stages"
      :title="title"
      :subtitle="subtitle"
      :tabbed="true"
      @toggle:stage="toggleStageHandler"
    >
      <template #content>
        <div v-if="!coverages.length" class="flex justify-center items-center">
          <h2 class="text-xl">No benefits!</h2>
        </div>
        <div v-else>
          <selection-benefits-covg-panel
            v-for="coverage in coverages"
            :key="coverage.coverage_id"
            :coverage="coverage"
            :label="coverage.coverage_label"
            @selections:change="coverageHandler"
          />
        </div>
      </template>

      <template #actions>
        <div class="flex justify-center">
          <app-button
            class="mx-3 border-theme-primary bg-theme-primary text-white"
            @click="save"
            >Next</app-button
          >
        </div>
      </template>
    </app-form-card>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import Model_SelectionBenefit from "@/models/Model_SelectionBenefit.js";
import SelectionBenefitsCovgPanel from "@/views/selections/Selection_Benefits/Selection_Benefits_CovgPanel.vue";

export default {
  name: "SelectionBenefits",
  components: { SelectionBenefitsCovgPanel },
  props: {
    plan_id: {
      required: true,
      type: [Number, String],
    },
  },
  data() {
    return {
      loaded: false,
      title: "Add Some Benefits",
      subtitle: "You're half-way done!",
      section_code: "main",
      _stages: [
        { label: "Main Benefits", id: "main", active: true },
        { label: "Optional Benefits", id: "optional" },
      ],
      section_coverages: [],
      selections: [],
      error: null,
    };
  },
  async mounted() {
    this.loaded = false;
    const res = await axios.get(`selections/plan/${this.plan_id}/benefits`);
    this.section_coverages = [...res.data];
    this.loaded = true;
  },
  computed: {
    stages() {
      return [
        ...this._stages.map((stg) => {
          return { ...stg, active: stg.id === this.section_code };
        }),
      ];
    },
    coverages() {
      const ix = this.section_coverages.findIndex((section) => {
        return section.section_code === this.section_code;
      });
      if (ix < 0) {
        return [];
      }
      return [...this.section_coverages[ix].coverages];
    },
    output() {
      return this.selections.reduce((prev, covg) => {
        const benefits = covg.benefits.map((bnft) => {
          const b = new Model_SelectionBenefit(
            this.plan_id,
            bnft.config_benefit_id,
            bnft.config_rate_group_id,
            bnft.ui_benefit_value
          );
          if (bnft.selection_benefit_id) {
            b.set_selection_benefit_id(bnft.selection_benefit_id);
          }
          return b;
        });
        return [...prev, ...benefits];
      }, []);
    },
  },
  methods: {
    toggleStageHandler(id) {
      this.section_code = id;
    },
    coverageHandler(el) {
      this.selections = [
        ...this.selections.filter((item) => {
          item.coverage_code !== el.coverage_code;
        }),
        { ...el },
      ];
    },
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        params: { ...params },
      });
    },
    async save() {
      const bnfts = await axios.post(
        `/selections/plan/${this.plan_id}/benefits`,
        this.output
      );
      if (bnfts.status === 201) {
        this.routeTo({
          name: "selections-provisions",
          params: {
            plan_id: bnfts.data.selection_plan_id,
          },
        });
      }
    },
  },
};
</script>

<style scoped></style>
