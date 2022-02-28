<template>
  <app-modal :ref="ref_name" v-bind="$attrs">
    <slot></slot>
    <template #header>Edit This Rule</template>
    <template #content="contentProps">
      <div class="flex flex-col items-center">
        <div class="w-5/6 mx-auto grid grid-cols-2 gap-8 py-8">
          <div class="my-8 w-72 mx-8">
            <app-select
              v-model="modelValue.class_name"
              :items="options_class_name"
              item_text="class_name"
              item_value="class_code"
              >Class Name</app-select
            >
          </div>
          <div class="my-8 w-72 mx-8">
            <app-select
              v-model.trim="modelValue.field_name"
              :items="options_field_name"
              item_text="field_name"
              item_value="field_code"
              >Field Name</app-select
            >
          </div>
          <div class="my-8 w-72 mx-8">
            <app-select
              :items="options_operators"
              item_text="comparison_operator_symbol"
              item_value="comparison_operator_code"
              v-model="modelValue.comparison_operator_code"
              >Operator</app-select
            >
          </div>

          <div class="my-8 w-72 mx-8">
            <app-input
              v-if="options_field_value_list.length === 0"
              v-model.trim="modelValue.field_value"
              >Field Value</app-input
            >
            <app-select
              v-if="options_field_value_list.length > 0"
              :items="options_field_value_list"
              item_text="label"
              item_code="code"
              v-model="modelValue.field_value"
              >Field Value</app-select
            >
          </div>
          <div class="my-8 w-72 mx-8">
            <app-input v-model.trim="modelValue.field_value_data_type"
              >Field Value Data Type</app-input
            >
          </div>
        </div>
        <app-button
          class="mx-auto mb-4"
          @click="addRuleHandler(contentProps.close)"
          >Save</app-button
        >
      </div>
    </template>
  </app-modal>
</template>

<script>
import axios from "@/services/axios.js";
import AppModal from "@/components/AppModal.vue";
import {
  Model_ConfigFactor,
  Model_ConfigFactorUI,
} from "@/models/Model_ConfigFactor.js";
import { FACTOR_OBJECTS } from "./factor_objects.js";

export default {
  name: "Config_Factor_Modal",
  inheritAttrs: false,
  components: {
    AppModal,
  },
  props: {
    factor: {
      required: true,
    },
    modelValue: {
      required: true,
    },
  },
  async mounted() {
    this.loaded = false;
    const options_operators = await axios.get(
      "/config/ref-comparison-operators"
    );
    const provision = await axios.get(
      `/config/provision-ui-component/${this.factor.provision_id}`
    );
    this.options_operators = [...options_operators.data];
    this.provision = { ...provision.data };
    this.options_factor_objects = this.factorOptionHandler(
      FACTOR_OBJECTS,
      this.provision
    );
    this.ref_name = (Math.random() + 1).toString(36).substring(4);
  },
  watch: {
    modelValue: {
      async handler(newVal, oldVal) {
        if (!newVal.field_name) return;
        const field = this.options_field_name.find((item) => {
          return item.field_code === newVal.field_name;
        });
        if (field.field_value_list) {
          const data = await field.field_value_list();
          this.options_field_value_list = [...data];
          this.modelValue.comparison_operator_code = "__eq__";
          this.modelValue.field_value_data_type = field.field_value_data_type;
        } else {
          this.options_field_value_list = [];
          this.modelValue.field_value_data_type = field.field_value_data_type;
        }
      },
      deep: true,
    },
  },
  data() {
    return {
      ref_name: null,
      loaded: false,
      options_operators: [],
      options_factor_objects: [],
      options_field_value_list: [],
      provision: {},
    };
  },
  computed: {
    options_class_name() {
      return this.options_factor_objects.map((item) => {
        return { class_name: item.class_name, class_code: item.class_code };
      });
    },
    options_field_name() {
      if (this.modelValue.class_name) {
        return this.options_factor_objects.find((item) => {
          return item.class_code === this.modelValue.class_name;
        }).fields;
      }
      return [];
    },
  },
  methods: {
    addRuleHandler(callback) {
      this.$emit("update:modelValue", this.modelValue);
      callback();
    },
    fieldValueDataTypeHandler(val) {
      if (!isNaN(Number(val))) return "number";
      if (["true", "false"].includes(val.toLowerCase())) return "booleans";
      return "string";
    },
    factorOptionHandler(data, provision) {
      const fields = new Model_ConfigFactorUI(provision);
      return [
        ...data,
        {
          class_code: "provision",
          class_name: "Provision",
          fields: [{ ...fields }],
        },
      ];
    },
    open() {
      this.$refs[this.ref_name].openHandler();
    },
  },
};
</script>
