<template>
  <div class="container">
    <div class="form-rater">
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group
          id="input-group-1"
          label="Group Size:"
          label-for="input-group-size"
        >
          <b-form-input
            id="input-group-size"
            v-model.number="form.groupsize"
            type="number"
            placeholder="Enter group size"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-checkbox
          id="input-pre"
          v-model="form.prex"
          name="check-button"
          switch
        >
          Pre-Existing Conditions
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
      form: {
        groupsize: null,
        prex: true,
      },
      show: true,
    };
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      const res = await axios.post(
        "http://localhost:5000/workflow/product-factors",
        this.form
      );
      console.log(res);
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.form.prex = true;
      this.form.groupsize = null;
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
};
</script>

<style>
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
