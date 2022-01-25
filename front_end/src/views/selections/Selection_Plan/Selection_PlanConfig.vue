<template>
  <div v-if="loaded">
    <app-form-card :stages="stages" :title="title" :subtitle="subtitle">
      <template #content>
        <div class="grid grid-cols-2 xl:grid-cols-2 gap-8">
          <div class="grid grid-rows-3 gap-6">
            <app-select
              class="w-60"
              v-model="product_variation_id"
              :items="config.product_variations"
              item_text="product_variation_label"
              item_value="product_variation_id"
              >Product Variation
            </app-select>

            <app-select
              class="w-60"
              v-model="state_id"
              :items="states"
              item_text="state_name"
              item_value="state_id"
              >Rating State
            </app-select>

            <app-input class="w-60" v-model="plan_effective_date" type="date"
              >Plan Effective Date
            </app-input>
          </div>
          <div class="mx-auto flex flex-col">
            <app-checkbox class="my-4" v-model="is_gender_distinct"
              >Gender Distinct
            </app-checkbox>
            <app-checkbox class="my-4" v-model="is_smoker_distinct"
              >Smoker Distinct
            </app-checkbox>
          </div>
        </div>
      </template>

      <template #actions>
        <div class="flex justify-center">
          <app-button
            class="mx-3 border-theme-primary bg-theme-primary text-white"
            @click="save"
            >Next</app-button
          >
          <app-button type="reset" class="mx-3 border-theme-primary"
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
  name: "SelectionPlanConfig",
  components: { AppFormCard },
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
  },
  data() {
    return {
      loaded: false,
      title: "Start a New Plan",
      subtitle: "Let's configure it!",
      stages: [
        { label: "Product", id: "product" },
        { label: "Configure", id: "config", active: true },
      ],
      product_variation_id: null,
      state_id: null,
      plan_effective_date: null,
      is_gender_distinct: false,
      is_smoker_distinct: false,
      error: null,
      config: {},
    };
  },
  async mounted() {
    const res = await axios.get(`/config/product/${this.product_id}`);
    this.config = { ...res.data };
    this.initialize(res.data);
    this.loaded = true;
  },
  computed: {
    states() {
      return this.config.states.map((state) => {
        return {
          state_name: state.state.state_name,
          state_id: state.state_id,
        };
      });
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
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        params: { ...params },
      });
    },
    initialize(data) {
      this.product_variation_id =
        data.product_variations[0].product_variation_id;
    },
    async save() {
      const plan = await axios.post("/selections/plan", this.output);
      if (plan.status === 201) {
        this.routeTo("selections-benefits", {
          plan_id: plan.data.selection_plan_id,
        });
      }
    },
    onReset() {
      console.log("Reset");
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
