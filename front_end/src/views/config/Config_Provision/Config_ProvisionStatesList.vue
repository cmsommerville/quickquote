<template>
  <div class="w-full bg-white shadow-xl rounded-md min-h-96 p-8">
    <app-form-header :title="title" :subtitle="subtitle" />
    <app-form-tabs :stages="stages" @toggle:stage="toggleHandler" />
    <div class="my-12" v-if="loaded">
      <div class="flex justify-center flex-col my-12">
        <div class="h-72 w-4/5 mx-auto">
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
        <div class="mx-auto mt-12 flex items-center">
          <config-new-provision-states-modal
            class="mx-4"
            :provision="provision"
            @close:modal="loadProvision"
          />
          <config-edit-provision-states-modal
            ref="editProvision"
            class="mx-4"
            :disabled="!_selection.provision_id"
            :transparent="true"
            :provision_state="_selection"
            :provision_code="provision.provision_code"
            @close:modal="loadProvision"
          />
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
import ConfigNewProvisionStatesModal from "./Config_NewProvisionStates_Modal.vue";
import ConfigEditProvisionStatesModal from "./Config_EditProvisionStates_Modal.vue";
import { AgGridVue } from "ag-grid-vue3";
import { CONFIG_PROVISION_STATES_LIST__COLUMN_DEFS } from "./config.js";

export default {
  name: "Config_ProvisionStatesList",
  components: {
    AgGridVue,
    AppFormTabs,
    AppFormHeader,
    ConfigNewProvisionStatesModal,
    ConfigEditProvisionStatesModal,
  },
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    provision_id: {
      required: true,
      type: [Number, String],
    },
  },
  async mounted() {
    this.loaded = false;
    await this.loadProvision();
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
          label: "Back to Provision",
          id: "provision",
          to: "config-provision-landing",
        },
        {
          label: "States",
          id: "landing",
          disabled: true,
        },
      ],
      provision: {},
      columnDefs: [...CONFIG_PROVISION_STATES_LIST__COLUMN_DEFS],
      _selection: {},
    };
  },
  methods: {
    doubleClickRowHandler() {
      this._selection = this.gridApi.getSelectedRows()[0];
      this.$refs.editProvision.open();
    },
    async loadProvision() {
      const res = await axios.get(`/config/provision/${this.provision_id}`);
      this.provision = { ...res.data };
    },
    routeTo(route_name, params = {}, query = {}) {
      this.$router.push({
        name: route_name,
        params: {
          product_id: this.product_id,
          provision_id: this.provision_id,
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
    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;
    },
    onGridSelectionChanged() {
      this._selection = this.gridApi.getSelectedRows()[0];
    },
  },
  computed: {
    rowData() {
      return this.provision.states.map((item) => {
        return {
          ...item,
          provision_code: this.provision.provision_code,
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
