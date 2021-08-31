<template>
  <div class="container">
    <div class="form-rater" v-if="loaded">
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group label="Group Name:" label-for="input-group-name">
          <b-form-input
            id="input-group-name"
            v-model="data.selections.group_name"
            type="input"
            placeholder="Group Name"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group label="Group Size:" label-for="input-group-size">
          <b-form-input
            id="input-group-size"
            v-model.number="data.selections.group_size"
            type="number"
            placeholder="Enter group size"
          ></b-form-input>
        </b-form-group>

        <b-form-group label="SIC Code:" label-for="input-sic-code">
          <b-form-input
            id="input-sic-code"
            v-model="data.selections.sic_code"
            type="input"
            placeholder="SIC Code"
          ></b-form-input>
        </b-form-group>

        <b-form-group label="Tax ID:" label-for="input-tax-id">
          <b-form-input
            id="input-tax-id"
            v-model="data.selections.tax_id"
            type="input"
            placeholder="Group Tax ID"
          ></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </div>
  </div>
</template>

<script>
const axios = require("axios");

export default {
  name: "Group",
  data() {
    return {
      loaded: false,
      data: null,
      show: true,
    };
  },
  async mounted() {
    const res = await axios.get("http://localhost:5000/workflow/group", {
      withCredentials: true,
    });
    this.data = { ...res.data };
    this.loaded = true;
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      const res = await axios.post(
        "http://localhost:5000/workflow/group",
        this.data.selections,
        { withCredentials: true }
      );

      this.$router.push({
        name: "plan",
        query: { group_id: res.data.group_id },
      });
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.data.selections.group_size = null;
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
