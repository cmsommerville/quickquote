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
      <v-btn color="primary" class="mx-4" @click="submitProvisionStates">
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
  name: "ConfigProvisionStates",
  data() {
    return {
      inherit: false,
      config: null,
      stateInput: [],
      states: [],
      requirementTypes: [
        { code: "permitted", label: "Permitted" },
        { code: "prohibited", label: "Prohibited" },
        { code: "mandatory", label: "Mandatory" },
      ],
    };
  },
  mounted() {
    this.loaded = false;
    if (this.$route.query.provision_id) {
      this.product_id = this.$route.query.product_id;
      this.provision_id = this.$route.query.provision_id;
      Promise.all([
        axios.get(`/config/provision/state/${this.$route.query.provision_id}`),
        axios.get("/config/ref-states"),
      ])
        .then(([states, stateInput]) => {
          if (states.data.length) {
            this.states = [...states.data];
            this.provision_effective_date =
              states.data[0].provision.provision_effective_date ?? "1900-01-01";
            this.provision_expiration_date =
              states.data[0].provision.provision_expiration_date ??
              "1900-01-01";
          }
          this.stateInput = [...stateInput.data];

          this.loaded = true;
        })
        .catch((this.error = true));
    }
  },
  computed: {
    output() {
      return {
        ...this.config,
      };
    },
  },
  methods: {
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        query: { product_id: this.product_id, ...params },
      });
    },
    addStateInput() {
      this.states = [
        ...this.states,
        {
          code: "",
          value: "permitted",
          effectiveDate: "1900-01-01",
          expiryDate: "9999-12-31",
        },
      ];
    },
    submitProvisionStates() {
      this.$store.commit("SET_NEW_PROVISION", this.outputProvision);
      this.routeToProvision();
    },
    overrideInheritedApplicability() {
      this.inherit = false;
      this.addStateInput();
    },
    setInherit() {
      this.inherit = true;
      this.states = [];
    },
  },
};
</script>

<style scoped></style>
