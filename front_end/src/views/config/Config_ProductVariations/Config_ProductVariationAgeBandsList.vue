<template>
  <div class="w-full bg-white shadow-xl rounded-md min-h-96 p-8">
    <app-form-header :title="title" :subtitle="subtitle" />
    <app-form-tabs :stages="stages" @toggle:stage="toggleHandler" />
    <div class="my-12" v-if="loaded">
      <div class="flex justify-center flex-col my-12">
        <div class="h-96 relative">
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
          <app-new-edit-delete-button
            :disabled_edit="!_selection.age_band_set_id"
            :disabled_delete="!_selection.age_band_set_id"
            @fab:new="newHandler"
            @fab:edit="editHandler"
            @fab:delete="deleteHandler"
          />
        </div>
        <div class="mx-auto mt-12">
          <app-button class="mx-6" @click="routeTo('config-product')"
            >Back</app-button
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
import AppFormTabs from "@/components/AppFormCard/AppFormTabs.vue";
import AppNewEditDeleteButton from "@/components/AppNewEditDeleteButton.vue";
import { AgGridVue } from "ag-grid-vue3";
import { CONFIG_AGE_BANDS__COLUMN_DEFS } from "../Config_AgeBands/config.js";
import { Model_ConfigAgeBands } from "@/models/Model_ConfigAgeBands.js";

export default {
  name: "Config_AgeBandsList",
  components: {
    AgGridVue,
    AppFormHeader,
    AppFormTabs,
    AppNewEditDeleteButton,
  },
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    product_variation_id: {
      required: true,
      type: [Number, String],
    },
  },
  mounted() {
    this.loaded = false;
    const p_age_bands = axios.get(
      `/qry-config/all-age-bands?product_variation_id=${this.product_variation_id}`
    );
    const selection = new Model_ConfigAgeBands();
    this._selection = { ...selection };

    Promise.all([p_age_bands])
      .then(([ab, vars]) => {
        this.age_bands = [...ab.data];
      })
      .catch((err) => {})
      .finally(() => (this.loaded = true));
  },
  data() {
    return {
      loaded: false,
      title: "Age Bands",
      subtitle: "Create a new age band or edit an existing one!",
      active_stage: "landing",
      _stages: [
        {
          label: "Back to Variation",
          id: "product_variation",
          to: "config-product-variation-landing",
        },
        {
          label: "Age Bands",
          id: "landing",
          disabled: true,
        },
        {
          label: "Configure",
          id: "configure",
          disabled: true,
        },
      ],
      age_bands: [],
      _selection: {},
      columnDefs: [...CONFIG_AGE_BANDS__COLUMN_DEFS],
    };
  },
  methods: {
    activeStageSetter(stage_name) {
      console.log(stage_name);
      this.active_stage = stage_name;
    },
    deleteHandler() {
      console.log("Delete handler");
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
    editHandler() {
      this.routeTo(
        "config-age-band",
        {},
        { age_band_set_id: this._selection.age_band_set_id }
      );
    },
    newHandler() {
      this.routeTo("config-age-band");
    },
    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;
    },
    onGridSelectionChanged() {
      this._selection = this.gridApi.getSelectedRows()[0];
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
    toggleHandler(stg) {
      this.routeTo(stg.to);
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
    stages() {
      return this._stages.map((item) => ({
        ...item,
        active: item.id === this.active_stage,
      }));
    },
  },
};
</script>
