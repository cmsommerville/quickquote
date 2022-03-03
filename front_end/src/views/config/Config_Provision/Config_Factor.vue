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
          <div
            class="absolute -bottom-8 -right-6 flex flex-col"
            @mouseenter="show_fab = true"
            @mouseleave="show_fab = false"
          >
            <transition name="scale-up">
              <div v-if="show_fab">
                <app-modal
                  :fab="true"
                  :disabled="!rule._id"
                  class="bg-red-700 text-white mb-4 border-2 border-red-700 disabled:border-gray-200"
                  ><x-icon class="h-16 w-16 p-5" />
                  <template #header>Are you sure?</template>
                  <template #content="contentProps">
                    <div class="flex justify-center items-center mx-32 my-8">
                      <app-button class="bg-red-700 mr-8" @click="deleteHandler"
                        >Delete record</app-button
                      >
                      <app-button
                        :transparent="true"
                        @click="contentProps.close"
                        >Cancel</app-button
                      >
                    </div>
                  </template>
                </app-modal>
              </div>
            </transition>
            <transition name="scale-up">
              <div v-if="show_fab">
                <app-button
                  class="bg-white text-theme-primary border-2 border-theme-primary mb-4 disabled:border-gray-200"
                  :disabled="!rule._id"
                  :fab="true"
                  @click="openEditHandler"
                  ><pencil-icon class="h-16 w-16 p-5"
                /></app-button>
              </div>
            </transition>

            <config-factor-modal
              class="mr-8 border-2 border-theme-primary disabled:border-gray-200"
              ref="newModal"
              :fab="true"
              v-model="rule"
              :factor="factor"
              @click="newRuleHandler"
              @update:modelValue="ruleSaveHandler"
              @close:modal="show_fab = false"
              ><plus-icon class="h-16 w-16 p-5"
            /></config-factor-modal>

            <config-factor-modal
              class="hidden"
              ref="editModal"
              v-model="rule"
              :factor="factor"
              @update:modelValue="ruleSaveHandler"
              @close:modal="show_fab = false"
            ></config-factor-modal>
          </div>
        </div>
        <div class="mx-auto mt-12 flex items-center">
          <app-button class="mx-8" @click="save">Save</app-button>
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
import ConfigFactorModal from "./Config_Factor_Modal.vue";
import { AgGridVue } from "ag-grid-vue3";
import { Model_ConfigFactor } from "@/models/Model_ConfigFactor.js";
import { CONFIG_FACTOR_RULE_LIST__COLUMN_DEFS } from "./config.js";

export default {
  name: "Config_Factor",
  components: {
    AppFormHeader,
    AppFormTabs,
    AppModal,
    AgGridVue,
    ConfigFactorModal,
  },
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    provision_id: {
      required: false,
      type: [Number, String],
    },
    factor_id: {
      required: false,
      type: [Number, String],
    },
  },
  mounted() {
    this.loaded = false;
    let p_factor;
    if (this.factor_id) {
      p_factor = axios.get(`/config/factor/${this.factor_id}`);
    } else {
      p_factor = new Promise((resolve, reject) => {
        resolve({ data: {} });
      });
    }

    const p_operators = axios.get("/config/ref-comparison-operators");
    const p_provision = axios.get(
      `/config/provision-ui-component/${this.provision_id}`
    );

    Promise.all([p_factor, p_operators, p_provision])
      .then(([factor, operators, provision]) => {
        const fctr = { ...factor.data };
        this.options_operators = [...operators.data];
        this.factor = this.modelSetter(fctr);
        this.provision = { ...provision.data };
        const rules = this.factor.factor_rules.map((rule) => {
          return {
            ...rule,
            _id: (Math.random() + 1).toString(36).substring(4),
          };
        });
        this.factor = { ...this.factor, factor_rules: [...rules] };
        this.loaded = true;
      })
      .catch((err) => {
        this.loaded = true;
      });
  },
  data() {
    return {
      loaded: false,
      show_fab: false,
      title: "Setup Rules",
      subtitle: "Add, edit, or delete a rule!",
      active_stage: "configure",
      _stages: [
        {
          label: "Back to Factors",
          id: "factor_list",
          to: "config-factor-list",
        },
        {
          label: "Configure",
          id: "configure",
          disabled: true,
        },
      ],
      factor: {},
      provision: {},
      rule: {},
      columnDefs: [...CONFIG_FACTOR_RULE_LIST__COLUMN_DEFS],
    };
  },
  computed: {
    output() {
      return this.modelSetter(this.factor);
    },
    rowData() {
      if (this.factor.factor_rules) {
        return this.factor.factor_rules.map((item) => {
          return {
            ...this.options_operators.find(
              (op) =>
                op.comparison_operator_code === item.comparison_operator_code
            ),
            ...item,
          };
        });
      }
      return [];
    },
    stages() {
      return this._stages.map((item) => ({
        ...item,
        active: item.id === this.active_stage,
      }));
    },
  },
  methods: {
    async deleteHandler() {
      if (this.rule.factor_rule_id) {
        const res = await axios.delete(
          `/config/factor-rule/${this.rule.factor_rule_id}`
        );
      }
      this.factor.factor_rules = [
        ...this.factor.factor_rules.filter((rule) => {
          return rule._id !== this.rule._id;
        }),
      ];
    },
    doubleClickRowHandler() {
      this.rule = { ...this.gridApi.getSelectedRows()[0] };
      this.$refs.editModal.open();
    },
    modelSetter(data) {
      return new Model_ConfigFactor(
        this.factor_id,
        this.provision_id,
        data.factor_priority,
        data.factor_value,
        data.factor_rules
      );
    },
    newRuleHandler() {
      this.rule = { _id: (Math.random() + 1).toString(36).substring(4) };
    },
    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;
    },
    onGridSelectionChanged(e) {
      this.rule = this.gridApi.getSelectedRows()[0];
    },
    openEditHandler() {
      this.show_fab = false;
      this.$refs.editModal.open();
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
    ruleSaveHandler() {
      const oldRules =
        this.factor.factor_rules.filter((item) => {
          return item._id !== this.rule._id;
        }) ?? [];
      this.factor.factor_rules = [...oldRules, { ...this.rule }];
    },
    async save() {
      try {
        const fctr = await axios.post("/config/factor", this.output);
        this.factor = { ...fctr.data };
        this.$store.commit("SET_SELECTIONS_OBJECT", this.factor);
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", "Saved to database!");
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
    toggleHandler(stage) {
      this.routeTo(stage.to);
    },
  },
};
</script>

<style scoped lang="scss">
.scale-up-enter-active,
.scale-up-leave-active {
  transition: all 0.3s ease;
}

.scale-up-enter-from,
.scale-up-leave-to {
  transform: translateY(2rem);
  opacity: 0;
}
</style>
