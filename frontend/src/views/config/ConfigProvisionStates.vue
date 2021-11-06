<template>
  <div>
    <v-card v-if="inherit">
      <v-card-title>States</v-card-title>
      <v-card-text
        >State applicability is inherited from the product level.</v-card-text
      >
    </v-card>
    <div v-if="!inherit">
      <v-list-item v-for="state in states" :key="state.code" dense>
        <v-row>
          <v-col sm="2" class="d-flex justify-center align-self-start">
            <v-select
              :items="stateInput"
              item-text="label"
              item-value="code"
              v-model="state.code"
              filled
              outlined
              dense
            ></v-select>
          </v-col>
          <v-col sm="3" class="d-flex justify-center align-self-start">
            <v-select
              :items="requirementTypes"
              item-text="label"
              item-value="code"
              v-model="state.value"
              filled
              outlined
              dense
            ></v-select>
          </v-col>

          <v-col sm="3" class="d-flex justify-center align-self-start">
            <v-text-field
              v-model="state.effectiveDate"
              filled
              outlined
              dense
              :disabled="state.value && state.value === 'prohibited'"
              type="date"
              label="Effective Date"
            />
          </v-col>

          <v-col sm="3" class="d-flex justify-center align-self-start">
            <v-text-field
              v-model="state.expiryDate"
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
      <v-btn
        v-if="inherit"
        color="secondary"
        class="mx-4"
        @click="overrideInheritedApplicability"
      >
        Override
      </v-btn>
      <v-btn
        v-if="!inherit"
        color="secondary"
        class="mx-4"
        @click="addStateInput"
      >
        Add State
      </v-btn>
      <v-btn v-if="!inherit" color="secondary" class="mx-4" @click="setInherit">
        Inherit State Applicability
      </v-btn>
    </div>
  </div>
</template>

<script>
import { STATES } from "../../data/lookups.js";

export default {
  name: "ConfigProvisionStates",
  props: {
    productId: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      inherit: false,
      config: null,
      stateInput: [...STATES],
      states: [],
      requirementTypes: [
        { code: "permitted", label: "Permitted" },
        { code: "prohibited", label: "Prohibited" },
        { code: "mandatory", label: "Mandatory" },
      ],
    };
  },
  mounted() {
    this.config = this.$store.getters.getProvisionConfig;
    if (this.config.states === "inherit") {
      this.inherit = true;
    } else {
      this.states = [...this.config.states];
    }
  },
  computed: {
    outputProvision() {
      return {
        ...this.config,
        states: this.inherit ? "inherit" : this.states,
      };
    },
  },
  methods: {
    routeToProvision() {
      this.$router.push({
        name: "config-provision",
        query: { code: this.config.name },
        params: { productId: this.productId },
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

<style></style>
