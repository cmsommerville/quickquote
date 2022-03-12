<template>
  <div v-if="loaded">
    <app-form-card
      :stages="stages"
      :title="title"
      :subtitle="subtitle"
      @toggle:stage="toggleHandler"
    >
      <template #content>
        <!-- CARD 1 -->
        <div class="grid grid-cols-2 gap-x-12">
          <div>
            <div
              class="grid grid-cols-2 gap-x-12 shadow-lg rounded-md p-4 mb-8 border border-gray-200"
            >
              <div
                class="border-b border-gray-200 py-2 mb-8 w-full text-center col-span-2"
              >
                <h2 class="text-xl font-medium">Basic Info</h2>
              </div>
              <div class="mb-8">
                <app-input v-model="variation.product_variation_code"
                  >Product Variation Code</app-input
                >
              </div>
              <div class="mb-8">
                <app-input v-model="variation.product_variation_label"
                  >Product Variation Name</app-input
                >
              </div>
              <div class="mb-8">
                <app-input
                  v-model="variation.product_variation_effective_date"
                  type="date"
                  >Effective Date</app-input
                >
              </div>
              <div class="mb-8">
                <app-input
                  v-model="variation.product_variation_expiration_date"
                  type="date"
                  >Expiration Date</app-input
                >
              </div>
            </div>

            <div
              class="grid grid-cols-2 gap-x-12 shadow-lg rounded-md p-4 mb-8 border border-gray-200"
            >
              <div
                class="border-b border-gray-200 py-2 mb-8 w-full text-center col-span-2"
              >
                <h2 class="text-xl font-medium">Rating</h2>
              </div>
              <div
                class="col-span-2 grid grid-cols-2 gap-x-12 gap-y-4 pb-8 mb-8 border-b border-gray-200"
              >
                <div class="">
                  <app-switch v-model="variation.is_age_rated"
                    >Age Rated</app-switch
                  >
                </div>
                <div class="">
                  <app-switch v-model="variation.is_gender_rated"
                    >Gender Rated</app-switch
                  >
                </div>
                <div class="">
                  <app-switch v-model="variation.is_tobacco_rated"
                    >Smoker Rated</app-switch
                  >
                </div>
                <div class="">
                  <app-switch v-model="variation.is_family_code_rated"
                    >Family Code Rated</app-switch
                  >
                </div>
              </div>
              <div
                class="col-span-2 grid grid-cols-2 gap-x-12 gap-y-4 pb-8 mb-8 border-b border-gray-200"
              >
                <div class="">
                  <app-switch
                    v-model="variation.vary_by_gender"
                    :disabled="!variation.is_gender_rated"
                    >Vary by Gender</app-switch
                  >
                </div>
                <div class="">
                  <app-switch
                    v-model="variation.vary_by_tobacco"
                    :disabled="!variation.is_tobacco_rated"
                    >Vary by Smoker</app-switch
                  >
                </div>
              </div>
            </div>
          </div>
          <!-- CARD 3 -->
          <div>
            <div class="shadow-lg rounded-md mb-8 p-4 border border-gray-200">
              <div
                class="border-b border-gray-200 py-2 mb-8 w-full text-center col-span-2"
              >
                <h2 class="text-xl font-medium">Distributions</h2>
              </div>
              <div
                class="grid grid-cols-2 gap-x-12 pb-8 mb-12 border-b border-gray-200"
              >
                <div class="col-start-1">
                  <app-input
                    v-model.number="variation.min_issue_age"
                    type="number"
                  >
                    Min Issue Age
                  </app-input>
                </div>
                <div class="">
                  <app-input
                    v-model.number="variation.max_issue_age"
                    type="number"
                    >Max Issue Age</app-input
                  >
                </div>
              </div>
              <div class="mb-8">
                <app-select
                  v-model.number="variation.age_distribution_set_id"
                  :items="options_age_distributions"
                  item_text="age_distribution_set_label"
                  item_value="age_distribution_set_id"
                  >Age Distribution</app-select
                >
              </div>
              <div class="mb-8">
                <app-select
                  v-model.number="variation.unisex_distribution_set_id"
                  :items="options_gender_distributions"
                  item_text="attr_distribution_set_label"
                  item_value="attr_distribution_set_id"
                  >Unisex Distribution</app-select
                >
              </div>
              <div class="mb-8 pb-8 border-b border-gray-200">
                <app-select
                  v-model.number="variation.unismoker_distribution_set_id"
                  :items="options_smoker_distributions"
                  item_text="attr_distribution_set_label"
                  item_value="attr_distribution_set_id"
                  >Unismoker Distribution</app-select
                >
              </div>
              <div class="mt-12 mb-8">
                <app-select
                  v-model.number="variation.sex_distinct_distribution_set_id"
                  :items="
                    options_gender_distributions.filter(
                      (item) => item.is_composite_default_dist
                    )
                  "
                  item_text="attr_distribution_set_label"
                  item_value="attr_distribution_set_id"
                  >Sex Distinct Distribution</app-select
                >
              </div>
              <div class="mb-8">
                <app-select
                  v-model.number="variation.smoker_distinct_distribution_set_id"
                  :items="
                    options_smoker_distributions.filter(
                      (item) => item.is_composite_default_dist
                    )
                  "
                  item_text="attr_distribution_set_label"
                  item_value="attr_distribution_set_id"
                  >Smoker Distinct Distribution</app-select
                >
              </div>
            </div>
          </div>
        </div>
      </template>

      <template #actions>
        <div class="flex justify-center">
          <app-button class="mx-3" @click="save">Save</app-button>
          <app-button class="mx-3" :transparent="true" @click="cancel"
            >Cancel</app-button
          >
        </div>
      </template>
    </app-form-card>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import { Model_ConfigProductVariation } from "@/models/Model_ConfigProductVariation.js";

