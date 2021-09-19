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
    <div class="content-benefits ml-6" v-if="selected">
      <v-switch
        v-for="benefit in coverage.benefits"
        :key="benefit.name"
        v-model="selections[benefit.name]"
        :label="benefit.text"
        :false-value="0"
        :true-value="benefit.default"
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
      selections: {},
    };
  },
  mounted() {
    this.selected = this.coverage.default;
    this.selections = [...this.coverage.benefits].reduce(
      (acc, curr) => ((acc[curr.name] = curr.amounts.default), acc),
      {}
    );
  },
  methods: {
    toggleCoverage() {
      this.coverage.benefits.map((bnft) => {
        this.selections[bnft.name] = this.selected ? bnft.amounts.default : 0;
      });
    },
    setValue() {
      this.$emit("selections-change", this.selections);
    },
  },
};
</script>

<style></style>
