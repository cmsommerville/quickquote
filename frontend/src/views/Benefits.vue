<template>
  <div class="container">
    <div class="form-rater" v-if="loaded">
      <v-form class="form" @submit="onSubmit" @reset="onReset" v-if="show">
        <div
          class="content-coverage"
          v-for="covg in coverages"
          :key="covg.name"
        >
          <div class="d-flex justify-space-between">
            <v-switch
              v-model="coverage_selections[covg.name]"
              :label="covg.text"
              @change="toggleCoverage(covg)"
            >
            </v-switch>
            <v-btn color="primary" fab dark small @click="showCoverage(covg)">
              <v-icon>mdi-menu-down-outline</v-icon>
            </v-btn>
          </div>
          <div class="content-benefits ml-6" v-if="showBenefitsPane[covg.name]">
            <v-switch
              v-for="benefit in covg.benefits"
              :key="benefit.name"
              v-model="benefit_selections[benefit.name]"
              :label="benefit.text"
              :false-value="0"
              :true-value="benefit.default"
            >
            </v-switch>
          </div>
        </div>
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
const axios = require("axios");

export default {
  name: "Benefits",
  data() {
    return {
      loaded: false,
      plan_config_id: null,
      plan_id: null,
      plan_config: null,
      coverage_selections: {},
      benefit_selections: {},
      show: {},
      hidden: false,
    };
  },
  computed: {
    showBenefitsPane() {
      return this.show;
    },
    coverages() {
      let covg_index;
      const coverages = [...this.plan_config.coverages];
      this.plan_config.benefits.map((bnft) => {
        covg_index = coverages.findIndex(
          (covg) => covg.name === bnft.coverage_code
        );
        if (coverages[covg_index].benefits) {
          coverages[covg_index].benefits = [
            ...coverages[covg_index].benefits,
            bnft,
          ];
        } else {
          coverages[covg_index].benefits = [bnft];
        }
      });

      return coverages;
    },
    benefits() {
      return this.plan_config.benefits;
    },
    selectionHandler() {
      return this.benefits
        .filter((bnft) =>
          Object.keys(this.benefit_selections).includes(bnft.name)
        )
        .map((item) => {
          return {
            plan_id: this.plan_id,
            coverage_code: item.coverage_code,
            benefit_code: item.name,
            benefit_uuid: item.uuid,
            benefit_value: this.benefit_selections[item.name],
          };
        });
    },
  },
  async mounted() {
    this.plan_config_id = this.$route.query.plan_config_id;
    const res = await axios.get(
      `http://localhost:5000/config/plan/${this.plan_config_id}`
    );
    this.plan_id = +this.$route.query.plan_id;
    this.plan_config = { ...res.data[0] };

    this.benefit_selections = [...res.data[0].benefits].reduce(
      (acc, curr) => ((acc[curr.name] = curr.amounts.default), acc),
      {}
    );

    for (let coverage of res.data[0].coverages) {
      this.coverage_selections[coverage.name] = coverage.default;
      this.show[coverage.name] = false;
    }

    for (let coverage of this.coverages) {
      this.toggleCoverage(coverage);
    }
    this.loaded = true;
  },
  methods: {
    showCoverage(coverage) {
      this.show[coverage.name] = !this.show[coverage.name];
      console.log(this.show);
    },
    toggleCoverage(coverage) {
      const selected = this.coverage_selections[coverage.name];
      coverage.benefits.map((bnft) => {
        this.benefit_selections[bnft.name] = selected
          ? bnft.amounts.default
          : 0;
      });
    },
    async onSubmit(event) {
      event.preventDefault();
      await axios.post(
        "http://localhost:5000/selections/benefits",
        this.selectionHandler,
        {
          withCredentials: true,
        }
      );
      this.$router.push({
        name: "age-bands",
        query: { plan_id: this.plan_id, plan_config_id: this.plan_config_id },
      });
    },
    onReset(event) {
      event.preventDefault();
      console.log(this.selectionSubmissionHandler());
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-rater {
  min-width: 60%;
  border: 1px solid #ddd;
  padding: 2rem;
}
</style>
