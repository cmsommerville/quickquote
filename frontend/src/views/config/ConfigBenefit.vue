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

            <v-text-field v-model="code" filled outlined label="Benefit Code" />

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
                title="Amounts"
                img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
                @click:configure="configureBenefit('config-benefit-amounts')"
              >
                Setup Benefit Amounts!
              </app-dashboard-card>
            </v-col>
          </v-row>

          <v-row>
            <v-col sm="12">
              <app-dashboard-card
                title="Duration"
                img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
                @click:configure="configureBenefit('config-benefit-durations')"
              >
                Vary by duration!
              </app-dashboard-card>
            </v-col>
          </v-row>

          <v-row>
            <v-col sm="12">
              <app-dashboard-card
                title="States"
                img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
                @click:configure="configureBenefit('config-benefit-states')"
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
                @click:configure="configureBenefit('config-benefit-factors')"
              >
                {{ `${factors.length} factor variations` }}
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
        @click="saveBenefit"
        :disabled="!formIsValid"
      >
        Save
      </v-btn>
    </div>
  </div>
</template>

<script>
import { COMPONENT_TYPES, INPUT_TYPES } from "../../data/lookups.js";
import AppModalListForm from "../../components/AppModalListForm.vue";
import AppDashboardCard from "../../components/AppDashboardCard.vue";

export default {
  name: "ConfigBenefit",
  props: {
    productId: {
      type: String,
      required: false,
    },
  },
  components: { AppModalListForm, AppDashboardCard },
  async mounted() {
    this.loaded = false;
    const bnft = await this.$store.getters.getBenefitConfig;

    this.config = { ...bnft };
    this.label = bnft.label ?? null;
    this.code = bnft.code ?? null;
    this.ui = bnft.ui ? { ...bnft.ui } : {};
    this.amounts = bnft.amounts ? { ...bnft.amounts } : {};
    this.factors = bnft.factors ? [...bnft.factors] : [];
    this.states = bnft.states ?? this.states;

    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      config: {},
      label: null,
      code: null,
      ui: {},
      amounts: {},
      factors: [],
      states: [
        { label: "Alabama", code: "AL", value: "permitted" },
        { label: "Alaska", code: "AK", value: "mandatory" },
        { label: "Arizona", code: "AZ", value: "prohibited" },
        { label: "Arkansas", code: "AR", value: "permitted" },
        { label: "North Carolina", code: "NC", value: "permitted" },
        { label: "South Carolina", code: "SC", value: "permitted" },
      ],
      componentTypes: [...COMPONENT_TYPES],
      inputTypes: [...INPUT_TYPES],
    };
  },
  computed: {
    formIsValid() {
      return !!this.label && !!this.code;
    },
    outputBenefit() {
      return {
        ...this.config,
        label: this.label,
        code: this.code,
        ui: { ...this.ui },
      };
    },
  },
  methods: {
    routeToBenefitRoute(name) {
      this.$router.push({
        name: name,
        params: { productId: this.productId },
      });
    },
    routeToBenefitList() {
      this.$router.push({
        name: "config-benefit-list",
        params: { productId: this.productId },
      });
    },
    storeBenefit() {
      this.$store.commit("SET_NEW_BENEFIT", this.outputBenefit);
    },
    saveBenefit() {
      this.storeBenefit();
      this.$store.dispatch("addNewBenefitToList");
      this.routeToBenefitList();
    },
    configureBenefit(route) {
      this.storeBenefit();
      this.routeToBenefitRoute(route);
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
