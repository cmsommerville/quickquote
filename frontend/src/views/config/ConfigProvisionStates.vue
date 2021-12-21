<template>
  <div>
    <div>
      <v-list-item
        v-for="state in states"
        :key="state.provision_state_applicability_id"
        dense
      >
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
              v-model="state.state_effective_date"
              filled
              outlined
              dense
              type="date"
              label="Effective Date"
            />
          </v-col>

          <v-col sm="3" class="d-flex justify-center align-self-start">
            <v-text-field
              v-model="state.state_expiration_date"
              filled
              outlined
              dense
              :disabled="state.value && state.value === 'prohibited'"
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
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";

export default {
  name: "ConfigProvisionStates",
  props: {
    provision_id: {
      required: true,
      type: [Number, String],
    },
    product_id: {
      required: true,
      type: [Number, String],
    },
  },
  data() {
    return {
      config: null,
      stateInput: [],
      states: [],
    };
  },
  mounted() {
    this.loaded = false;
    Promise.all([
      axios.get(
        `/qry-config/all-provision-states?provision_id=${this.provision_id}`
      ),
      axios.get("/config/ref-states"),
    ])
      .then(([states, stateInput]) => {
        this.initializeData(states.data);
        this.stateInput = [...stateInput.data];

        this.loaded = true;
      })
      .catch((this.error = true));
  },
  computed: {
    output() {
      return [
        ...this.states.map((state_obj) => {
          const { provision_state_availability_id, is_new, ...state } =
            state_obj;
          if (is_new) {
            return { ...state };
          }
          return { ...state, provision_state_availability_id };
        }),
      ];
    },
  },
  methods: {
    initializeData(config) {
      this.states = config.map((state) => {
        return { ...state };
      });
    },
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        params: {
          product_id: this.product_id,
          provision_id: this.provision_id,
        },
        query: { ...params },
      });
    },
    async save() {
      await axios.post(`/config/provision/state`, this.output);
      this.routeTo("config-provision", { provision_id: this.provision_id });
    },
    addStateInput() {
      this.states = [
        ...this.states,
        {
          provision_state_availability_id: Math.random(),
          is_new: true,
          provision_id: this.provision_id,
          state_id: null,
          state_effective_date: "1900-01-01",
          state_expiration_date: "9999-12-31",
        },
      ];
    },
  },
};
</script>

<style scoped></style>
