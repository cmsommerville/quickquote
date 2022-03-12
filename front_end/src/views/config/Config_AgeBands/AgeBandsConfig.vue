<template>
  <div class="w-full bg-white shadow-xl rounded-md min-h-96 p-8">
    <app-form-header :title="title" :subtitle="subtitle" />
    <app-form-tabs :stages="stages" @toggle:stage="toggleHandler" />
    <div class="my-12" v-if="loaded">
      <div class="flex justify-center flex-col">
        <div class="grid grid-cols-3 gap-8 my-4">
          <div class="col-span-2 p-2 border-l-8 border-gray-200">
            <app-age-band-selector
              :input_data="_selection.age_bands"
              @change:bands="ageBandHandler"
            />
          </div>
          <div class="flex flex-col pr-8">
            <div class="w-full my-6">
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
            <div class="w-full my-6" v-if="age_band_set_id">
              <app-input
                v-model="states[0].state_name"
                :disabled="true"
                :top="true"
                >State</app-input
              >
            </div>
            <div class="w-full my-6">
              <app-input
                v-model="_selection.age_band_effective_date"
                :disabled="!!age_band_set_id"
                type="date"
                :top="true"
                >Effective Date</app-input
              >
            </div>
            <div class="w-full my-6">
              <app-input
                v-model="_selection.age_band_expiration_date"
                :disabled="!!age_band_set_id"
                type="date"
                :top="true"
                >Expiration Date</app-input
              >
            </div>
            <div v-if="!age_band_set_id" class="flex justify-center">
              <config-age-bands-states-modal
                :fab="true"
                :transparent="true"
                @add:states="addStatesHandler"
                class="p-4 h-16 w-16 flex justify-center items-center"
              />
            </div>
          </div>
        </div>
        <div class="mx-auto mt-6 flex">
          <app-button class="mx-8" @click="save">Save</app-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import AppFormHeader from "@/components/AppFormCard/AppFormHeader.vue";
import AppFormTabs from "@/components/AppFormCard/AppFormTabs.vue";
import AppAgeBandSelector from "@/components/AppAgeBandSelector.vue";
import ConfigAgeBandsStatesModal from "./AgeBandsStatesModal.vue";
import { Model_ConfigAgeBands } from "@/models/Model_ConfigAgeBands.js";

export default {
  name: "Config_AgeBandSet",
  components: {
    AppAgeBandSelector,
    AppFormTabs,
    AppFormHeader,
    ConfigAgeBandsStatesModal,
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
    let age_band_set;
    if (this.age_band_set_id) {
      age_band_set = await axios.get(
        `/config/age-band-set/${this.age_band_set_id}`
      );
      this._selection = { ...this.modelSetter(age_band_set.data) };
      this.states = [{ ...age_band_set.data.state }];
    } else {
      this._selection = this.modelSetter(age_band_set);
    }

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
      _stages: [
        {
          label: "Back to Product",
          id: "product",
          to: "config-product",
        },
        {
          label: "Age Bands",
          id: "landing",
          to: "config-age-bands",
        },
        {
          label: "Configure",
          id: "configure",
          disabled: true,
        },
      ],
      _selection: {},
      age_bands: [],
      product_variations: [],
      states: [],
    };
  },
  methods: {
    addStatesHandler(states) {
      this.states = [...states];
    },
    modelSetter(data) {
      return new Model_ConfigAgeBands(
        data.age_band_set_id ?? null,
        data.product_variation_id ?? null,
        data.state_id ?? null,
        data.age_band_effective_date ?? null,
        data.age_band_expiration_date ?? null,
        data.age_bands ?? null
      );
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
    ageBandHandler(bands) {
      this._selection.age_bands = [...bands];
    },
    configure() {
      this.routeTo("config-age-band-states");
    },
    async save() {
      try {
        const res = await axios.post(`/config/age-band-sets`, this.output);

        this.$store.dispatch("SET_SNACKBAR_MESSAGE", "Updated age bands");
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
  },
  computed: {
    output() {
      return this.states.map((state) => {
        return this.modelSetter({
          ...this._selection,
          state_id: state.state_id,
        });
      });
    },
    stages() {
      return this._stages.map((item) => ({
        ...item,
        active: item.id === this.active_stage,
      }));
    },
    subtitle() {
      return this.age_band_set_id
        ? "Let's make some changes..."
        : "Let's create a new age band!";
    },
  },
};
</script>
