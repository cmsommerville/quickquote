<template>
  <div class="container">
    <div class="content" v-if="loaded">
      <div class="form-item buttons">
        <b-button variant="primary" @click="planRateHandler"
          >Generate Plan Rates</b-button
        >
        <p v-if="text.plan_rates">{{ text.plan_rates }}</p>
      </div>
      <div class="form-item buttons">
        <b-button variant="secondary" @click="factorHandler"
          >Generate Factors</b-button
        >
        <p v-if="text.factors">{{ text.factors }}</p>
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

.content {
  width: 60%;
  border: 1px solid #ddd;
  padding: 2rem;
}

.form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.form-item {
  margin: 0.5rem;
}

.tile-wrapper {
  width: 200px;
  height: 200px;
  border: 1px solid #ddd;
  border-radius: 20px;
  cursor: pointer;
  position: relative;
  background: rgb(243, 222, 249);

  display: flex;
  justify-content: center;
  align-items: center;
}

.tile-wrapper input {
  cursor: pointer;
  position: absolute;
  height: 100%;
  width: 100%;
  opacity: 0;
}

.tile-wrapper label {
  font-size: 2.2rem;
}
</style>
