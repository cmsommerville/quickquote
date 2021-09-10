<template>
  <div class="container">
    <div class="form-rater d-flex justify-center">
      <v-btn depressed color="primary" @click="createTables" class="my-3"
        >Create New Tables Only</v-btn
      >
      <v-spacer></v-spacer>
      <v-btn depressed color="warning" @click="dropCreateTables" class="my-3"
        >Drop and Recreate Tables</v-btn
      >

      <v-snackbar
        v-model="snackbar"
        :timeout="timeout"
        class="text-uppercase font-weight-black"
      >
        {{ data.message }}

        <template v-slot:action="{ attrs }">
          <v-btn
            color="secondary"
            text
            v-bind="attrs"
            @click="snackbar = false"
          >
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </div>
  </div>
</template>

<script>
const axios = require("axios");

export default {
  name: "CreateTables",
  data() {
    return {
      data: { message: null },
      snackbar: false,
      timeout: 5000,
    };
  },
  methods: {
    async createTables() {
      const res = await axios.get(
        "http://localhost:5000/admin/create-tables?drop='N'"
      );
      this.data = { ...res.data };
      this.snackbar = true;
    },
    async dropCreateTables() {
      const res = await axios.get(
        "http://localhost:5000/admin/create-tables?drop='Y'"
      );
      this.data = { ...res.data };
      this.snackbar = true;
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

.response {
  margin: 3rem 0;
}
</style>
