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
            :rowDragManaged="true"
            @selection-changed="onGridSelectionChanged"
            @row-double-clicked="doubleClickRowHandler"
            @row-drag-end="priorityHandler"
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
import { CONFIG_FACTOR_LIST__COLUMN_DEFS } from "./config.js";

export default {
  name: "Config_FactorList",
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
    provision_id: {
      required: true,
      type: [Number, String],
    },
  },
  async mounted() {
    this.loaded = false;
    const res = await axios.get(
      `/qry-config/factors?provision_id=${this.provision_id}`
    );

    this.factors = [...res.data];
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      title: "Factors",
      subtitle: "Create a new factor or edit an existing one!",
      active_stage: "factors",
      _stages: [
        {
          label: "Back to Provision",
          id: "provision",
          to: "config-provision-landing",
        },
        {
          label: "Factors",
          id: "factors",
          disabled: true,
        },
      ],
      factors: [],
      columnDefs: [...CONFIG_FACTOR_LIST__COLUMN_DEFS],
      _selection: {},
    };
  },
  methods: {
    priorityHandler() {
      const data = [];
      this.gridApi.forEachNode(function (row, index) {
        data.push({ ...row.data, factor_priority: index });
      });
      this.factors = [
        ...data.map((f, ix) => {
          return { ...f, factor_priority: ix };
        }),
      ];
    },
    configure() {
      this.routeTo(
        "config-factor",
        {},
        {
          factor_id: this._selection.factor_id,
        }
      );
    },
    doubleClickRowHandler() {
      this._selection = this.gridApi.getSelectedRows()[0];
      this.configure();
    },
    newBenefitHandler() {
      this.routeTo("config-factor");
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
          provision_id: this.provision_id,
          ...params,
        },
        query: { ...query },
      });
    },
    ruleFormatter(rule) {
      const ops = {
        __lt__: "<",
        __le__: "<=",
        __gt__: ">",
        __ge__: ">=",
        __eq__: "=",
        __ne__: "!=",
      };
      if (!rule) return "";
      return `${rule.field_name} ${ops[rule.comparison_operator_code]} ${
        rule.field_value
      }`;
    },
    toggleHandler(stg) {
      this.routeTo(stg.to);
    },
  },
  computed: {
    output() {
      return this.factors;
    },
    rowData() {
      return this.factors.map((item, i) => {
        const rule1 =
          item.factor_rules && item.factor_rules.length >= 1
            ? item.factor_rules[0]
            : null;
        const rule2 =
          item.factor_rules && item.factor_rules.length >= 2
            ? item.factor_rules[1]
            : null;
        const rule3 =
          item.factor_rules && item.factor_rules.length >= 3
            ? item.factor_rules[2]
            : null;
        return {
          ...item,
          rule1: this.ruleFormatter(rule1),
          rule2: this.ruleFormatter(rule2),
          rule3: this.ruleFormatter(rule3),
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
