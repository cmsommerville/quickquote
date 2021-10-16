<template>
  <div class="content-coverage">
    <div class="d-flex justify-space-between">
      <v-switch
        v-model="selected"
        :label="coverage.text"
        @change="toggleCoverage"
      >
      </v-switch>
      <v-btn color="accent" fab dark small outlined @click="hidden = !hidden">
        <v-icon>mdi-arrow-down</v-icon>
      </v-btn>
    </div>
    <div class="content-benefits ml-6 mb-6" v-if="!hidden">
      <v-row v-for="benefit in benefits" :key="benefit.name">
        <v-col cols="12" sm="6">
          <v-subheader>{{ benefit.text }}</v-subheader>
        </v-col>
        <v-col cols="12" sm="3">
          <component
            :is="benefit.ui.component"
            v-bind="{ ...benefit.ui }"
            :name="benefit.name"
            :label="benefit.text"
            v-model="benefit.selectedValue"
            :prefix="benefit.amounts.unit === 'dollar' ? '$' : ''"
            :suffix="benefit.amounts.unit === 'percent' ? '%' : ''"
            @change="setValue"
            outlined
            dense
            rounded
            background-color="lightest"
          />
        </v-col>
        <v-col v-if="!!benefit.duration" cols="12" sm="3">
          <component
            :is="benefit.duration.component"
            v-bind="{ ...benefit.duration }"
            :name="benefit.duration.name"
            :label="benefit.duration.label"
            v-model="benefit.selectedDuration"
            @change="setValue"
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
  },
  data() {
    return {
      hidden: true,
      selected: false,
      benefits: [],
    };
  },
  mounted() {
    this.selected = this.coverage.default;
    this.benefits = this.coverage.benefits.map((bnft) => {
      return {
        ...bnft,
        selectedValue: bnft.amounts.default,
        selectedDuration: bnft.duration ? bnft.duration.default : 0,
      };
    });
    this.toggleCoverage();
  },
  methods: {
    toggleCoverage() {
      this.benefits.map((bnft) => {
        bnft.selectedValue = this.selected ? bnft.amounts.default : 0;
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
