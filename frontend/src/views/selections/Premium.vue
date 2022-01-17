<template>
  <div class="container">
    <div class="content">
      <div class="distributions mb-6 d-flex justify-space-between">
        <v-slider
          v-model="weightNonSmoker"
          :min="0"
          :max="100"
          :thumb-size="24"
          thumb-label="always"
          label="% Non-Smoker"
          class="align-center mr-6"
          @mouseup="setSmokerStatus"
        >
        </v-slider>

        <v-slider
          v-model="weightMale"
          :min="0"
          :max="100"
          :thumb-size="24"
          thumb-label="always"
          label="% Male"
          class="align-center"
          @mouseup="setGender"
        >
        </v-slider>
      </div>
      <div class="rate-table-grid" v-if="rate_group_summary && loaded">
        <v-card class="rate-table" v-for="(tbl, key) in table_data" :key="key">
          <v-card-title> Rates: {{ key }} </v-card-title>
          <v-data-table
            :headers="headers"
            :items="tbl"
            :options="{
              sortBy: ['family_code', 'smoker_status', 'age_band'],
            }"
            class="elevation-1"
          ></v-data-table>
        </v-card>
      </div>
      <div class="action-buttons mt-6 d-flex justify-center align-center">
        <v-btn @click="calculateRates" color="primary">Calculate</v-btn>
      </div>
    </div>
  </div>
</template>

<script>
const _ = require("lodash");
import axios from "../../services/axios.js";

export default {
  name: "Premium",
  props: {
    plan_id: {
      required: true,
      type: [String, Number],
    },
  },
  data() {
    return {
      loaded: false,
      rate_group_summary: [],
      weightNonSmoker: null,
      weightMale: null,
      headers: [
        { text: "Family Code", value: "family_code" },
        { text: "Smoker Status", value: "smoker_status" },
        { text: "Age Band", value: "_age_band" },
        { text: "Rate", value: "rate_group_premium" },
      ],
    };
  },
  computed: {
    table_data() {
      return _.groupBy(this.rate_group_summary, (obj) => {
        return obj.family_code + "-" + obj.smoker_status;
      });
    },
  },
  mounted() {
    const p_rates = axios.get(`/selections/plan/${this.plan_id}/rates`);
    const p_dist = axios.get(`/selections/plan/${this.plan_id}/dist`);

    Promise.all([p_rates, p_dist]).then(([rates, dist]) => {
      this.rate_group_summary = [
        ...rates.data.map((item) => {
          return {
            ...item,
            _age_band: `${item.age_band.age_band_lower}-${item.age_band.age_band_upper}`,
          };
        }),
      ];
      this.loaded = true;

      this.weightNonSmoker = this.distributionHandler(
        dist.data,
        "smoker_status",
        "N"
      );
      this.weightMale = this.distributionHandler(dist.data, "gender", "M");
    });
  },
  methods: {
    distributionHandler(data, attr_type_code, attr_value) {
      const denom = data
        .filter((item) => {
          return item.attr_type_code === attr_type_code;
        })
        .reduce((prev, curr) => {
          return prev.weight + curr.weight;
        });

      const num = data.find(
        (item) =>
          item.attr_type_code === attr_type_code &&
          item.attr_value === attr_value
      ).weight;

      console.log({ num, denom });

      return (num / denom) * 100;
    },
    async setSmokerStatus() {
      await axios.post(
        `/selections/plan/${this.plan_id}/dist?pct_ns=${this.weightNonSmoker}`
      );
    },
    async setGender() {
      await axios.post(
        `/selections/plan/${this.plan_id}/dist?pct_m=${this.weightMale}`
      );
    },
    async calculateRates() {
      const rates = await axios.get(`/selections/plan/${this.plan_id}/rates`);
      this.rate_group_summary = [
        ...rates.data.map((item) => {
          return {
            ...item,
            _age_band: `${item.age_band.age_band_lower}-${item.age_band.age_band_upper}`,
          };
        }),
      ];
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

.content {
  min-width: 90%;
  border: 1px solid #ddd;
  padding: 2rem;
}

.rate-table-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  grid-gap: 2rem;
  align-items: center;
  justify-items: center;
  margin: 0 auto;
}
</style>
