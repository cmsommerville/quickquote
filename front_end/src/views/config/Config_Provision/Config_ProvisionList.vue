<template>
  <div class="w-full bg-white shadow-xl rounded-md min-h-96 p-8">
    <app-form-header :title="title" :subtitle="subtitle" />
    <app-form-tabs :stages="stages" @toggle:stage="toggleHandler" />
    <div class="my-12" v-if="loaded">
      <div class="flex justify-center flex-col my-12">
        <div class="h-72 w-full mx-auto">
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
          <app-button class="mx-6" @click="configure">Edit</app-button>
          <app-button
            class="mx-6"
            :transparent="true"
            @click="newBenefitHandler"
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
import AppFormTabs from "@/components/AppFormCard/AppFormTabs.vue";
import { AgGridVue } from "ag-grid-vue3";
import { CONFIG_PROVISION_LIST__COLUMN_DEFS } from "./config.js";

export default {
  name: "Config_ProvisionList",
  components: {
    AgGridVue,
    AppFormTabs,
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
      `/qry-config/all-provisions?product_id=${this.product_id}`
    );

    this.provisions = [...res.data];
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      title: "Provisions",
      subtitle: "Create a new provision or edit an existing one!",
      active_stage: "landing",
      _stages: [
        {
          label: "Back to Product",
          id: "product",
          to: "config-product",
        },
        {
          label: "All Provisions",
          id: "landing",
          disabled: true,
        },
        {
          label: "Configure",
          id: "configure",
          disabled: true,
        },
      ],
      provisions: [],
      columnDefs: [...CONFIG_PROVISION_LIST__COLUMN_DEFS],
      _selection: {},
    };
  },
  methods: {
    configure() {
      this.routeTo("config-provision-landing", {
        provision_id: this._selection.provision_id,
      });
    },
    doubleClickRowHandler() {
      this._selection = this.gridApi.getSelectedRows()[0];
      this.configure();
    },
    newBenefitHandler() {
      this.routeTo("config-provision-new");
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
        params: { product_id: this.product_id, ...params },
        query: { ...query },
      });
    },
    toggleHandler(stg) {
      this.routeTo(stg.to);
    },
  },
  computed: {
    rowData() {
      return this.provisions.map((item) => {
        return {
          ...item,
          state_count: item.states.length ?? 0,
          factor_count: item.factors.length ?? 0,
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
