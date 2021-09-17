<template>
  <div class="container">
    <v-data-table
      v-if="benefit_rates && loaded"
      :headers="headers"
      :items="table_data"
      :items-per-page="10"
      :options="{
        sortBy: ['benefit_id', 'family_code', 'smoker_status', 'age_band_id'],
      }"
      class="elevation-1"
    ></v-data-table>
  </div>
</template>

<script>
const axios = require("axios");

export default {
  name: "Premium",
  data() {
    return {
      loaded: false,
      benefit_rates: null,
      headers: [
        { text: "Benefit ID", value: "benefit_id" },
        { text: "Family Code", value: "family_code" },
        { text: "Smoker Status", value: "smoker_status" },
        { text: "Age Band ID", value: "age_band_id" },
        { text: "Premium", value: "benefit_rate_final_premium" },
      ],
      plan_id: null,
      show: true,
    };
  },
  computed: {
    table_data() {
      return this.benefit_rates.map((br) => {
        return {
          ...br,
        };
      });
    },
  },
  async mounted() {
    this.plan_id = this.$route.query.plan_id;
    const res = await axios.get(
      `http://localhost:5000/rating-calculator?plan_id=${this.plan_id}`
    );
    this.benefit_rates = [...res.data];
    this.loaded = true;
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      await axios.post(
        "http://localhost:5000/selections/provisions",
        this.selectionHandler,
        {
          withCredentials: true,
        }
      );
      this.$router.push({
        name: "plan-rate",
        query: { plan_id: this.plan_id },
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
