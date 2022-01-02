<template>
  <div class="content-coverage">
    <div class="d-flex justify-space-between">
      <v-switch v-model="selected" :label="label" @change="toggleCoverage">
      </v-switch>
      <v-btn color="accent" fab dark small outlined @click="hidden = !hidden">
        <v-icon>mdi-arrow-down</v-icon>
      </v-btn>
    </div>
    <div class="content-benefits ml-6 mb-6" v-if="!hidden">
      <v-row v-for="benefit in benefits" :key="benefit.benefit_id">
        <v-col cols="12" sm="6">
          <v-subheader>{{ benefit.benefit_label }}</v-subheader>
        </v-col>
        <v-col cols="12" sm="3">
          <v-text-field
            :name="benefit.benefit_code"
            :label="benefit.benefit_label"
            v-model="benefit.ui_benefit_value"
            :prefix="benefit.unit_code === 'Dollar' ? '$' : ''"
            :suffix="benefit.unit_code === 'Percent' ? '%' : ''"
            @change="setValue"
            outlined
            dense
            rounded
            background-color="lightest"
          />
        </v-col>
        <v-col
          v-for="duration in benefit.durations"
          :key="duration.benefit_duration_id"
          cols="12"
          sm="3"
        >
          <v-select
            :items="duration.duration_items"
            :name="duration.duration_code"
            :label="duration.duration_label"
            v-model="duration.ui_duration_item_code"
            @change="setValue"
            item-text="item_label"
            item-value="item_code"
            outlined
            dense
            rounded
            background-color="lightest"
          />
        </v-col>
        <v-spacer></v-spacer>
      </v-row>
    </div>
  </div>
</template>

<script>
import { VTextField, VSelect, VSwitch } from "vuetify/lib";
export default {
  name: "CoverageSelectionsExpansionPanel",
  components: {
    VTextField,
    VSelect,
    VSwitch,
  },
  props: {
    coverage: {
      type: Object,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      hidden: true,
      selected: false,
      benefits: [],
    };
  },
  mounted() {
    this.selected = this.coverage.default_value;
    this.benefits = this.coverage.benefits;
    // this.toggleCoverage();
  },
  methods: {
    toggleCoverage() {
      this.benefits.map((bnft) => {
        bnft.ui_selection_value = this.selected
          ? (bnft.selected_benefit && bnft.selected_benefit.benefit_value) ??
            bnft.default_value
          : 0;
        if (bnft.durations) {
          for (const dur of bnft.durations) {
            const default_val = dur.duration_items.find((item) => {
              return item.item_code === dur.default_duration_item_code;
            });
            dur.ui_selection_value = this.selected
              ? default_val ?? dur.duration_items[0]
              : null;
          }
        }
      });
      this.setValue();
    },
    setValue() {
      this.$emit("selections-change", this.benefits);
    },
  },
};
</script>

<style>
.content-benefits {
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 0.5rem;
}
</style>
