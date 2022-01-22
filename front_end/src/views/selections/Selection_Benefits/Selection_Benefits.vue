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
        <selection-benefits-covg-panel
          v-for="coverage in coverages"
          :key="coverage.coverage_id"
          :coverage="coverage"
          :label="coverage.coverage_label"
          @selections:change="coverageHandler"
        />
      </template>

      <template #actions>
        <div class="flex justify-center">
          <app-button
            class="mx-3 border-theme-primary bg-theme-primary text-white"
            @click="save"
            >Next</app-button
          >
          <app-button
            type="reset"
            class="mx-3 border-theme-primary"
            :transparent="true"
            >Reset</app-button
          >
        </div>
      </template>
    </app-form-card>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import AppFormCard from "@/components/AppFormCard/AppFormCard.vue";
import SelectionBenefitsCovgPanel from "@/views/selections/Selection_Benefits/Selection_Benefits_CovgPanel.vue";

export default {
  name: "SelectionBenefits",
  components: { AppFormCard, SelectionBenefitsCovgPanel },
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
      coverages: [],
      selections: [],
      error: null,
    };
  },
  async mounted() {
    this.loaded = false;
    const res = await axios.get(`selections/plan/${this.plan_id}/benefits`);
    const section_coverages = [...res.data];
    this.coverages = [
      ...section_coverages.find((section) => {
        return section.section_code === this.section_code;
      }).coverages,
    ];
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
    output() {
      return {};
    },
  },
  methods: {
    toggleStageHandler(id) {
      console.log(id);
    },
    coverageHandler(el) {
      this.selections = [
        ...this.selections.filter((item) => {
          item.coverage_code !== el.coverage_code;
        }),
        { ...el },
      ];
    },
    routeTo(route_name) {
      this.$router.push({
        name: route_name,
      });
    },
    initialize(data) {
      this.product_variation_id =
        data.product_variations[0].product_variation_id;
    },
    async save() {
      const plan = await axios.post(
        `/selections/plan/${this.plan_id}/benefits`,
        this.output
      );
      if (plan.status === 201) {
        this.routeTo({
          name: "selections-provisions",
          params: {
            plan_id: plan.data.selection_plan_id,
          },
        });
      }
    },
    onReset() {
      console.log("Reset");
    },
  },
};
</script>

<style scoped></style>
