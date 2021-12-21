<template>
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="red lighten-2" dark v-bind="attrs" v-on="on">
        <slot> Add Variability</slot>
      </v-btn>
    </template>

    <v-card>
      <v-card-title
        class="text-h5 grey lighten-2 d-flex justify-space-between mb-4"
      >
        Add a factor rule
      </v-card-title>

      <v-card-text>
        <v-row v-for="(item, ix) in config" :key="ix">
          <v-col cols="12" sm="3">
            <v-select
              :items="variationOptions"
              filled
              outlined
              item-text="label"
              item-value="code"
              label="Varies By"
              v-model="item.item"
              return-object
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
              v-model="item.comparison"
            />
          </v-col>
          <v-col cols="12" :sm="item.comparison === 'range' ? 3 : 6">
            <v-text-field
              filled
              outlined
              :label="item.comparison === 'range' ? 'Lower Value' : 'Value'"
              v-model="item.value"
            />
          </v-col>
          <v-col cols="12" sm="3" v-if="item.comparison === 'range'">
            <v-text-field
              v-model="item.upper"
              filled
              outlined
              label="Upper Value"
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
  data() {
    return {
      dialog: false,
      factor_value: null,
      config: [{}],
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
        { label: "Between", code: "range" },
        { label: "Not Between", code: "nrange" },
      ],
    };
  },
  computed: {
    output() {
      return {
        factor_value: this.factor_value,
        rules: this.config.map((rule, index) => {
          let val;
          if (!isNaN(rule.value)) {
            val = +rule.value;
          }
          return {
            comparison_operator_code: rule.comparison,
            class_name: "test",
            factor_rule_priority: index,
            field_name: rule.item.code,
            field_value: rule.value,
            field_value_data_type: typeof val,
          };
        }),
      };
    },
  },
  methods: {
    addCondition() {
      this.config = [...this.config, {}];
    },
    initialize() {
      this.config = [{}];
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
