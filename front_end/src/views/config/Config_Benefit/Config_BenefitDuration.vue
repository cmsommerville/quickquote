<template>
  <div v-if="loaded">
    <app-form-card
      :stages="stages"
      :title="title"
      :subtitle="subtitle"
      @toggle:stage="toggleHandler"
    >
      <template #content>
        <div class="my-12 grid grid-cols-3 gap-16" v-if="loaded">
          <div class="flex flex-col">
            <div class="mb-8">
              <app-input v-model.trim="duration.benefit_duration_code"
                >Duration Code</app-input
              >
            </div>
            <div class="mb-8">
              <app-input v-model.trim="duration.benefit_duration_label"
                >Duration Name</app-input
              >
            </div>
            <div class="mb-8">
              <app-select
                v-model.trim="duration.default_duration_item_code"
                :items="duration.items"
                item_text="item_label"
                item_value="item_code"
                >Default Duration Item</app-select
              >
            </div>
          </div>
          <div class="col-span-2 flex justify-center flex-col">
            <div class="h-72 w-full mx-auto">
              <ag-grid-vue
                class="ag-theme-alpine"
                style="width: 100%; height: 100%"
                :columnDefs="columnDefs"
                @grid-ready="onGridReady"
                :rowData="rowData"
                rowSelection="single"
                @selection-changed="onGridSelectionChanged"
              >
              </ag-grid-vue>
            </div>
          </div>
        </div>
      </template>

      <template #actions>
        <div class="flex justify-center">
          <div class="flex justify-center">
            <app-button class="mx-3" @click="save">Save</app-button>
          </div>
          <app-modal>
            Add Item
            <template #header>Add Benefit Duration Item</template>
            <template #content="slotProps">
              <div class="mt-16 mb-8 grid grid-cols-2 lg:grid-cols-3 gap-4">
                <div class="mb-8">
                  <app-input v-model.trim="item.item_code"
                    >Duration Item Code</app-input
                  >
                </div>
                <div class="mb-8">
                  <app-input v-model.trim="item.item_label"
                    >Duration Item Name</app-input
                  >
                </div>
                <div class="mb-8">
                  <app-input
                    type="number"
                    v-model.number="item.benefit_duration_factor"
                    >Duration Item Factor</app-input
                  >
                </div>
              </div>
              <div class="flex justify-center">
                <app-button @click="saveItemHandler(slotProps.close)"
                  >Save</app-button
                >
              </div>
            </template>
          </app-modal>
        </div>
      </template>
    </app-form-card>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import AppModal from "@/components/AppModal.vue";
import { AgGridVue } from "ag-grid-vue3";
import { CONFIG_BENEFIT_DURATION_ITEMS_LIST__COLUMN_DEFS } from "./config.js";
import { Model_ConfigBenefitDuration } from "@/models/Model_ConfigBenefitDuration.js";

export default {
  name: "Config_BenefitDuration",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    benefit_id: {
      required: true,
      type: [Number, String],
    },
    duration_id: {
      required: false,
      type: [Number, String],
    },
  },
  components: { AgGridVue, AppModal },
  mounted() {
    this.loaded = false;
    let p_duration;
    if (this.duration_id) {
      p_duration = axios.get(`/config/benefit-duration/${this.duration_id}`);
    } else {
      p_duration = new Promise((resolve, reject) => {
        resolve({ data: {} });
      });
    }

    Promise.all([p_duration])
      .then(([duration]) => {
        this.duration = { ...this.modelSetter(duration.data) };
        this.loaded = true;
      })
      .catch((err) => {
        this.loaded = true;
      });
  },
  data() {
    return {
      loaded: false,
      title: "Setup This Benefit Duration",
      subtitle: "",
      active_stage: "configure",
      _stages: [
        {
          label: "All Durations",
          id: "durations",
          to: "config-benefit-duration-list",
        },
        {
          label: "Configure",
          id: "configure",
          disabled: true,
        },
      ],
      columnDefs: [...CONFIG_BENEFIT_DURATION_ITEMS_LIST__COLUMN_DEFS],
      duration: { items: [] },
      item: {},
    };
  },
  computed: {
    rowData() {
      if (this.duration.items) {
        return this.duration.items.map((item) => {
          return {
            benefit_duration_item_id: "-",
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
    output() {
      return this.modelSetter(this.duration);
    },
  },
  methods: {
    modelSetter(data) {
      return new Model_ConfigBenefitDuration(
        data.benefit_duration_id ?? null,
        this.benefit_id,
        data.benefit_duration_code ?? null,
        data.benefit_duration_label ?? null,
        data.default_duration_item_code ?? null,
        data.items ?? []
      );
    },
    routeTo(route_name, params = {}, query = {}) {
      this.$router.push({
        name: route_name,
        params: {
          product_id: this.product_id,
          benefit_id: this.benefit_id,
          ...params,
        },
        query: { ...query },
      });
    },
    saveItemHandler(callback) {
      if (this.duration.items) {
        const editItem = this.duration.items.find(
          (i) => i.item_code === this.item.item_code
        );

        if (editItem && editItem.benefit_duration_item_id) {
          this.item = {
            ...this.item,
            benefit_duration_item_id: editItem.benefit_duration_item_id,
          };
        }
      }
      this.duration.items = [
        ...this.duration.items.filter((i) => {
          return i.item_code !== this.item.item_code;
        }),
        { ...this.item },
      ];
      this.item = {};
      callback();
    },
    async save() {
      try {
        const res = await axios.post(`/config/benefit-duration`, this.output);
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", "Saved benefit duration");
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
    toggleHandler(stage) {
      this.routeTo(stage.to);
    },
    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;
    },
    onGridSelectionChanged() {
      this._selection = this.gridApi.getSelectedRows()[0];
    },
    clickHandler() {
      console.log(Math.random());
    },
  },
};
</script>
