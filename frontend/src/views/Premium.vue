<template>
  <div class="container">
    <div class="content">
      <div class="rate-table-grid" v-if="plan_rates && loaded">
        <v-card class="rate-table" v-for="(tbl, key) in table_data2" :key="key">
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
    </div>
  </div>
</template>

<script>
const _ = require("lodash");
import axios from "../services/axios.js";

export default {
  name: "Premium",
  data() {
    return {
      loaded: false,
      plan_rates: null,
      headers: [
        { text: "Family Code", value: "family_code" },
        { text: "Smoker Status", value: "smoker_status" },
        { text: "Age Band", value: "age_band" },
        { text: "Rate", value: "plan_rate_premium" },
      ],
      plan_id: null,
      show: true,
    };
  },
  computed: {
    table_data() {
      return this.plan_rates.map((br) => {
        return {
          ...br,
        };
      });
    },
    table_data2() {
      return _.groupBy(this.plan_rates, (obj) => {
        return obj.family_code + "-" + obj.smoker_status;
      });
    },
  },
  async mounted() {
    this.plan_id = this.$route.query.plan_id;
    const res = await axios.post(
      `/rating-calculator?plan_id=${this.plan_id}`,
      {}
    );
    this.plan_rates = [
      ...res.data.map((pr) => {
        return {
          ...pr,
          age_band: pr.age_band.lower_age + " - " + pr.age_band.upper_age,
        };
      }),
    ];
    this.loaded = true;
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      console.log("clicked");
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
