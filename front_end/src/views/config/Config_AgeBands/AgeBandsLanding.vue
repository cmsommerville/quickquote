<template>
  <div class="w-full bg-white shadow-xl rounded-md min-h-96 p-8">
    <app-form-header :title="title" :subtitle="subtitle" />
    <age-bands-tabs :active_stage="active_stage" />
    <div class="my-12" v-if="loaded">
      <div
        v-if="age_bands.length === 0"
        class="flex flex-col justify-center my-12"
      >
        <div class="w-1/2 h-2/3 mx-auto py-8 flex items-center">
          <shield-exclamation-icon class="w-24 h-24 text-gray-300 mr-4" />
          <div class="text-gray-400 uppercase tracking-wide">
            <p class="text-4xl font-extralight my-2">Uh oh!</p>
            <p class="font-light text-md">
              No age bands have been configured yet.
            </p>
          </div>
        </div>
        <div class="mx-auto mt-6">
          <app-button @click="configure">Create New</app-button>
        </div>
      </div>
      <div v-else class="flex justify-center flex-col my-12">
        <div class="h-96">
          <ag-grid-vue
            class="ag-theme-alpine"
            style="width: 100%; height: 100%"
            :columnDefs="columnDefs"
            @grid-ready="onGridReady"
            :rowData="rowData"
            rowSelection="single"
            @selection-changed="onGridSelectionChanged"
            @row-double-clicked="doubleClickRowHandler"
          >
          </ag-grid-vue>
        </div>
        <div class="mx-auto mt-12">
          <app-button
            class="mx-6"
            :disabled="!_selection.age_band_set_id"
            @click="configure"
            >Edit</app-button
          >
          <app-button class="mx-6" :transparent="true" @click="configure"
            >Create New</app-button
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine.css";
import AppFormHeader from "@/components/AppFormCard/AppFormHeader.vue";
import AgeBandsTabs from "./AgeBandsTabs.vue";
import { AgGridVue } from "ag-grid-vue3";
import { CONFIG_AGE_BANDS__COLUMN_DEFS } from "./config.js";
import { Model_ConfigAgeBands } from "@/models/Model_ConfigAgeBands.js";

export default {
  name: "Config_ProductVariations",
  components: {
    AgGridVue,
    AgeBandsTabs,
    AppFormHeader,
  },
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
  },
  mounted() {
    this.loaded = false;
    const p_age_bands = axios.get(
      `/qry-config/product/${this.product_id}/all-age-bands`
    );
    const p_variations = axios.get(
      `/qry-config/all-product-variations?product_id=${this.product_id}`
    );

    const selection = new Model_ConfigAgeBands();
    this._selection = { ...selection };

    Promise.all([p_age_bands, p_variations])
      .then(([ab, vars]) => {
        this.age_bands = [...ab.data];
        this.product_variations = [...vars.data];

        this.loaded = true;
      })
      .catch((err) => {
        this.loaded = true;
      });
  },
  data() {
    return {
      loaded: false,
      title: "Age Bands",
      subtitle: "Create a new age band or edit an existing one!",
      active_stage: "landing",
      age_bands: [],
      product_variations: [],
      _selection: {},
      columnDefs: [...CONFIG_AGE_BANDS__COLUMN_DEFS],
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
    activeStageSetter(stage_name) {
      console.log(stage_name);
      this.active_stage = stage_name;
    },
    toggleHandler(stage) {
      if (!!stage.tab) {
        this.active_stage = stage.id;
      } else {
        this.routeTo(stage.to);
      }
    },
    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;
    },
    onGridSelectionChanged() {
      this._selection = this.gridApi.getSelectedRows()[0];
    },
    doubleClickRowHandler() {
      const selection = this.gridApi.getSelectedRows()[0];
      this.$store.commit("SET_SELECTIONS_OBJECT", selection);
      if (this._selection.age_band_set_id) {
        this.routeTo(
          "config-age-band",
          {},
          { age_band_set_id: this._selection.age_band_set_id }
        );
      } else {
        this.routeTo("config-age-band");
      }
    },
    configure() {
      this.$store.commit("SET_SELECTIONS_OBJECT", this._selection);
      if (this._selection.age_band_set_id) {
        this.routeTo(
          "config-age-band",
          {},
          { age_band_set_id: this._selection.age_band_set_id }
        );
      } else {
        this.routeTo("config-age-band");
      }
    },
  },
  computed: {
    rowData() {
      return this.age_bands.map((item) => {
        return {
          ...item,
          product_variation_code: item.product_variation.product_variation_code,
          product_variation_label:
            item.product_variation.product_variation_label,
          state_code: item.state.state_code,
          state_name: item.state.state_name,
        };
      });
    },
  },
};
</script>
