<template>
  <div class="container">
    <v-data-table
      v-if="benefit_rates && loaded"
      :headers="headers"
      :items="table_data"
      :items-per-page="10"
      :options="{
        sortBy: ['benefit_code', 'family_code', 'smoker_status', 'age_band_id'],
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
      benefit_rates: null,
      headers: [
        { text: "Benefit Code", value: "benefit_code" },
        { text: "Family Code", value: "family_code" },
        { text: "Smoker Status", value: "smoker_status" },
        { text: "Lower Age", value: "lower_age" },
        { text: "Upper Age", value: "upper_age" },
        { text: "Premium", value: "benefit_rate_premium" },
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
    const res = await axios.post(
      `/rating-calculator?plan_id=${this.plan_id}`,
      {},
      {
        withCredentials: true,
      }
    );
    this.benefit_rates = [
      ...res.data.map((bnft) => {
        return {
          ...bnft,
          benefit_code: bnft.benefit.benefit_code,
          benefit_selected_value: bnft.benefit.benefit_value,
          lower_age: bnft.age_band.lower_age,
          upper_age: bnft.age_band.upper_age,
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
