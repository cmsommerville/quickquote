<template>
  <app-modal ref="modal" v-bind="$attrs" @close:modal="$emit('close:modal')">
    <template #header>Edit Gender Distribution</template>
    <template #content="contentProps">
      <div class="min-w-[48rem]">
        <div class="flex flex-col">
          <div class="mt-8 lg:w-72">
            <app-input v-model="modelValue.attr_distribution_set_label">
              Label
            </app-input>
          </div>
        </div>
        <div class="h-72 w-full mx-auto mt-4">
          <ag-grid-vue
            class="ag-theme-alpine"
            style="width: 100%; height: 100%"
            :columnDefs="columnDefs"
            @grid-ready="onGridReady"
            :rowData="rowData"
            rowSelection="single"
          >
          </ag-grid-vue>
        </div>
        <div class="mt-12 mb-6 flex justify-center">
          <app-button class="mx-4" @click="save(contentProps.close)"
            >Save</app-button
          >
          <app-button @click="contentProps.close" :transparent="true"
            >Cancel</app-button
          >
        </div>
      </div>
    </template>
    <slot />
  </app-modal>
</template>

<script>
import AppModal from "@/components/AppModal.vue";
import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine.css";
import { AgGridVue } from "ag-grid-vue3";
import { CONFIG_GENDER_DISTRIBUTION__COLUMN_DEFS } from "./config.js";
import { Model_ConfigAttrDistribution } from "@/models/Model_ConfigDistributions.js";

export default {
  name: "Config_GenderDistribution_Modal",
  components: { AppModal, AgGridVue },
  props: {
    modelValue: {
      required: false,
      type: Object,
    },
  },
  data() {
    return {
      columnDefs: [...CONFIG_GENDER_DISTRIBUTION__COLUMN_DEFS],
    };
  },
  methods: {
    initialize() {},
    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;
    },
    open() {
      this.$refs.modal.openHandler();
    },
    save(callback) {
      this.$emit("update:modelValue", this.output);
      callback();
    },
  },
  computed: {
    output() {
      const d = this.rowData.map((item) => {
        const output = new Model_ConfigAttrDistribution(
          item.attr_distribution_id,
          item.attr_value,
          item.weight
        );
        return { ...output };
      });
      return {
        ...this.modelValue,
        attr_distribution: [...d],
      };
    },
    rowData() {
      return this.modelValue.attr_distribution;
    },
  },
};
</script>

<style></style>
