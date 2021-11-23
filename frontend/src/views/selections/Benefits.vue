<template>
  <div class="container">
    <div class="content" v-if="loaded">
      <v-form class="form" @submit="onSubmit">
        <coverage-selections-expansion-panel
          v-for="coverage in coverages"
          :key="coverage.label"
          :coverage="coverage"
          :label="coverage.label"
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
  data() {
    return {
      loaded: false,
      plan_config_id: null,
      plan_id: null,
      plan_config: {},
      coverages: [],
      plan: {},
      selections: {},
    };
  },
  computed: {
    selectionFormatter() {
      const selections = [];

      for (const key in this.selections) {
        const sel = {
          plan_id: this.plan_id,
          coverage_code: this.selections[key].coverage_code,
          plan_rate_code: this.selections[key].plan_rate_code,
          benefit_code: this.selections[key].code,
          benefit_uuid: this.selections[key].uuid,
          benefit_value: this.selections[key].selectedValue,
        };
        if (this.selections[key].durations) {
          sel["durations"] = this.selections[key].durations.map((dur) => {
            return {
              plan_id: this.plan_id,
              duration_code: dur.code,
              duration_data_type:
                dur.selectedDuration &&
                (typeof dur.selectedDuration.value ?? null),
              duration_value:
                dur.selectedDuration && (dur.selectedDuration.value ?? null),
              duration_factor:
                dur.selectedDuration && (dur.selectedDuration.factor ?? null),
            };
          });
        }
        selections.push(sel);
      }
      return selections;
    },
  },
  async mounted() {
    this.loaded = false;
    this.plan_config_id = this.$route.query.plan_config_id;
    this.plan_id = +this.$route.query.plan_id;
    const res = await axios.get("/selections/benefits", {
      params: { plan_config_id: this.plan_config_id, plan_id: this.plan_id },
    });
    this.coverages = [...res.data.coverages];
    this.plan_config = { ...res.data.plan_config };
    this.plan = { ...res.data.plan };
    this.loaded = true;
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
