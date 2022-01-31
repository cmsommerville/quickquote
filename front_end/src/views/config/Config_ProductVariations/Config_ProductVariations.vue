<template>
  <div class="w-full bg-white shadow-xl rounded-md min-h-96 p-8">
    <app-form-header :title="title" :subtitle="subtitle" />
    <product-variation-tabs
      :active_stage="active_stage"
      @toggle:stage="toggleHandler"
    />
    <div class="my-12">
      <product-variations-landing
        v-if="active_stage === 'product_variations'"
        :product_variations="product_variations"
        :selection="selection"
        @input:data="inputHandler"
      />
      <product-variation-rating
        v-if="active_stage === 'product_variation_rating'"
        :selection="selection"
        @input:data="inputHandler"
      />
    </div>
    <div class="my-8">
      <div class="flex justify-center">
        <app-button
          class="mx-3"
          v-if="active_stage === 'product_variations'"
          @click="active_stage = 'product_variation_rating'"
          >Configure</app-button
        >

        <app-button
          class="mx-3"
          v-if="active_stage === 'product_variation_rating'"
          :disabled="!validate"
          @click="save"
          >Save</app-button
        >
        <app-button
          v-if="selection && selection.product_variation_id"
          class="mx-3"
          :transparent="true"
          >Edit</app-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import AppFormHeader from "@/components/AppFormCard/AppFormHeader.vue";
import ProductVariationTabs from "./ProductVariationTabs.vue";
import ProductVariationsLanding from "./ProductVariationsLanding.vue";
import ProductVariationRating from "./ProductVariationRating.vue";
import { Model_ConfigProductVariation } from "@/models/Model_ConfigProductVariation.js";

export default {
  name: "Config_ProductVariations",
  components: {
    ProductVariationsLanding,
    ProductVariationRating,
    ProductVariationTabs,
    AppFormHeader,
  },
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
  },
  async mounted() {
    this.loaded = false;
    const res = await axios.get(
      `/qry-config/all-product-variations?product_id=${this.product_id}`
    );
    this.product_variations = [...res.data];
    this.selection = new Model_ConfigProductVariation(this.product_id);
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      title: "Add Some Variations",
      subtitle: "",
      active_stage: "product_variations",
      product_variations: [],
      selection: {},
    };
  },
  computed: {
    output() {
      return new Model_ConfigProductVariation(
        this.product_id,
        this.selection.product_variation_code,
        this.selection.product_variation_label,
        this.selection.product_variation_effective_date,
        this.selection.product_variation_expiration_date,
        this.selection.is_gender_rated ?? null,
        this.selection.is_age_rated ?? null,
        this.selection.is_tobacco_rated ?? null,
        this.selection.is_family_code_rated ?? null,
        this.selection.family_code_rating_algorithm_code ?? null,
        this.selection.min_issue_age ?? null,
        this.selection.max_issue_age ?? null,
        this.selection.unismoker_distribution_set_id ?? null,
        this.selection.unisex_distribution_set_id ?? null,
        this.selection.age_distribution_set_id ?? null,
        this.selection.vary_by_gender ?? null,
        this.selection.vary_by_tobacco ?? null
      );
    },
    validate() {
      const variation = new Model_ConfigProductVariation(
        this.product_id,
        this.selection.product_variation_code,
        this.selection.product_variation_label,
        this.selection.product_variation_effective_date,
        this.selection.product_variation_expiration_date,
        this.selection.is_gender_rated ?? null,
        this.selection.is_age_rated ?? null,
        this.selection.is_tobacco_rated ?? null,
        this.selection.is_family_code_rated ?? null,
        this.selection.family_code_rating_algorithm_code ?? null,
        this.selection.min_issue_age ?? null,
        this.selection.max_issue_age ?? null,
        this.selection.unismoker_distribution_set_id ?? null,
        this.selection.unisex_distribution_set_id ?? null,
        this.selection.age_distribution_set_id ?? null,
        this.selection.vary_by_gender ?? null,
        this.selection.vary_by_tobacco ?? null
      );
      return variation.validate();
    },
  },
  methods: {
    inputHandler(data) {
      this.selection = { ...this.selection, ...data };
    },
    routeTo(route_name, params = {}, query = {}) {
      this.$router.push({
        name: route_name,
        params: { product_id: this.product_id, ...params },
        query: { ...query },
      });
    },
    toggleHandler(stage) {
      if (!!stage.tab) {
        this.active_stage = stage.id;
      } else {
        this.routeTo(stage.to);
      }
    },
    async save() {
      await axios.post("/config/product-variations", this.output);
    },
  },
};
</script>
