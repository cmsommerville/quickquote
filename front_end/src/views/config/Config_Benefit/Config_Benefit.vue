<template>
  <div v-if="loaded">
    <app-form-card
      :stages="stages"
      :title="title"
      :subtitle="subtitle"
      @toggle:stage="toggleHandler"
    >
      <template #content>
        <div class="grid grid-cols-2 gap-6">
          <!-- CARD 1 -->
          <div class="flex flex-col">
            <div
              class="grid grid-cols-2 gap-x-12 shadow-lg rounded-md p-4 mb-8 border border-gray-200"
            >
              <div
                class="border-b border-gray-200 py-2 mb-8 w-full text-center col-span-2"
              >
                <h2 class="text-xl font-medium">Basic Info</h2>
              </div>
              <div class="mb-8">
                <app-input v-model="benefit.benefit_code"
                  >Benefit Code</app-input
                >
              </div>
              <div class="mb-8">
                <app-input v-model="benefit.benefit_label"
                  >Benefit Name</app-input
                >
              </div>
              <div class="mb-8">
                <app-input v-model="benefit.benefit_effective_date" type="date"
                  >Effective Date</app-input
                >
              </div>
              <div class="mb-8">
                <app-input v-model="benefit.benefit_expiration_date" type="date"
                  >Expiration Date</app-input
                >
              </div>
            </div>

            <!-- CARD 3 -->
            <div
              class="grid grid-cols-2 gap-x-12 shadow-lg rounded-md mb-8 p-4 border border-gray-200"
            >
              <div
                class="border-b border-gray-200 py-2 mb-8 w-full text-center col-span-2"
              >
                <h2 class="text-xl font-medium">Rating</h2>
              </div>
              <div class="mb-8">
                <app-select
                  v-model.number="benefit.coverage_id"
                  :items="coverages"
                  item_text="coverage_label"
                  item_value="coverage_id"
                  >Coverage</app-select
                >
              </div>
              <div class="mb-8">
                <app-select
                  v-model.number="benefit.rate_group_id"
                  :items="rate_groups"
                  item_text="rate_group_label"
                  item_value="rate_group_id"
                  >Rate Group</app-select
                >
              </div>
              <div class="mb-8 col-span-2 mx-auto">
                <app-switch v-model="benefit.is_durational"
                  >Rated by Duration</app-switch
                >
              </div>
            </div>
          </div>
          <div class="flex flex-col">
            <!-- CARD 2 -->
            <div
              class="grid grid-cols-2 gap-x-12 shadow-lg rounded-md p-4 mb-8 border border-gray-200"
            >
              <div
                class="border-b border-gray-200 py-2 mb-8 w-full text-center col-span-2"
              >
                <h2 class="text-xl font-medium">Amounts</h2>
              </div>
              <div class="mb-8">
                <app-select
                  v-model="benefit.unit_code"
                  :items="unit_codes"
                  item_text="unit_label"
                  item_value="unit_code"
                  >Unit Code</app-select
                >
              </div>
              <div class="mb-8 col-start-1">
                <app-input
                  v-model.number="benefit.min_value"
                  type="number"
                  :suffix="suffix"
                >
                  Benefit Minimum
                </app-input>
              </div>
              <div class="mb-8">
                <app-input
                  v-model.number="benefit.max_value"
                  type="number"
                  :suffix="suffix"
                  >Benefit Maximum</app-input
                >
              </div>
              <div class="mb-8">
                <app-input
                  v-model.number="benefit.step_value"
                  type="number"
                  :suffix="suffix"
                  >Step Size</app-input
                >
              </div>
              <div class="mb-8">
                <app-input
                  v-model.number="benefit.default_value"
                  type="number"
                  :suffix="suffix"
                  >Default Value</app-input
                >
              </div>
            </div>
            <!-- CARD 4 -->
            <div
              class="grid grid-cols-1 gap-x-12 shadow-lg rounded-md p-4 mb-8 border border-gray-200"
            >
              <div
                class="border-b border-gray-200 py-2 mb-8 w-full text-center"
              >
                <h2 class="text-xl font-medium">States</h2>
              </div>
              <div class="flex flex-col justify-center items-center">
                <app-checkbox v-model="multiple_states"
                  >Will this benefit be used in multiple states?</app-checkbox
                >
                <div class="mt-12 mb-4">
                  <app-select
                    v-if="!multiple_states"
                    v-model="benefit.state_id"
                    :items="states"
                    item_text="state_name"
                    item_value="state_id"
                    >Choose a state</app-select
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <template #actions>
        <div class="flex justify-center">
          <app-button class="mx-3" @click="save">Next</app-button>
        </div>
      </template>
    </app-form-card>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import { Model_ConfigBenefit } from "@/models/Model_ConfigBenefit.js";

