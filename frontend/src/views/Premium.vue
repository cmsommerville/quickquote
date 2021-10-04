<template>
  <div class="container">
    <v-data-table
      v-if="plan_rates && loaded"
      :headers="headers"
      :items="table_data"
      :items-per-page="10"
      :options="{
        sortBy: ['plan_rate_code', 'family_code', 'smoker_status', 'age_band'],
      }"
      class="elevation-1"
    ></v-data-table>
  </div>
</template>

<script>
import axios from "../services/axios.js";

export default {
  name: "Premium",
  data() {
    return {
      loaded: false,
      plan_rates: null,
      headers: [
        { text: "Plan Rate Code", value: "plan_rate_code" },
        { text: "Family Code", value: "family_code" },
        { text: "Smoker Status", value: "smoker_status" },
        { text: "Age Band", value: "age_band" },
        { text: "Premium", value: "plan_rate_premium" },
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

.form-rater {
  min-width: 60%;
  border: 1px solid #ddd;
  padding: 2rem;
}
</style>
