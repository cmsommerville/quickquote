<template>
  <div class="container">
    <div class="form-rater" v-if="loaded">
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group
          id="input-group-1"
          label="Pre-Existing Condition Limitation:"
          label-for="input-prex"
        >
          <b-form-select
            id="input-prex"
            v-model="data.selections.prex"
            :options="inputPrex.options"
          ></b-form-select>
        </b-form-group>

        <b-form-checkbox
          v-model="data.selections.reductionAt70"
          name="check-button"
          switch
        >
          50% Reduction At Age 70
        </b-form-checkbox>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </div>
  </div>
</template>

<script>
const axios = require("axios");

export default {
  name: "ProductFactors",
  data() {
    return {
      loaded: false,
      data: null,
      show: true,
    };
  },
  async mounted() {
    const res = await axios.get(
      "http://localhost:5000/workflow/product-factors",
      {
        withCredentials: true,
      }
    );
    this.data = { ...res.data };
    this.loaded = true;
  },
  computed: {
    states() {
      return this.data.statesApproved.map((stateObj) => {
        return {
          value: stateObj.state,
          text: stateObj.state,
        };
      });
    },
    inputPrex() {
      return this.data.factors.filter((item) => item.id === "prex")[0];
    },
    inputReductionAt70() {
      return this.data.factors.filter((item) => item.id === "reductionAt70")[0];
    },
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      await axios.post(
        "http://localhost:5000/workflow/product-factors",
        this.data.selections,
        { withCredentials: true }
      );
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.data.selections.groupsize = null;
      this.data.selections.state = null;
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
  width: 60%;
  border: 1px solid #ddd;
  padding: 2rem;
}
</style>
