<template>
  <div>
    <div class="mb-4" v-if="loaded">
      <v-row>
        <v-col sm="5">
          <v-form>
            <v-text-field
              v-model="label"
              filled
              outlined
              label="Benefit Name"
            />

            <v-text-field v-model="name" filled outlined label="Benefit Code" />

            <v-row>
              <v-col :sm="ui.component === 'v-select' ? 9 : 12">
                <v-select
                  v-model="ui.component"
                  filled
                  outlined
                  label="Component Type"
                  :items="componentTypes"
                  item-text="label"
                  item-value="code"
                />
              </v-col>
              <v-col v-if="ui.component === 'v-select'" sm="3">
                <app-modal-list-form
                  v-if="ui.component === 'v-select'"
                  title="Select Options"
                  :schema="[
                    { code: 'text', label: 'Label' },
                    { code: 'value', label: 'Value' },
                  ]"
                  @submit:list-data="selectListItemsHandler"
                  class="ma-2"
                >
                  <v-icon>mdi-pencil-outline</v-icon>
                </app-modal-list-form>
              </v-col>
            </v-row>

            <v-select
              v-if="ui.component === 'v-text-field'"
              v-model="ui.type"
              filled
              outlined
              label="Input Type"
              :items="inputTypes"
              item-text="label"
              item-value="code"
            />
          </v-form>
        </v-col>
        <v-col></v-col>
        <v-col sm="6" class="d-flex flex-column">
          <v-row>
            <v-col sm="12">
              <app-dashboard-card
                title="States"
                img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
                @click:configure="configureStates"
              >
                {{
                  states === "inherit"
                    ? "Applicability inherited"
                    : states.length
                    ? `${states.length} states configured`
                    : "Setup States!"
                }}
              </app-dashboard-card>
            </v-col>
          </v-row>

          <v-row>
            <v-col sm="12">
              <app-dashboard-card
                title="Factors"
                img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
                @click:configure="configureRateTables"
              >
                {{
                  config && config.factor
                    ? `${config.factor.variability.length} factor variations`
                    : "Setup Rate Tables!"
                }}
              </app-dashboard-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </div>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn
        color="primary"
        class="mx-4"
        @click="saveProvision"
        :disabled="!formIsValid"
      >
        Save
      </v-btn>
    </div>
  </div>
</template>

<script>
import AppModalListForm from "../../components/AppModalListForm.vue";
import AppDashboardCard from "../../components/AppDashboardCard.vue";

export default {
  name: "ConfigProvision",
  props: {
    productId: {
      type: String,
      required: false,
    },
  },
  components: { AppModalListForm, AppDashboardCard },
  async mounted() {
    this.loaded = false;
    const code = this.$route.query.code;
    if (code) {
      const prov = await this.$store.getters.getProvisionConfig;
      // if (prov) {
      this.config = { ...prov };
      this.label = prov.label;
      this.name = prov.name;
      this.ui = { ...prov.ui };
      this.states = prov.states ? prov.states : this.states;
      // }
    }
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      modal: false,
      config: null,
      label: null,
      name: null,
      ui: {},
      states: [
        { label: "Alabama", code: "AL", value: "permitted" },
        { label: "Alaska", code: "AK", value: "mandatory" },
        { label: "Arizona", code: "AZ", value: "prohibited" },
        { label: "Arkansas", code: "AR", value: "permitted" },
        { label: "North Carolina", code: "NC", value: "permitted" },
        { label: "South Carolina", code: "SC", value: "permitted" },
      ],

      componentTypes: [
        { code: "v-text-field", label: "Input" },
        { code: "v-select", label: "Select" },
        { code: "v-checkbox", label: "Checkbox" },
        { code: "v-radio", label: "Radio" },
        { code: "v-switch", label: "Switch" },
      ],
      inputTypes: [
        { code: "text", label: "Text" },
        { code: "number", label: "Number" },
        { code: "date", label: "Date" },
        { code: "email", label: "Email" },
        { code: "password", label: "Password" },
      ],
    };
  },
  computed: {
    formIsValid() {
      return !!this.label && !!this.name;
    },
    stateAvailabilityList() {
      return {
        permitted: {
          color: "primary",
          states: this.states.filter((state) => state.value === "permitted"),
        },
        mandatory: {
          color: "teal",
          states: this.states.filter((state) => state.value === "mandatory"),
        },
        prohibited: {
          color: "red",
          states: this.states.filter((state) => state.value === "prohibited"),
        },
      };
    },
    outputProvision() {
      return {
        ...this.config,
        label: this.label,
        name: this.name,
        ui: { ...this.ui },
        states: this.states,
      };
    },
  },
  methods: {
    routeToProvisionList() {
      this.$router.push({
        name: "config-provision-list",
        params: { productId: this.productId },
      });
    },
    routeToProvisionFactors() {
      this.$router.push({
        name: "config-provision-factors",
        params: { productId: this.productId },
        query: { code: this.name },
      });
    },
    routeToProvisionStates() {
      this.$router.push({
        name: "config-provision-states",
        params: { productId: this.productId },
        query: { code: this.name },
      });
    },
    storeProvision() {
      this.$store.commit("SET_NEW_PROVISION", this.outputProvision);
    },
    configureStates() {
      this.storeProvision();
      this.routeToProvisionStates();
    },
    configureFactors() {
      this.storeProvision();
      this.routeToProvisionFactors();
    },
    saveProvision() {
      this.storeProvision();
      this.$store.dispatch("addNewProvisionToList");
      this.routeToProvisionList();
    },
    selectListItemsHandler(payload) {
      this.ui.items = [...payload];
    },
  },
};
</script>

<style>
.card-state {
  position: relative;
}

.btn-edit {
  position: absolute;
  top: -15px;
  right: -15px;
}
</style>
