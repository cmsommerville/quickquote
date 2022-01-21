<template>
  <div v-if="loaded">
    <app-form-card :stages="stages" :title="title" :subtitle="subtitle">
      <template #content>
        <div class="grid grid-cols-2 xl:grid-cols-2 gap-8">
          <app-input
            v-for="bnft in benefits"
            :key="bnft.config_benefit_id"
            class="w-60"
            v-model="bnft.ui_benefit_value"
            >{{ bnft.benefit_label }}
          </app-input>
        </div>
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

export default {
  name: "SelectionBenefits",
  components: { AppFormCard },
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
      subtitle: "You're half way through!",
      stages: [
        { label: "Base Benefits", id: "base", active: true },
        { label: "Optional Benefits", id: "optional" },
      ],
      coverages: [],
      selected_value: null,
      error: null,
      config: {},
    };
  },
  async mounted() {
    this.loaded = false;
    const res = await axios.get(`selections/plan/${this.plan_id}/benefits`);
    this.coverages = [...res.data];
    this.loaded = true;
  },
  computed: {
    benefits() {
      const active_stage = this.stages.find((stg) => stg.active);
      return this.coverages.find((covg) => {
        return covg.coverage_code === active_stage.id;
      }).benefits;
    },
    output() {
      return {
        config_product_id: this.product_id,
        config_product_variation_id: this.product_variation_id,
        config_state_id: this.state_id,
        plan_effective_date: this.plan_effective_date,
        is_smoker_distinct: this.is_smoker_distinct,
        is_gender_distinct: this.is_gender_distinct,
      };
    },
  },
  methods: {
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
      const plan = await axios.post("/selections/plan", this.output);
      if (plan.status === 201) {
        this.routeTo({
          name: "selections-benefits",
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
