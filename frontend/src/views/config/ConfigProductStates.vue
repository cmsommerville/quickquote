<template>
  <div>
    <div class="mt-6">
      <v-list-item
        v-for="state in states"
        :key="state.code"
        dense
        class="state-item"
      >
        <v-select
          :items="stateInput"
          item-text="state_name"
          item-value="state_id"
          v-model="state.state_id"
          filled
          outlined
          dense
        ></v-select>

        <v-text-field
          v-model="state.state_effective_date"
          filled
          outlined
          dense
          type="date"
          :min="product_effective_date"
          :max="product_expiration_date"
          label="Effective Date"
        />
        <v-text-field
          v-model="state.state_expiration_date"
          filled
          outlined
          dense
          type="date"
          :min="product_effective_date"
          :max="product_expiration_date"
          label="Expiration Date"
        />
      </v-list-item>
    </div>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn color="primary" class="mx-4" @click="saveProductStates">
        Save
      </v-btn>
      <v-btn color="secondary" class="mx-4" @click="addStateInput">
        Add State
      </v-btn>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";

export default {
  name: "ConfigProductStates",
  data() {
    return {
      loaded: false,
      product_id: null,
      product_effective_date: "1900-01-01",
      product_expiration_date: "9999-12-31",
      stateInput: null,
      states: [],
      error: false,
    };
  },
  mounted() {
    this.loaded = false;
    if (this.$route.query.product_id) {
      this.product_id = this.$route.query.product_id;
      Promise.all([
        axios.get(`/config/product/state/${this.$route.query.product_id}`),
        axios.get("/config/ref-states"),
      ])
        .then(([states, stateInput]) => {
          if (states.data.length) {
            this.states = [...states.data];
            this.product_effective_date =
              states.data[0].product.product_effective_date ?? "1900-01-01";
            this.product_expiration_date =
              states.data[0].product.product_expiration_date ?? "1900-01-01";
          }
          this.stateInput = [...stateInput.data];

          this.loaded = true;
        })
        .catch((this.error = true));
    }
  },
  computed: {
    output() {
      return this.states.map((state) => {
        return {
          ...state,
          product_id: +this.product_id,
        };
      });
    },
  },
  methods: {
    routeTo(route_name) {
      this.$router.push({
        name: route_name,
        query: { product_id: this.product_id },
      });
    },
    addStateInput() {
      this.states = [
        ...this.states,
        {
          state_id: null,
          state_effective_date: this.product_effective_date,
          state_expiration_date: this.product_expiration_date,
        },
      ];
    },
    async saveProductStates() {
      await axios.post("/config/product/state", this.output);
      this.routeTo("config-product");
    },
  },
};
</script>

<style scoped>
.state-item {
  display: grid;
  grid-template-columns: 1fr 2fr 2fr;
  grid-template-rows: 10px;
  column-gap: 20px;
  row-gap: 20px;
}
</style>
