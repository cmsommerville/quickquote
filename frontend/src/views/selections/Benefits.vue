<template>
  <div class="container">
    <div class="content" v-if="loaded">
      <v-form class="form" @submit="save">
        <coverage-selections-expansion-panel
          v-for="coverage in coverages"
          :key="coverage.coverage_label"
          :coverage="coverage"
          :label="coverage.coverage_label"
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
      coverages: [],
    };
  },
  computed: {
    output() {
      // reduce list of coverages to list of benefits
      const bnfts_arr = this.coverages.reduce((prev, curr) => {
        return [...prev, ...curr.benefits];
      }, []);

      // format to match the database model for selection benefits
      const bnfts = bnfts_arr.map((bnft) => {
        const dur_arr = bnft.durations ?? [];
        return {
          selection_plan_id: +this.plan_id,
          config_benefit_id: bnft.config_benefit_id,
          config_rate_group_id: bnft.config_rate_group_id,
          benefit_value: bnft.ui_benefit_value,
          durations: dur_arr.map((dur) => {
            const selected_item = dur.duration_items.find((item) => {
              return item.item_code === dur.ui_duration_item_code;
            });

            return {
              selection_plan_id: +this.plan_id,
              config_benefit_duration_id: dur.benefit_duration_id,
              config_benefit_duration_item_id:
                selected_item.benefit_duration_item_id ?? null,
              duration_value: dur.ui_duration_item_code,
              duration_data_type: typeof dur.ui_duration_item_code,
              duration_factor: selected_item.benefit_duration_factor ?? 1,
            };
          }),
        };
      });

      return bnfts;
    },
  },
  methods: {
    async save(event) {
      event.preventDefault();
      await axios.post(
        `/selections/plan/${this.plan_id}/benefits`,
        this.output
      );
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
