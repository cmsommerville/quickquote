<template>
  <div class="container">
    <div class="form-rater" v-if="loaded">
      <v-form class="form" @submit="onSubmit" @reset="onReset">
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
      :columnDefs="benefitsGrid.columnDefs"
      :rowData="benefitsGrid.rowData"
      @customized-benefits="customBenefitsHandler"
    />
  </div>
</template>

<script>
const axios = require("axios");
import CoverageSelectionsExpansionPanel from "../components/CoverageSelectionsExpansionPanel.vue";
import SelectionsModal from "../components/SelectionsModal.vue";

function numberParser(params) {
  return Number(params.newValue);
}

export default {
  name: "Benefits",
  components: { CoverageSelectionsExpansionPanel, SelectionsModal },
  data() {
    return {
      fab: false,
      loaded: false,
      plan_config_id: null,
      plan_id: null,
      plan_config: null,
      selections: {},
    };
  },
  computed: {
    benefits() {
      return this.plan_config.benefits;
    },
    benefitsGrid() {
      const columnDefs = [
        { headerName: "Benefit Code", field: "name", hide: true },
        { headerName: "Benefit Name", field: "text" },
        {
          headerName: "Selected Amount",
          field: "amount",
          editable: true,
          valueParser: numberParser,
        },
        { headerName: "Unit", field: "unit" },
      ];
      if (this.plan_config) {
        return {
          columnDefs: columnDefs,
          rowData: this.plan_config.benefits.map((bnft) => {
            return {
              name: bnft.name,
              text: bnft.text,
              amount: bnft.amounts.default,
              unit: bnft.amounts.unit === "percent" ? "%" : "$",
            };
          }),
        };
      }
      return {
        columnDefs: columnDefs,
        rowData: [],
      };
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
    selectionHandler() {
      return this.benefits
        .filter((bnft) => Object.keys(this.selections).includes(bnft.name))
        .map((item) => {
          return {
            plan_id: this.plan_id,
            coverage_code: item.coverage_code,
            benefit_code: item.name,
            benefit_uuid: item.uuid,
            benefit_value: this.selections[item.name],
          };
        });
    },
  },
  async mounted() {
    this.plan_config_id = this.$route.query.plan_config_id;
    this.plan_id = +this.$route.query.plan_id;

    const res = await axios.get(
      `http://localhost:5000/config/plan/${this.plan_config_id}`
    );
    this.plan_config = { ...res.data[0] };
    this.loaded = true;
  },
  methods: {
    customBenefitsHandler(payload) {
      this.selections[payload.name] = payload.amount;
    },
    selectionChangeHandler(selections) {
      this.selections = { ...this.selections, ...selections };
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
