<template>
  <div>
    <div>
      <v-list-item v-for="state in states" :key="state.code" dense>
        <v-row>
          <v-col sm="2" class="d-flex justify-center align-self-start">
            <v-select
              :items="stateInput"
              item-text="state_name"
              item-value="state_id"
              v-model="state.state_id"
              filled
              outlined
              dense
            ></v-select>
          </v-col>

          <v-col sm="3" class="d-flex justify-center align-self-start">
            <v-text-field
              v-model="state.benefit_effective_date"
              filled
              outlined
              dense
              type="date"
              label="Effective Date"
            />
          </v-col>

          <v-col sm="3" class="d-flex justify-center align-self-start">
            <v-text-field
              v-model="state.benefit_expiration_date"
              filled
              outlined
              dense
              type="date"
              label="Expiry Date"
            />
          </v-col>
        </v-row>
      </v-list-item>
    </div>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn color="primary" class="mx-4" @click="save"> Save </v-btn>
      <v-btn color="secondary" class="mx-4" @click="addStateInput">
        Add State
      </v-btn>
      <v-btn
        color="primary"
        class="mx-4"
        @click="routeTo('config-benefit', { benefit_id })"
      >
        Back
      </v-btn>
    </div>

    <v-snackbar
      v-model="snackbar"
      :timeout="5000"
      class="text-uppercase font-weight-black"
    >
      {{ snackbar_message }}

      <template v-slot:action="{ attrs }">
        <v-btn color="secondary" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import axios from "../../services/axios";
export default {
  name: "ConfigBenefitStates",
  props: {
    product_id: {
      type: Number,
      required: true,
    },
    benefit_id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      snackbar: false,
      snackbar_message: "",
      config: {},
      benefit: {},
      stateInput: [],
      states: [],
    };
  },
  async mounted() {
    this.loaded = false;

    const promise_bnft_state = axios.get(
      `/config/benefit-state/${this.benefit_id}`
    );
    const promise_states = axios.get("/config/ref-states");
    const promise_bnft = axios.get(`/config/benefit/${this.benefit_id}`);

    Promise.all([promise_bnft_state, promise_states, promise_bnft]).then(
      ([res_bnft_state, res_states, res_bnft]) => {
        this.states = [...res_bnft_state.data];
        this.stateInput = [
          ...res_states.data.filter((item) => item.state_code !== "XX"),
        ];
        this.benefit = { ...res_bnft.data };

        this.loaded = true;
      }
    );
  },
  computed: {
    output() {
      return [
        ...this.states.map((state) => {
          /* eslint-disable no-unused-vars */
          const { state_code, state_name, ...bnft } = state;
          /* eslint-enable no-unused-vars */
          return { ...bnft };
        }),
      ];
    },
  },
  methods: {
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        query: { ...params },
        params: { product_id: this.product_id, benefit_id: this.benefit_id },
      });
    },
    addStateInput() {
      this.states = [
        ...this.states,
        {
          state_id: null,
          benefit_effective_date: "1900-01-01",
          benefit_expiration_date: "9999-12-31",
          parent_id: this.benefit_id,
          product_id: this.product_id,
          benefit_code: this.benefit.benefit_code,
        },
      ];
    },
    async save() {
      try {
        await axios.post("/config/benefit", this.output);
        this.snackbar_message = "Saved to DB!";
        this.snackbar = true;
      } catch (err) {
        this.snackbar_message = err;
        this.snackbar = true;
      }
    },
  },
};
</script>

<style scoped></style>
