<template>
  <app-form-card
    :title="title"
    :subtitle="subtitle"
    :stages="stages"
    @toggle:stage="toggleHandler"
  >
    <template #content>
      <div class="my-12" v-if="loaded">
        <div class="flex justify-center flex-col my-12">
          <div class="h-72 w-2/3 mx-auto">
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
        </div>
      </div>
    </template>
    <template #actions>
      <div class="flex justify-center">
        <div class="flex justify-center mx-4">
          <app-button
            :disabled="!_selection.benefit_duration_id"
            @click="editHandler"
            >Edit</app-button
          >
        </div>
        <div class="flex justify-center mx-4">
          <app-button :transparent="true" @click="newHandler"
            >Create New</app-button
          >
        </div>
      </div>
    </template>
  </app-form-card>
</template>

<script>
import axios from "@/services/axios.js";
import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine.css";
import AppFormCard from "@/components/AppFormCard/AppFormCard.vue";
import { AgGridVue } from "ag-grid-vue3";
import { CONFIG_BENEFIT_DURATIONS_LIST__COLUMN_DEFS } from "./config.js";

export default {
  name: "Config_BenefitDurationsList",
  components: { AppFormCard, AgGridVue },
  props: {
    benefit_id: {
      required: true,
      type: [Number, String],
    },
    product_id: {
      required: true,
      type: [Number, String],
    },
  },
  async mounted() {
    this.loaded = false;
    await this.loadDurations();
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      title: "Benefit Durations",
      subtitle: "Create a new benefit duration or edit an existing one!",
      active_stage: "durations",
      _stages: [
        {
          label: "Back to Benefit",
          id: "benefit",
          to: "config-benefit-landing",
        },
        {
          label: "Durations",
          id: "durations",
          disabled: true,
        },
      ],
      durations: [],
      columnDefs: [...CONFIG_BENEFIT_DURATIONS_LIST__COLUMN_DEFS],
      _selection: {},
    };
  },
  methods: {
    doubleClickRowHandler() {
      this._selection = this.gridApi.getSelectedRows()[0];
      this.editHandler();
    },
    editHandler() {
      this.routeTo(
        "config-benefit-duration",
        {},
        { duration_id: this._selection.benefit_duration_id }
      );
    },
    async loadDurations() {
      const res = await axios.get(
        `/qry-config/all-benefit-durations?benefit_id=${this.benefit_id}`
      );
      this.durations = [...res.data];
    },
    newHandler() {
      this.routeTo("config-benefit-duration");
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
          benefit_id: this.benefit_id,
          ...params,
        },
        query: {
          ...query,
        },
      });
    },
    toggleHandler(stg) {
      this.routeTo(stg.to);
    },
  },
  computed: {
    rowData() {
      return this.durations.map((item) => {
        return {
          ...item,
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

<style></style>
