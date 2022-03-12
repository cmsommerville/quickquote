<template>
  <app-modal ref="modal" v-bind="$attrs" @close:modal="$emit('close:modal')">
    <template #header>Edit Age Distribution</template>
    <template #content="contentProps">
      <div class="min-w-[48rem]">
        <div class="flex flex-col">
          <div class="mt-8 lg:w-72">
            <app-input v-model="modelValue.age_distribution_set_label">
              Label
            </app-input>
          </div>
          <div
            v-if="!modelValue.age_distribution"
            class="mt-6 grid grid-cols-3 gap-8"
          >
            <div class="mt-2 lg:w-72">
              <app-input v-model.number="min_age"> Minimum Age </app-input>
            </div>
            <div class="mt-2 lg:w-72">
              <app-input v-model.number="max_age"> Maximum Age </app-input>
            </div>
            <div class="mt-2 lg:w-72">
              <app-input v-model.number="step"> Step Size </app-input>
            </div>
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
import { CONFIG_AGE_DISTRIBUTION__COLUMN_DEFS } from "./config.js";
import { Model_ConfigAgeDistribution } from "@/models/Model_ConfigDistributions.js";

export default {
  name: "Config_AgeDistribution_Modal",
  components: { AppModal, AgGridVue },
  props: {
    modelValue: {
      required: false,
      type: Object,
    },
  },
  data() {
    return {
      min_age: 17,
      max_age: 99,
      step: 1,
      columnDefs: [...CONFIG_AGE_DISTRIBUTION__COLUMN_DEFS],
    };
  },
  methods: {
    initialize() {
      this.min_age = 17;
      this.max_age = 99;
      this.step = 1;
    },
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
        const output = new Model_ConfigAgeDistribution(
          item.age_distribution_id,
          item.age,
          item.weight
        );
        return { ...output };
      });
      return {
        ...this.modelValue,
        age_distribution: [...d],
      };
    },
    rowData() {
      if (this.modelValue?.age_distribution) {
        return this.modelValue.age_distribution;
      }
      return Array.from(
        { length: (this.max_age - this.min_age) / this.step + 1 },
        (v, k) => ({
          age: this.step * k + this.min_age,
          weight: null,
        })
      );
    },
  },
};
</script>

<style></style>
