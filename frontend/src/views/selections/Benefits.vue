<template>
  <div class="container">
    <div class="content" v-if="loaded">
      <v-form class="form" @submit="save">
        <coverage-selections-expansion-panel
          v-for="coverage in coverages"
          :key="coverage.coverage_label"
          :coverage="coverage"
          :label="coverage.coverage_label"
          @selections-change="selectionChangeHandler"
        />

        <div class="d-flex justify-center my-3">
          <v-btn depressed color="primary" type="submit" class="mx-3">
            Submit
          </v-btn>

          <v-btn depressed color="secondary" class="mx-3"> Reset </v-btn>
        </div>
      </v-form>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios.js";

import CoverageSelectionsExpansionPanel from "../../components/CoverageSelectionsExpansionPanel.vue";

export default {
  name: "Benefits",
  components: {
    CoverageSelectionsExpansionPanel,
  },
  props: {
    plan_id: {
      type: [String, Number],
      required: true,
    },
  },
  async mounted() {
    this.loaded = false;
    const res = await axios.get(
      `selections/plan/${this.plan_id}/benefit-product-variations`
    );
    this.coverages = [...res.data.coverages];
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      coverages: {},
      selections: {},
    };
  },
  computed: {
    output() {
      return this.selections;
    },
  },
  methods: {
    selectionChangeHandler(selections) {
      const selections_obj = {};
      console.log(selections);
      for (let sel of selections) {
        selections_obj[sel.code] = sel;
      }
      this.selections = { ...this.selections, ...selections_obj };
    },
    async save(event) {
      event.preventDefault();
      await axios.post("/selections/benefits", this.output);
    },
    async onSubmit(event) {
      event.preventDefault();
      await axios.post("/selections/benefits", this.selectionFormatter, {
        withCredentials: true,
      });
      this.$router.push({
        name: "age-bands",
        query: { plan_id: this.plan_id, plan_config_id: this.plan_config_id },
      });
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  position: relative;
}

.content {
  min-width: 70%;
  border: 1px solid #ddd;
  padding: 2rem;
  margin-right: 220px;
}
</style>
