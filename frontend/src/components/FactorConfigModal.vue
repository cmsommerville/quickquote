<template>
  <v-dialog v-model="show">
    <v-card>
      <v-card-title
        class="text-h5 grey lighten-2 d-flex justify-space-between mb-4"
      >
        Add a factor rule
      </v-card-title>

      <v-card-text>
        <ul>
          <li class="factor-rule" v-for="(item, ix) in factor_rules" :key="ix">
            <v-select
              :items="classes"
              filled
              outlined
              item-text="label"
              item-value="code"
              label="Class Name"
              v-model="item.class_name"
            />
            <v-select
              :items="getClassAttributes(item.class_name)"
              filled
              outlined
              item-text="label"
              item-value="code"
              label="Varies By"
              v-model="item.field_name"
            />
            <v-select
              :items="comparisonOperators"
              filled
              outlined
              item-text="label"
              item-value="code"
              label="Operator"
              v-model="item.comparison_operator_code"
            />
            <v-text-field
              filled
              outlined
              label="Value"
              v-model="item.field_value"
            />
            <v-icon large color="pink lighten-2" @click="addCondition">
              mdi-plus-circle
            </v-icon>
          </li>
        </ul>

        <div class="factor-value">
          <v-text-field
            class="factor-field"
            v-model.number="factor_value"
            filled
            outlined
            label="Factor"
          />
        </div>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" text @click="emitConfig"> Save </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { FACTOR_RULE_FIELDS } from "../data/lookups.js";
export default {
  name: "FactorConfigModal",
  inheritAttrs: true,
  props: {
    value: {
      type: Boolean,
    },
    input_data: {
      type: Object,
    },
  },
  watch: {
    input_data: function (newVal) {
      this.factor_rules = [...newVal.factor_rules];
      this.factor_value = newVal.factor_value;
      this.factor_priority = newVal.factor_priority;
    },
  },
  data() {
    return {
      factor_priority: null,
      factor_value: null,
      factor_rules: [{}],
      fields: [...FACTOR_RULE_FIELDS],
      variationOptions: [
        { label: "Rating State", code: "rating_state" },
        { label: "Group Size", code: "group_size" },
        { label: "Attained Age", code: "attained_age" },
        { label: "Issue Age", code: "issue_age" },
        { label: "Provision Value", code: "provision_value" },
      ],
      comparisonOperators: [
        { label: "=", code: "__eq__" },
        { label: "<", code: "__lt__" },
        { label: "<=", code: "__le__" },
        { label: ">", code: "__gt__" },
        { label: ">=", code: "__ge__" },
        { label: "!=", code: "__ne__" },
      ],
    };
  },
  computed: {
    show: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
    classes() {
      return this.fields.map((item) => {
        return { label: item.class_label, code: item.class_code };
      });
    },
    output() {
      return {
        factor_value: this.factor_value,
        factor_priority: this.factor_priority,
        factor_rules: this.factor_rules.map((rule) => {
          let val = rule.field_value;
          if (!isNaN(rule.field_value)) {
            val = +rule.field_value;
          }
          return {
            comparison_operator_code: rule.comparison_operator_code,
            class_name: rule.class_name,
            field_name: rule.field_name,
            field_value: rule.field_value,
            field_value_data_type: typeof val,
          };
        }),
      };
    },
  },
  methods: {
    addCondition() {
      this.factor_rules = [...this.factor_rules, {}];
    },
    initialize() {
      this.factor_rules = [{}];
      this.factor_value = null;
    },
    getClassAttributes(class_code) {
      if (class_code) {
        const class_obj = this.fields.find(
          (item) => item.class_code === class_code
        );
        return class_obj.attributes;
      }
      return [];
    },
    emitConfig() {
      this.$emit("submit:factor-config", this.output);
      this.initialize();
      this.dialog = false;
    },
  },
};
</script>

<style></style>

<style scoped>
.factor-rule {
  list-style-type: none;
  display: grid;
  grid-template-columns: 2fr 2fr 1fr 2fr 50px;
  grid-gap: 10px;
}

.factor-value {
  display: grid;
  grid-template-columns: 1fr 20rem;
}

.factor-field {
  grid-column-start: 2;
}
</style>
