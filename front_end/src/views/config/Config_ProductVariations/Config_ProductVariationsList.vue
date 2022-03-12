<template>
  <div class="w-full bg-white shadow-xl rounded-md min-h-96 p-8">
    <app-form-header :title="title" :subtitle="subtitle" />
    <app-form-tabs :stages="stages" @toggle:stage="toggleHandler" />
    <div class="my-12" v-if="loaded">
      <div class="flex justify-center flex-col my-12">
        <div class="h-72 w-full mx-auto relative">
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
            :disabled_edit="!_selection.product_variation_id"
            :disabled_delete="!_selection.product_variation_id"
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
import AppModal from "@/components/AppModal.vue";
import AppNewEditDeleteButton from "@/components/AppNewEditDeleteButton.vue";
import { AgGridVue } from "ag-grid-vue3";
import { CONFIG_PRODUCT_VARIATIONS_LIST__COLUMN_DEFS } from "./config.js";

export default {
  name: "Config_ProductVariationsList",
  components: {
    AgGridVue,
    AppFormTabs,
    AppFormHeader,
    AppModal,
    AppNewEditDeleteButton,
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

    this.variations = [
      ...res.data.map((item) => {
        return { ...item, _id: (Math.random() + 1).toString(36).substring(4) };
      }),
    ];
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      show_fab: false,
      title: "Product Variations",
      subtitle: "Create a new variation or edit an existing one!",
      active_stage: "variations",
      _stages: [
        {
          label: "Back to Product",
          id: "product",
          to: "config-product",
        },
        {
          label: "Variations",
          id: "variations",
          disabled: true,
        },
        {
          label: "Configure",
          id: "configure",
          disabled: true,
        },
      ],
      variations: [],
      columnDefs: [...CONFIG_PRODUCT_VARIATIONS_LIST__COLUMN_DEFS],
      _selection: {},
    };
  },
  methods: {
    addDistributionHandler(data) {
      this.variations = [
        ...this.variations.filter((dist) => {
          return (
            dist.product_variation_id == null ||
            dist.product_variation_id !== data.product_variation_id
          );
        }),
        { ...data, _id: (Math.random() + 1).toString(36).substring(4) },
      ];
    },
    async deleteHandler() {
      if (this._selection.product_variation_id) {
        await axios.delete(
          `/config/age-distribution-set/${this._selection.product_variation_id}`
        );
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", "Deleted from DB");
      }
      this.distributions = [
        ...this.variations.filter((item) => {
          item._id !== this._selection._id;
        }),
      ];
    },
    doubleClickRowHandler() {
      this._selection = this.gridApi.getSelectedRows()[0];
      this.routeTo("config-product-variation", {
        product_variation_id: this._selection.product_variation_id,
      });
    },
    editHandler() {
      this.routeTo("config-product-variation", {
        product_variation_id: this._selection.product_variation_id,
      });
    },
    newHandler() {
      this._selection = {};
      this.routeTo("config-product-variation");
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
    async save() {
      try {
        const res = await axios.post("/config/product-variations", this.output);
        this.variations = [...res.data];
        this.$store.dispatch(
          "SET_SNACKBAR_MESSAGE",
          "Successfully added data to DB"
        );
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
    toggleHandler(stg) {
      this.routeTo(stg.to);
    },
  },
  computed: {
    output() {
      if (this.variations.length > 0) {
        return this.variations.map((v) => {
          return v; //this.modelSetter(dist);
        });
      }
      return [];
    },
    rowData() {
      return this.variations.map((item) => {
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
