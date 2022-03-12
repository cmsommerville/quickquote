<template>
  <div v-if="loaded">
    <app-form-card
      :stages="stages"
      :title="title"
      :subtitle="subtitle"
      @toggle:stage="toggleHandler"
    >
      <template #content>
        <div class="w-2/3 mx-auto grid grid-cols-2 gap-x-12">
          <div class="my-8">
            <app-select
              :items="options_component_types"
              item_text="component_type_label"
              item_value="component_type_enum"
              v-model="_selection.component_type"
              >Component Type</app-select
            >
          </div>

          <div class="my-8 w-full flex justify-end">
            <div class="w-full">
              <app-select
                v-if="_selection.component_type === 'INPUT'"
                :items="options_input_types"
                item_text="type_code"
                item_value="type_code"
                v-model="_selection.input_type"
                >Input Type</app-select
              >
            </div>
            <div v-if="_selection.component_type === 'SELECT'">
              <app-modal class="hidden" ref="modal" :fab="true">
                <template #header>Edit an Item</template>
                <template #content="contentProps">
                  <div class="flex flex-col items-center">
                    <div class="w-5/6 mx-auto grid grid-cols-2 gap-8 py-8">
                      <div class="my-8">
                        <app-input v-model.trim="_item.item_code"
                          >Item Code</app-input
                        >
                      </div>
                      <div class="my-8">
                        <app-input v-model.trim="_item.item_label"
                          >Item Label</app-input
                        >
                      </div>
                    </div>
                    <app-button
                      class="mx-auto mb-4"
                      @click="addSelectItemHandler(contentProps.close)"
                      >Save</app-button
                    >
                  </div>
                </template>
              </app-modal>
            </div>
          </div>
          <div
            class="h-72 w-full col-span-2 relative"
            v-if="_selection.component_type === 'SELECT'"
          >
            <ag-grid-vue
              class="ag-theme-alpine"
              style="width: 100%; height: 100%"
              :columnDefs="selectItemColumnDefs"
              @grid-ready="onGridReady"
              :rowData="selectItemRowData"
              rowSelection="single"
              @selection-changed="onGridSelectionChanged"
              @row-double-clicked="doubleClickRowHandler"
            >
            </ag-grid-vue>
            <app-new-edit-delete-button
              :disabled_edit="!_item.item_code"
              :disabled_delete="!_item.item_code"
              @fab:new="newItemHandler"
              @fab:edit="editItemHandler"
              @fab:delete="deleteItemHandler"
            />
          </div>
          <div
            class="grid grid-cols-3 gap-x-8 col-span-2"
            v-if="
              _selection.component_type === 'INPUT' &&
              _selection.input_type === 'number'
            "
          >
            <div class="my-8">
              <app-input v-model="_selection.min_value">Min Value</app-input>
            </div>
            <div class="my-8">
              <app-input v-model="_selection.max_value">Max Value</app-input>
            </div>
            <div class="my-8">
              <app-input v-model="_selection.step_value">Step Size</app-input>
            </div>
          </div>
        </div>
      </template>

      <template #actions>
        <div class="flex justify-center">
          <app-button class="mx-3" @click="save">Save</app-button>
          <app-button class="mx-3" :transparent="true" @click="cancel"
            >Cancel</app-button
          >
        </div>
      </template>
    </app-form-card>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import AppModal from "@/components/AppModal.vue";
import AppNewEditDeleteButton from "@/components/AppNewEditDeleteButton.vue";
import { AgGridVue } from "ag-grid-vue3";
import { CONFIG_PROVISION_UI_SELECT_ITEMS__COLUMN_DEFS } from "./config.js";
import { Model_ConfigProvisionUI } from "@/models/Model_ConfigProvision.js";

export default {
  name: "Config_ProvisionUI",
  components: { AgGridVue, AppModal, AppNewEditDeleteButton },
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

    this.selectItemColumnDefs = [
      ...CONFIG_PROVISION_UI_SELECT_ITEMS__COLUMN_DEFS,
    ];
    const p_component = axios.get(
      `/config/provision-ui-component/${this.provision_id}`
    );
    const p_comp_types = axios.get("/config/ref-component-types");
    const p_input_types = axios.get("/config/ref-text-field-types");

    Promise.all([p_comp_types, p_input_types, p_component])
      .then(([comp_types, input_types, component]) => {
        this.options_component_types = [...comp_types.data];
        this.options_input_types = [...input_types.data];
        this._selection = { ...component.data };
        this.loaded = true;
      })
      .catch((err) => {
        this.loaded = true;
      });
  },
  data() {
    return {
      loaded: false,
      title: "Setup This Provision's UI",
      subtitle: "",
      active_stage: "ui",
      _stages: [
        {
          label: "Back to Provision",
          id: "provision",
          to: "config-provision-landing",
        },
        {
          label: "User Interface",
          id: "ui",
          disabled: true,
        },
      ],
      selectItemColumnDefs: [],
      options_component_types: [],
      options_input_types: [],
      _selection: {},
      _item: {},
    };
  },
  computed: {
    output() {
      return this.modelSetter({
        ...(this.options_component_types.find((item) => {
          return item.component_type_enum === this._selection.component_type;
        }) ?? {}),
        ...this._selection,
        provision_id: this.provision_id,
      });
    },
    selectItemRowData() {
      if (this._selection.items && this._selection.items.length) {
        return this._selection.items.map((item) => {
          return { ...item };
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
    addSelectItemHandler(callback) {
      let otherItems = [];
      let thisItem = {};
      if (this._selection.items && this._selection.items.length) {
        otherItems = this._selection.items.filter((item) => {
          return item.item_code !== this._item.item_code;
        });

        thisItem = {
          ...this._selection.items.find((item) => {
            return item.item_code === this._item.item_code;
          }),
        };
      }

      this._selection.items = [...otherItems, { ...thisItem, ...this._item }];
      this._item = {};
      callback();
    },
    cancel() {
      this.routeTo("config-provision-landing");
    },
    deleteItemHandler() {
      if (!this._item) return;
      if (this._item.ui_component_item_id) {
        console.log("Delete request");
      } else {
        this._selection.items = this._selection.items.filter((item) => {
          return item.item_code !== this._item.item_code;
        });
      }
    },
    doubleClickRowHandler() {
      this._item = this.gridApi.getSelectedRows()[0];
      this.$refs.modal.openHandler();
    },
    editItemHandler() {
      this.$refs.modal.openHandler();
    },
    modelSetter(data) {
      return new Model_ConfigProvisionUI(data);
    },
    newItemHandler() {
      this._item = {};
      this.$refs.modal.openHandler();
    },
    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;
    },
    onGridSelectionChanged() {
      this._item = this.gridApi.getSelectedRows()[0];
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
    async save() {
      try {
        const res = await axios.post(
          "/config/provision-ui-component",
          this.output
        );
        this._selection = { ...res.data };
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", "Added to database");
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

<style></style>