export default {
  name: "Config_Benefit",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    benefit_id: {
      default: null,
      type: [Number, String, null],
    },
  },
  mounted() {
    this.loaded = false;
    let p_benefit;
    if (this.benefit_id) {
      p_benefit = axios.get(`/config/benefit/${this.benefit_id}`);
    } else {
      p_benefit = new Promise((resolve, reject) => {
        resolve({ data: {} });
      });
    }

    const p_rate_groups = axios.get(
      `/qry-config/all-rate-groups?product_id=${this.product_id}`
    );
    const p_coverages = axios.get(
      `/qry-config/all-coverages?product_id=${this.product_id}`
    );
    const p_states = axios.get(`/config/ref-states`);
    const p_unit_codes = axios.get("/config/ref-unit-codes");
    Promise.all([p_benefit, p_unit_codes, p_rate_groups, p_coverages, p_states])
      .then(([benefit, unit_codes, rate_groups, coverages, states]) => {
        const bnft = { ...benefit.data };
        this.unit_codes = [...unit_codes.data];
        this.rate_groups = [...rate_groups.data];
        this.coverages = [...coverages.data];
        this.states = [...states.data];

        if (!bnft.child_states) {
          this.multiple_states = true;
        } else if (bnft.child_states.length > 0) {
          this.multiple_states = true;
        } else {
          this.multiple_states = false;
        }

        this.benefit = this.applyModel(
          this.product_id,
          bnft,
          this.multiple_states
        );

        this.loaded = true;
      })
      .catch((err) => {
        this.loaded = true;
      });
  },
  data() {
    return {
      loaded: false,
      title: "Setup This Benefit",
      subtitle: "",
      active_stage: "configure",
      _stages: [
        {
          label: "All Benefits",
          id: "landing",
          to: "config-benefits",
        },
        {
          label: "Configure",
          id: "configure",
          disabled: true,
        },
      ],
      multiple_states: true,
      benefit: {},
      unit_codes: [],
      rate_groups: [],
      coverages: [],
      states: [],
    };
  },
  computed: {
    stages() {
      return this._stages.map((item) => ({
        ...item,
        active: item.id === this.active_stage,
      }));
    },
    suffix() {
      return this.benefit.unit_code === "percent" ? "%" : "$";
    },
    output() {
      const bnft = this.applyModel(
        this.product_id,
        this.benefit,
        this.multiple_states
      );

      if (this.benefit.benefit_id) {
        bnft.set_benefit_id(this.benefit.benefit_id);
      }

      return bnft;
    },
  },
  methods: {
    applyModel(product_id, data, multiple_states) {
      return new Model_ConfigBenefit(
        data.benefit_id,
        product_id,
        multiple_states ? 0 : data.state_id,
        data.benefit_code,
        data.benefit_label,
        data.benefit_effective_date,
        data.benefit_expiration_date,
        data.coverage_id,
        data.rate_group_id,
        data.min_value,
        data.max_value,
        data.step_value,
        data.default_value,
        data.unit_code,
        data.is_durational
      );
    },
    routeTo(route_name, query = {}) {
      this.$router.push({
        name: route_name,
        params: { product_id: this.product_id },
        query: { ...query },
      });
    },
    sortOrderHandler() {
      console.log("Sort order handler!");
    },
    toggleHandler(stage) {
      this.routeTo(stage.to);
    },
    async save() {
      try {
        const bnft = await axios.post("/config/benefit", this.output);
        this.benefit = { ...bnft.data };
        this.$store.commit("SET_SELECTIONS_OBJECT", this.benefit);
        this.$store.dispatch(
          "SET_SNACKBAR_MESSAGE",
          "Inserted benefit to database!"
        );

        if (this.multiple_states) {
          this.routeTo("config-benefit-states", {
            benefit_id: this.benefit.benefit_id,
          });
        } else {
          this.routeTo("config-product");
        }
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
  },
};
</script>
