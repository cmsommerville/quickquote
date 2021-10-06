<template>
  <div class="container">
    <div class="content d-flex justify-center">
      <v-btn depressed color="primary" @click="createRateTables" class="my-3"
        >Insert Rate Tables</v-btn
      >

      <v-snackbar
        v-model="snackbar"
        :timeout="timeout"
        class="text-uppercase font-weight-black"
      >
        {{ message }}

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
import axios from "../../services/axios.js";
import { rateTables } from "../../data/rateTable.js";

export default {
  name: "InsertRateTables",
  data() {
    return {
      snackbar: false,
      timeout: 5000,
      message: "Rate Tables Inserted",
    };
  },
  methods: {
    async createRateTables() {
      console.log(rateTables);
      await axios.post("/config/rate-table", rateTables);
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

.content {
  min-width: 60%;
  border: 1px solid #ddd;
  padding: 2rem;
}

.response {
  margin: 3rem 0;
}
</style>
