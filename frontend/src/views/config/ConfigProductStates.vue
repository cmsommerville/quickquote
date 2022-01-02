<template>
  <div>
    <div class="mt-6">
      <v-list-item
        v-for="state in product_states"
        :key="state.code"
        dense
        class="state-item"
      >
        <v-select
          :items="states"
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
          :min="product.product_effective_date"
          :max="product.product_expiration_date"
          label="Effective Date"
        />
        <v-text-field
          v-model="state.state_expiration_date"
          filled
          outlined
          dense
          type="date"
          :min="product.product_effective_date"
          :max="product.product_expiration_date"
          label="Expiration Date"
        />
      </v-list-item>
    </div>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn color="primary" class="mx-4" @click="save"> Save </v-btn>
      <v-btn color="primary" class="mx-4" outlined @click="addStateInput">
        Add State
      </v-btn>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";

export default {
  name: "ConfigProductStates",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
  },
  data() {
    return {
      loaded: false,
      product: {},
      product_states: [],
      states: [],
      error: false,
    };
  },
  mounted() {
    this.loaded = false;
    Promise.all([
      axios.get(`/qry-config/all-product-states?product_id=${this.product_id}`),
      axios.get("/config/ref-states"),
      axios.get(`/config/product/${this.product_id}`),
    ])
      .then(([states, stateInput, product]) => {
        this.product = { ...product.data };
        this.product_states = [...states.data];
        this.states = [...stateInput.data];
        this.loaded = true;
      })
      .catch((this.error = true));
  },
  computed: {
    output() {
      return this.product_states.map((state) => {
        return {
          ...state,
          product_id: +this.product_id,
        };
      });
    },
  },
  methods: {
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        params: { product_id: this.product_id },
        query: { ...params },
      });
    },
    addStateInput() {
      this.product_states = [
        ...this.product_states,
        {
          product_id: this.product_id,
          state_id: null,
          state_effective_date: this.product.product_effective_date,
          state_expiration_date: this.product.product_expiration_date,
        },
      ];
    },
    async save() {
      await axios.post("/config/product/states", this.output);
      this.routeTo("config-product", { product_id: this.product_id });
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
