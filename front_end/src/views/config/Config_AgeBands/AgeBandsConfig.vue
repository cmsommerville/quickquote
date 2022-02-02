<template>
  <div class="w-full bg-white shadow-xl rounded-md min-h-96 p-8">
    <app-form-header :title="title" :subtitle="subtitle" />
    <age-bands-tabs :active_stage="active_stage" />
    <div class="my-12" v-if="loaded">
      <div class="flex justify-center flex-col">
        <div class="grid grid-cols-3 gap-8 my-4">
          <div class="col-span-2 p-2 border-l-8 border-gray-200">
            <app-age-band-selector
              :input_data="_selection.age_bands"
              @change:bands="ageBandHandler"
            />
          </div>
          <div class="flex flex-col">
            <div class="w-60 my-6">
              <app-select
                v-model="_selection.product_variation_id"
                :disabled="!!age_band_set_id"
                :items="product_variations"
                item_text="product_variation_label"
                item_value="product_variation_id"
                :top="true"
                >Product Variation</app-select
              >
            </div>
            <div class="w-60 my-6" v-if="age_band_set_id">
              <app-input
                v-model="_selection.state.state_name"
                :disabled="true"
                :top="true"
                >State</app-input
              >
            </div>
            <div class="w-60 my-6">
              <app-input
                v-model="_selection.age_band_effective_date"
                :disabled="!!age_band_set_id"
                type="date"
                :top="true"
                >Effective Date</app-input
              >
            </div>
            <div class="w-60 my-6">
              <app-input
                v-model="_selection.age_band_expiration_date"
                :disabled="!!age_band_set_id"
                type="date"
                :top="true"
                >Expiration Date</app-input
              >
            </div>
          </div>
        </div>
        <div class="mx-auto mt-6">
          <app-button v-if="!age_band_set_id" @click="configure"
            >States</app-button
          >
          <app-button v-else @click="save">Save</app-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import AppFormHeader from "@/components/AppFormCard/AppFormHeader.vue";
import AgeBandsTabs from "./AgeBandsTabs.vue";
import AppAgeBandSelector from "@/components/AppAgeBandSelector.vue";
import { Model_ConfigAgeBands } from "@/models/Model_ConfigAgeBands.js";

export default {
  name: "Config_ProductVariations",
  components: {
    AppAgeBandSelector,
    AgeBandsTabs,
    AppFormHeader,
  },
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    age_band_set_id: {
      default: null,
      type: [Number, String, null],
    },
  },
  async mounted() {
    this.loaded = false;
    this._selection = { ...this.$store.getters.get_selections_object };
    const variations = await axios.get(
      `/qry-config/all-product-variations?product_id=${this.product_id}`
    );
    this.product_variations = [...variations.data];
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      title: "Age Bands",
      active_stage: "configure",
      _selection: {},
      age_bands: [],
      product_variations: [],
    };
  },
  methods: {
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
    ageBandHandler(bands) {
      this._selection.age_bands = [...bands];
    },
    configure() {
      this.$store.commit("SET_SELECTIONS_OBJECT", this._selection);
      this.routeTo("config-age-band-states");
    },
    async save() {
      try {
        const res = await axios.put(
          `/config/age-band-set/${this.age_band_set_id}`,
          this.output
        );
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", "Updated age bands");
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
  },
  computed: {
    subtitle() {
      return this.age_band_set_id
        ? "Let's make some changes..."
        : "Let's create a new age band!";
    },
    output() {
      const age_band_set = new Model_ConfigAgeBands(
        this._selection.product_variation_id,
        this._selection.state_id,
        this._selection.age_band_effective_date,
        this._selection.age_band_expiration_date,
        this._selection.age_bands
      );

      if (this.age_band_set_id)
        age_band_set.set_age_band_set_id(this.age_band_set_id);

      return age_band_set;
    },
  },
};
</script>
