<template>
  <div>
    <app-form-card
      :stages="stages"
      :title="title"
      :subtitle="subtitle"
      :tabbed="true"
      @toggle:stage="toggleHandler"
      @input:variation="inputHandler"
    >
      <template #content>
        <product-variations-landing
          v-if="active_stage === 'product_variations'"
          :product_variations="product_variations"
          :setter="inputHandler"
        />
        <product-variation-config
          v-if="active_stage === 'product_variation_config'"
          :selection="selection"
        />
      </template>

      <template #actions>
        <div class="flex justify-center">
          <app-button
            class="mx-3"
            :disabled="!selection"
            @click="
              routeTo('config-product-variation-config', {
                product_variation_id: selection.product_variation_id,
              })
            "
            >Next</app-button
          >
          <app-button
            v-if="selection && selection.product_variation_id"
            class="mx-3"
            :transparent="true"
            >Edit</app-button
          >
        </div>
      </template>
    </app-form-card>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import ProductVariationsLanding from "./ProductVariationsLanding.vue";
import ProductVariationConfig from "./ProductVariationConfig.vue";
import Model_ConfigProductVariation from "@/models/Model_ConfigProductVariation.js";

export default {
  name: "Config_ProductVariations",
  components: { ProductVariationsLanding, ProductVariationConfig },
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
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      title: "Add Some Variations",
      subtitle: "",
      active_stage: "product_variations",
      _stages: [
        { label: "Product", id: "product", to: "config-product" },
        {
          label: "Variations",
          id: "product_variations",
          tabbed: true,
        },
        {
          label: "Config",
          id: "product_variation_config",
          tabbed: true,
        },
        {
          label: "Age Bands",
          id: "config-age-bands",
          to: "config-age-bands",
        },
      ],
      product_variations: [],
      selection: {},
    };
  },
  watch: {
    selection(newVal) {
      this.$store.commit("");
    },
  },
  computed: {
    stages() {
      return this._stages.map((stg) => {
        return { ...stg, active: this.active_stage === stg.id };
      });
    },
  },
  methods: {
    inputHandler(data) {
      console.log(data);
      this.selection = { ...this.selection, ...data };
    },
    formatDateText(input_dt) {
      const dt = new Date(input_dt);
      const dtDateOnly = new Date(
        dt.valueOf() + dt.getTimezoneOffset() * 60 * 1000
      );
      return format(dtDateOnly, "M/d/yyyy");
    },
    routeTo(route_name, params = {}, query = {}) {
      this.$router.push({
        name: route_name,
        params: { product_id: this.product_id, ...params },
        query: { ...query },
      });
    },
    toggleHandler(id) {
      const stage = this.stages.find((stg) => stg.id === id);
      if (!!stage.tabbed) {
        this.active_stage = stage.id;
      } else {
        this.routeTo(stage.to);
      }
    },
  },
};
</script>
