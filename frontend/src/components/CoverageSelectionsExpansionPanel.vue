<template>
  <div class="content-coverage">
    <div class="d-flex justify-space-between">
      <v-switch
        v-model="selected"
        :label="coverage.text"
        @change="toggleCoverage"
      >
      </v-switch>
      <v-btn color="primary" fab dark small @click="hidden = !hidden">
        <v-icon>mdi-menu-down-outline</v-icon>
      </v-btn>
    </div>
    <div class="content-benefits ml-6" v-if="!hidden">
      <v-switch
        v-for="benefit in benefits"
        :key="benefit.name"
        v-model="benefit.selectedValue"
        :label="
          benefit.text +
          (benefit.selectedValue !== 0 ? ` (${benefit.selectedValue}%)` : '')
        "
        :false-value="0"
        :true-value="benefit.amounts.default"
        @change="setValue"
      >
      </v-switch>
    </div>
  </div>
</template>

<script>
export default {
  name: "CoverageSelectionsExpansionPanel",
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
      return { ...bnft, selectedValue: bnft.amounts.default };
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

<style></style>
