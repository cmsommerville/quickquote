<template>
  <div class="container">
    <div class="content">
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
  async mounted() {
    const res = await axios.get(`/selections/plan/${this.plan_id}/rates`, {});
    this.rate_group_summary = [
      ...res.data.map((item) => {
        return {
          ...item,
          _age_band: `${item.age_band.age_band_lower}-${item.age_band.age_band_upper}`,
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
