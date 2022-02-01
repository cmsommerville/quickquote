<template>
  <div>
    <div v-if="age_bands.length === 0" class="flex flex-col justify-center">
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
        <app-button @click="clickHandler">Create New</app-button>
      </div>
    </div>
    <div v-else class="flex justify-center flex-col">
      <div class="h-96">
        <ag-grid-vue
          class="ag-theme-alpine"
          style="width: 100%; height: 100%"
          :columnDefs="columnDefs"
          @grid-ready="onGridReady"
          :rowData="rowData"
          rowSelection="single"
          @selection-changed="onGridSelectionChanged"
          @row-double-clicked="doubleClickHandler"
        >
        </ag-grid-vue>
      </div>
      <div class="mx-auto mt-12">
        <app-button @click="clickHandler">Edit</app-button>
      </div>
    </div>
  </div>
</template>

<script>
import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine.css";
import { AgGridVue } from "ag-grid-vue3";

export default {
  name: "LandingAgeBands",
  components: { AgGridVue },
  props: {
    age_bands: {
      required: true,
      type: Array,
    },
  },
  data() {
    return {
      selection: null,
      columnDefs: [
        {
          headerName: "Age Band Set ID",
          field: "age_band_set_id",
          sortable: true,
          filter: true,
        },
        {
          headerName: "Variation Code",
          field: "product_variation_code",
          sortable: true,
          filter: true,
        },
        {
          headerName: "Variation Name",
          field: "product_variation_label",
          sortable: true,
          filter: true,
        },
        {
          headerName: "State Code",
          field: "state_code",
          sortable: true,
          filter: true,
        },
        {
          headerName: "State Name",
          field: "state_name",
          sortable: true,
          filter: true,
        },
        {
          headerName: "Effective Date",
          field: "age_band_effective_date",
          sortable: true,
          filter: true,
        },
        {
          headerName: "Expiration Date",
          field: "age_band_expiration_date",
          sortable: true,
          filter: true,
        },
      ],
      rowSelection: null,
    };
  },
  methods: {
    clickHandler() {
      this.$emit("click:edit", this.selection);
    },
    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;
    },
    onGridSelectionChanged() {
      this.rowSelection = this.gridApi.getSelectedRows()[0];
    },
    doubleClickHandler() {
      this.rowSelection = this.gridApi.getSelectedRows()[0];
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

<style></style>
