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
            :disabled_edit="!_selection.attr_distribution_set_id"
            :disabled_delete="!_selection.attr_distribution_set_id"
            @fab:new="newHandler"
            @fab:edit="editHandler"
            @fab:delete="deleteHandler"
          />
          <config-gender-distribution-modal
            class="hidden"
            ref="modal"
            v-model="_selection"
            @update:modelValue="addDistributionHandler"
            @close:modal="show_fab = false"
          ></config-gender-distribution-modal>
        </div>
        <div class="mx-auto mt-12">
          <app-button class="mx-6" @click="save">Save</app-button>
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
import ConfigGenderDistributionModal from "./Config_GenderDistribution_Modal.vue";
import { AgGridVue } from "ag-grid-vue3";
import { CONFIG_GENDER_DISTRIBUTION_LIST__COLUMN_DEFS } from "./config.js";
import { Model_ConfigAttrDistributionSet } from "@/models/Model_ConfigDistributions.js";

export default {
  name: "Config_AgeDistributionList",
  components: {
    AgGridVue,
    AppFormTabs,
    AppFormHeader,
    AppNewEditDeleteButton,
    AppModal,
    ConfigGenderDistributionModal,
  },
  props: {},
  async mounted() {
    this.loaded = false;
    const res = await axios.get(
      `/qry-config/attr-distribution-sets?attr_code=gender`
    );

    this.distributions = [
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
      title: "Gender Distributions",
      subtitle: "Create a new distribution or edit an existing one!",
      active_stage: "gender",
      _stages: [
        {
          label: "All Distributions",
          id: "landing",
          to: "config-distribution-list",
        },
        {
          label: "Gender Distributions",
          id: "gender",
          disabled: true,
        },
      ],
      distributions: [],
      columnDefs: [...CONFIG_GENDER_DISTRIBUTION_LIST__COLUMN_DEFS],
      _selection: {},
    };
  },
  methods: {
    addDistributionHandler(data) {
      this.distributions = [
        ...this.distributions.filter((dist) => {
          return (
            dist.attr_distribution_set_id == null ||
            dist.attr_distribution_set_id !== data.attr_distribution_set_id
          );
        }),
        { ...data, _id: (Math.random() + 1).toString(36).substring(4) },
      ];
    },
    async deleteHandler() {
      if (this._selection.attr_distribution_set_id) {
        await axios.delete(
          `/config/attr-distribution-set/${this._selection.attr_distribution_set_id}`
        );
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", "Deleted from DB");
      }
      this.distributions = [
        ...this.distributions.filter((item) => {
          item._id !== this._selection._id;
        }),
      ];
    },
    doubleClickRowHandler() {
      this._selection = this.gridApi.getSelectedRows()[0];
      this.$refs.modal.open();
    },
    editHandler() {
      this.$refs.modal.open();
    },
    modelSetter(data) {
      const dist = new Model_ConfigAttrDistributionSet(
        data.attr_distribution_set_id,
        data.attr_distribution_set_label,
        "gender",
        data.attr_distribution
      );
      return dist;
    },
    newHandler() {
      this._selection = {
        attr_distribution: [{ attr_value: "M" }, { attr_value: "F" }],
      };
      this.$refs.modal.initialize();
      this.$refs.modal.open();
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
        params: { ...params },
        query: { ...query },
      });
    },
    async save() {
      try {
        const res = await axios.post(
          "/config/attr-distribution-sets",
          this.output
        );
        this.distributions = [...res.data];
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
      if (this.distributions.length > 0) {
        return this.distributions.map((dist) => {
          return this.modelSetter(dist);
        });
      }
      return [];
    },
    rowData() {
      return this.distributions.map((item) => {
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