export default {
  name: "Config_ProductVariation",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    product_variation_id: {
      required: false,
      type: [Number, String],
    },
  },
  mounted() {
    this.loaded = false;
    let p_variation;
    if (this.product_variation_id) {
      p_variation = axios.get(
        `/config/product-variations/${this.product_variation_id}`
      );
    } else {
      p_variation = new Promise((resolve, reject) => {
        resolve({ data: {} });
      });
    }

    const p_age_dist = axios.get(`/qry-config/age-distribution-sets`);
    const p_smoker_dist = axios.get(
      `/qry-config/attr-distribution-sets?attr_code=smoker_status`
    );
    const p_gender_dist = axios.get(
      `/qry-config/attr-distribution-sets?attr_code=gender`
    );
    Promise.all([p_variation, p_age_dist, p_smoker_dist, p_gender_dist])
      .then(([variation, age_dist, smoker_dist, gender_dist]) => {
        const prod_var = { ...variation.data };
        this.options_age_distributions = [...age_dist.data];
        this.options_smoker_distributions = [...smoker_dist.data];
        this.options_gender_distributions = [...gender_dist.data];

        this.variation = { ...this.modelSetter(prod_var) };
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
          label: "All Variations",
          id: "landing",
          to: "config-product-variations",
        },
        {
          label: "Configure",
          id: "configure",
          disabled: true,
        },
        {
          label: "Age Bands",
          id: "age_bands",
          disabled: true,
        },
      ],
      variation: {},
      options_age_distributions: [],
      options_smoker_distributions: [],
      options_gender_distributions: [],
    };
  },
  computed: {
    stages() {
      return this._stages
        .filter((item) => {
          if (this.$route.params.benefit_id) {
            return item.id !== "benefits";
          } else {
            return item.id !== "benefit";
          }
        })
        .map((item) => ({
          ...item,
          active: item.id === this.active_stage,
        }));
    },
    output() {
      return this.modelSetter(this.variation);
    },
  },
  methods: {
    cancel() {
      if (this.$route.params.product_variation_id) {
        this.routeTo("config-product-variations-landing");
      } else {
        this.routeTo("config-product-variations");
      }
    },
    modelSetter(data) {
      return new Model_ConfigProductVariation(
        this.product_variation_id,
        this.product_id,
        data.product_variation_code,
        data.product_variation_label,
        data.product_variation_effective_date,
        data.product_variation_expiration_date,
        data.is_gender_rated,
        data.is_age_rated,
        data.is_tobacco_rated,
        data.is_family_code_rated,
        data.family_code_rating_algorithm_code,
        data.min_issue_age,
        data.max_issue_age,
        data.unismoker_distribution_set_id,
        data.unisex_distribution_set_id,
        data.age_distribution_set_id,
        data.smoker_distinct_distribution_set_id,
        data.sex_distinct_distribution_set_id,
        data.vary_by_gender,
        data.vary_by_tobacco
      );
    },
    routeTo(route_name, params = {}, query = {}) {
      this.$router.push({
        name: route_name,
        params: {
          product_id: this.product_id,
          product_variation_id: this.product_variation_id,
          ...params,
        },
        query: { ...query },
      });
    },
    async save() {
      try {
        const variation = await axios.post(
          "/config/product-variations",
          this.output
        );
        this.variation = { ...variation.data };
        this.$store.commit("SET_SELECTIONS_OBJECT", this.variation);
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", "Saved to database!");

        this.routeTo("config-age-bands");
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
    toggleHandler(stage) {
      this.routeTo(stage.to);
    },
  },
};
</script>
