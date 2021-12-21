<template>
  <div>
    <v-form>
      <div class="mb-4 main-form" v-if="loaded">
        <v-select
          v-model="component_type_selection"
          :items="component_types"
          item-text="component_type_label"
          item-value="component_type_code"
          return-object
          filled
          outlined
          label="Component Type"
        />

        <v-text-field
          v-model="provision_ui.ui_label"
          filled
          outlined
          label="UI Label"
        />

        <v-select
          v-if="component_type_selection.component_type_enum === 'INPUT'"
          v-model="provision_ui.input_type"
          :items="['number', 'input', 'date']"
          filled
          outlined
          label="Input Type"
        />
        <div v-if="!!provision_ui.input_type">
          <v-text-field
            v-if="output.input_type === 'number'"
            v-model="provision_ui.min_value"
            filled
            outlined
            label="Minimum Value"
          />
          <v-text-field
            v-if="output.input_type === 'number'"
            v-model="provision_ui.max_value"
            filled
            outlined
            label="Maximum Value"
          />
          <v-text-field
            v-if="output.input_type === 'number'"
            v-model="provision_ui.step_value"
            filled
            outlined
            label="Step Size"
          />
        </div>
      </div>
    </v-form>

    <app-modal-list-form
      v-if="
        component_type_selection &&
        component_type_selection.component_type_enum === 'SELECT'
      "
      title="Add Selections"
      :schema="[
        { code: 'item_code', label: 'Item Code' },
        { code: 'item_label', label: 'Item Label' },
      ]"
      :inputData="select_items"
      @submit:list-data="selectItemHandler"
    />

    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn color="primary" class="mx-4" @click="save" :disabled="!valid">
        Save
      </v-btn>
      <v-btn color="accent" class="mx-4" @click="$router.go(-1)"> Back </v-btn>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";
import { ProvisionUIModel } from "../../models/ProvisionModels.js";
import AppModalListForm from "../../components/AppModalListForm.vue";

export default {
  name: "ConfigProvision",
  components: { AppModalListForm },
  props: {
    product_id: {
      type: [Number, String],
      required: true,
    },
    provision_id: {
      type: [Number, String],
      required: true,
    },
  },
  async mounted() {
    this.loaded = false;
    const components = await axios.get(`/qry-config/all-ui-components`);
    this.component_types = [...components.data];
    const res = await axios.get(
      `/config/provision-ui-component/${this.provision_id}`
    );
    this.initializeData(res.data);
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      editable: true,
      modal: false,
      provision_ui: null,
      component_type_selection: null,
      component_types: [],
      select_items: [],
    };
  },
  computed: {
    valid() {
      return true;
    },
    output() {
      /* eslint-disable no-unused-vars */
      const { component_type, ...output } = {
        ...this.provision_ui,
      };

      output.provision_id = +this.provision_id;
      output.component_type_code =
        this.component_type_selection.component_type_code;
      output.component_type = this.component_type_selection.component_type_enum;
      output.items = this.select_items.map((item) => {
        return {
          ...item,
          provision_id: this.provision_id,
        };
      });

      /* eslint-enable no-unused-vars */
      return ProvisionUIModel(output);
    },
    schema_validator() {
      return this.output.validate();
    },
  },
  methods: {
    initializeData(config) {
      this.provision_ui = { ...config };
      this.component_type_selection = {
        component_type_enum: config.component_type ?? null,
        component_type_code: config.component_type_code ?? null,
      };
      this.select_items = [...config.items];
    },
    selectItemHandler(data) {
      this.select_items = [...data];
    },
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        params: {
          product_id: +this.product_id,
          provision_id: +this.provision_id,
        },
        query: { ...params },
      });
    },
    async save() {
      const output = { ...this.output };
      await axios.post("/config/provision-ui-component", {
        ...output,
      });
    },
  },
};
</script>

<style scoped>
.main-form {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  column-gap: 10px;
  row-gap: 15px;
}

.section-configure {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  column-gap: 10px;
  row-gap: 15px;
}

.btn-edit {
  position: absolute;
  top: -15px;
  right: -15px;
}
</style>
