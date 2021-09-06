<template>
  <div class="container">
    <div class="form-rater my-6" v-if="loaded">
      <v-form @submit="onSubmit" @reset="onReset" v-if="show">
        <v-text-field
          v-model="data.selections.group_name"
          label="Group Name"
          required
        ></v-text-field>

        <v-text-field
          v-model.number="data.selections.group_size"
          label="Group Size"
          required
        ></v-text-field>

        <v-text-field
          v-model="data.selections.sic_code"
          label="SIC Code"
        ></v-text-field>

        <v-text-field
          v-model="data.selections.tax_id"
          label="Tax ID"
        ></v-text-field>

        <div class="d-flex justify-center">
          <v-btn depressed color="primary" type="submit" class="mx-3">
            Submit
          </v-btn>

          <v-btn depressed color="secondary" class="mx-3"> Reset </v-btn>
        </div>
      </v-form>
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
  min-width: 60%;
  border: 1px solid #ddd;
  padding: 2rem;
}
</style>
