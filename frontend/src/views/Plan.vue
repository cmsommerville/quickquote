<template>
  <div class="container">
    <div class="form-rater my-6" v-if="loaded">
      <v-form class="form" @submit="onSubmit" @reset="onReset" v-if="show">
        <v-btn-toggle v-model="selections.product_code" borderless class="my-3">
          <v-btn value="critical_illness">
            <span class="hidden-sm-and-down">Critical Illness</span>

            <v-icon right> mdi-heart-circle </v-icon>
          </v-btn>

          <v-btn value="accident">
            <span class="hidden-sm-and-down">Accident</span>

            <v-icon right> mdi-bone </v-icon>
          </v-btn>

          <v-btn value="hospital_indemnity">
            <span class="hidden-sm-and-down">Hospital Indemnity</span>

            <v-icon right> mdi-hospital-box </v-icon>
          </v-btn>

          <v-btn value="disability">
            <span class="hidden-sm-and-down">Disability</span>
            <v-icon right> mdi-cash-multiple </v-icon>
          </v-btn>
        </v-btn-toggle>

        <v-select
          :items="states"
          v-model="selections.rating_state"
          label="Rating State"
          class="my-3"
        ></v-select>

        <v-text-field
          v-model="selections.plan_effective_date"
          label="Plan Effective Date"
          type="date"
          class="my-3"
        ></v-text-field>

        <div class="d-flex justify-content my-3">
          <v-btn type="submit" color="primary" class="mx-3">Submit</v-btn>
          <v-btn type="reset" color="secondary" class="mx-3">Reset</v-btn>
        </div>
      </v-form>
    </div>
  </div>
</template>

<script>
const axios = require("axios");

export default {
  name: "Plan",
  data() {
    return {
      loaded: false,
      data: null,
      selections: {
        product_code: null,
        rating_state: null,
        plan_effective_date: null,
      },
      show: true,
    };
  },
  async mounted() {
    const res = await axios.get("http://localhost:5000/config/plans");
    this.data = [...res.data];
    this.loaded = true;
  },
  computed: {
    states() {
      if (this.selections.product_code) {
        const product = this.data.find(
          (product) => product.name === this.selections.product_code
        );
        return product.statesApproved.map((stateObj) => {
          return {
            value: stateObj.state,
            text: stateObj.state,
          };
        });
      }
      return ["AL", "AZ", "NC", "SC"];
    },
    config_id() {
      if (this.selections.product_code) {
        const product = this.data.find(
          (product) => product.name === this.selections.product_code
        );
        return product._id;
      }
      return null;
    },
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      const res = await axios.post(
        "http://localhost:5000/selections/plan",
        this.selections,
        {
          withCredentials: true,
        }
      );
      this.$router.push({
        name: "benefits",
        query: { plan_id: res.data.plan_id, plan_config_id: this.config_id },
      });
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.selections.product_name = null;
      this.selections.plan_effective_date = null;
      this.selections.rating_state = null;
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
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
