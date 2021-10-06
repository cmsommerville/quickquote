<template>
  <div class="container">
    <div class="form-rater" v-if="loaded">
      <v-form class="form" @submit="onSubmit">
        <div
          class="content-coverage"
          v-for="covg in coverages"
          :key="covg.name"
        >
          <coverage-selections-expansion-panel
            :coverage="covg"
            @selections-change="selectionChangeHandler"
          />
        </div>
        <div class="d-flex justify-center my-3">
          <v-btn depressed color="primary" type="submit" class="mx-3">
            Submit
          </v-btn>

          <v-btn depressed color="secondary" class="mx-3"> Reset </v-btn>
        </div>
      </v-form>
    </div>
    <selections-modal
      title="Customize Benefit Selections"
      :selections="selections"
      @customized-benefits="customBenefitsHandler"
    />
  </div>
</template>

<script>
import axios from "../services/axios.js";
import CoverageSelectionsExpansionPanel from "../components/CoverageSelectionsExpansionPanel.vue";
import SelectionsModal from "../components/SelectionsModal.vue";

export default {
  name: "Benefits",
  components: {
    CoverageSelectionsExpansionPanel,
    SelectionsModal,
  },
  data() {
    return {
      loaded: false,
      plan_config_id: null,
      plan_id: null,
      plan_config: null,
      selections: {},
    };
  },
  computed: {
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
    selectionFormatter() {
      const selections = [];

      for (const key in this.selections) {
        selections.push({
          plan_id: this.plan_id,
          coverage_code: this.selections[key].coverage_code,
          plan_rate_code: this.selections[key].plan_rate_code,
          benefit_code: this.selections[key].name,
          benefit_uuid: this.selections[key].uuid,
          benefit_value: this.selections[key].selectedValue,
        });
      }
      return selections;
    },
  },
  async mounted() {
    this.plan_config_id = this.$route.query.plan_config_id;
    this.plan_id = +this.$route.query.plan_id;

    const res = await axios.get(`/config/plan/${this.plan_config_id}`);
    this.plan_config = { ...res.data[0] };
    this.loaded = true;
  },
  methods: {
    customBenefitsHandler(payload) {
      this.selections[payload.name].selectedValue = payload.selectedValue;
    },
    selectionChangeHandler(selections) {
      const selections_obj = {};

      for (let sel of selections) {
        selections_obj[sel.name] = sel;
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
  align-items: center;
}

.form-rater {
  min-width: 60%;
  border: 1px solid #ddd;
  padding: 2rem;
}
</style>
