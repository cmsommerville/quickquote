<template>
  <v-card v-if="loaded">
    <v-card-title
      class="text-h5 grey lighten-2 d-flex justify-space-between mb-4"
    >
      Add a factor rule
    </v-card-title>

    <v-card-text>
      <ul>
        <li class="rule" v-for="(item, ix) in config" :key="ix">
          <v-select
            :items="variationOptions"
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
      <!-- <v-row v-for="(item, ix) in config" :key="ix">
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
      </v-row> -->

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
      <v-btn color="primary" text> Save </v-btn>
      <v-btn color="pink lighten-2" dark @click="addCondition">
        Add Rule
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { FACTOR_RULE_FIELDS } from "../../data/lookups.js";

export default {
  props: {
    product_id: {
      required: true,
      type: [String, Number],
    },
    provision_id: {
      required: true,
      type: [String, Number],
    },
  },
  mounted() {
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      config: [{}],
      factor_value: null,
      fields: [...FACTOR_RULE_FIELDS],
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
        return this.visible;
      },
      set(value) {
        if (!value) {
          this.$emit("close", this.output);
          this.initialize();
        }
      },
    },
    output() {
      return {
        factor_value: this.factor_value,
        rules: this.config.map((rule) => {
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
      this.config = [...this.config, {}];
    },
    initialize() {
      this.config = [{}];
      this.factor_value = null;
    },
  },
};
</script>

<style scoped>
.rule {
  list-style-type: none;
  display: grid;
  grid-template-columns: 2fr 2fr 1fr 2fr;
  grid-gap: 10px;
}
</style>
