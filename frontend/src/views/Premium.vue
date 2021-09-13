<template>
  <div class="container">
    <v-data-table
      v-if="benefit_rates && loaded"
      :headers="headers"
      :items="benefit_rates"
      :items-per-page="10"
      :options="{ sortBy: ['family_code', 'smoker_status', 'age'] }"
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
        { text: "Family Code", value: "family_code" },
        { text: "Smoker Status", value: "smoker_status" },
        { text: "Age", value: "age" },
        { text: "Premium", value: "benefit_rate_final_premium" },
      ],
      plan_id: null,
      show: true,
    };
  },
  computed: {
    provisions() {
      return this.plan_config.provisions;
    },
    provisions_object() {
      return this.provisions.reduce(
        (obj, item) => Object.assign(obj, { [item.name]: item }),
        {}
      );
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
