<template>
  <v-dialog v-model="show">
    <v-card>
      <v-card-title
        class="text-h5 grey lighten-2 d-flex justify-space-between mb-4"
      >
        Add a factor rule
      </v-card-title>

      <v-card-text>
        <v-row v-for="(item, ix) in factor_rules" :key="ix">
          <v-col cols="12" sm="3">
            <v-select
              :items="variationOptions"
              filled
              outlined
              item-text="label"
              item-value="code"
              label="Varies By"
              v-model="item.field_name"
            />
          </v-col>
          <v-col cols="12" sm="2">
            <v-select
              :items="comparisonOperators"
              filled
              outlined
              item-text="label"
              item-value="code"
              label="Operator"
              v-model="item.comparison_operator_code"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field
              filled
              outlined
              label="Value"
              v-model="item.field_value"
            />
          </v-col>
          <v-col cols="12" sm="1" class="py-6">
            <v-icon large color="pink lighten-2" @click="addCondition">
              mdi-plus-circle
            </v-icon>
          </v-col>
        </v-row>

        <v-row class="py-4">
          <v-col></v-col>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model.number="factor_value"
              filled
              outlined
              label="Factor"
            />
          </v-col>
        </v-row>
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
      variationOptions: [
        { label: "Rating State", code: "rating_state" },
        { label: "Group Size", code: "group_size" },
        { label: "Attained Age", code: "attained_age" },
        { label: "Issue Age", code: "issue_age" },
        { label: "Provision Value", code: "provision_value" },
      ],
      comparisonOperators: [
        { label: "=", code: "eq" },
        { label: "<", code: "lt" },
        { label: "<=", code: "le" },
        { label: ">", code: "gt" },
        { label: ">=", code: "ge" },
        { label: "!=", code: "ne" },
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
            class_name: "test",
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
    emitConfig() {
      this.$emit("submit:factor-config", this.output);
      this.initialize();
      this.dialog = false;
    },
  },
};
</script>

<style></style>
