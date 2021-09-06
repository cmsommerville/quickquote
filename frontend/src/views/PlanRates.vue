<template>
  <div class="container">
    <div class="form-rater d-flex flex-column" v-if="loaded">
      <div class="d-flex flex-column my-6 align-center">
        <v-btn
          depressed
          color="primary"
          type="button"
          class="mx-3"
          @click="planRateHandler"
        >
          Generate Plan Rates
        </v-btn>
        <p v-if="text.plan_rates" class="my-3 warning--text">
          {{ text.plan_rates }}
        </p>
      </div>
      <div class="d-flex flex-column my-6 align-center">
        <v-btn
          depressed
          color="primary"
          type="button"
          class="mx-3"
          @click="factorHandler"
        >
          Generate Factors
        </v-btn>
        <p v-if="text.factors" class="my-3 warning--text">
          {{ text.factors }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require("axios");

export default {
  name: "PlanRates",
  data() {
    return {
      loaded: false,
      text: { plan_rates: null, factors: null },
    };
  },
  async mounted() {
    this.plan_id = +this.$route.query.plan_id || null;
    this.loaded = true;
  },
  methods: {
    async planRateHandler() {
      this.loaded = false;
      await axios.post("http://localhost:5000/workflow/plan-rate", null, {
        params: { plan_id: this.plan_id },
        withCredentials: true,
      });

      this.text.plan_rates = "Plan Rates Generated!";
      this.loaded = true;
    },

    async factorHandler() {
      this.loaded = false;
      await axios.post("http://localhost:5000/workflow/factor-calc", null, {
        params: { plan_id: this.plan_id },
        withCredentials: true,
      });
      this.text.factors = "Factors Generated!";
      this.loaded = true;
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
