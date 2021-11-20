<template>
  <div class="container">
    <div class="content">
      <v-row v-if="loaded">
        <v-col></v-col>
        <v-col sm="6">
          <v-form>
            <v-text-field
              v-model="label"
              filled
              outlined
              label="Duration Name"
            />

            <v-text-field
              v-model="code"
              filled
              outlined
              label="Duration Code"
            />

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
                    { code: 'factor', label: 'Factor' },
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
      </v-row>
      <v-divider></v-divider>
      <v-row class="mt-4">
        <v-col sm="12">
          <div class="call-to-action d-flex justify-center align-center">
            <v-btn @click="saveHandler" color="primary" class="mx-4">
              Save Benefit Durations
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import { COMPONENT_TYPES, INPUT_TYPES } from "../../data/lookups.js";
import AppModalListForm from "../../components/AppModalListForm.vue";

export default {
  name: "ConfigBenefitDurations",
  components: {
    AppModalListForm,
  },
  props: {
    productId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      loaded: false,
      label: null,
      code: null,
      ui: null,
      componentTypes: [...COMPONENT_TYPES],
      inputTypes: [...INPUT_TYPES],
    };
  },
  async mounted() {
    this.loaded = false;
    const bnft = this.$store.getters.getBenefitConfig;
    this.label = (bnft.durations && bnft.durations.label) ?? null;
    this.code = (bnft.durations && bnft.durations.code) ?? null;
    this.ui =
      bnft.durations && bnft.durations.ui
        ? { ...bnft.durations.ui }
        : { component: null };
    this.loaded = true;
  },
  methods: {
    selectListItemsHandler(payload) {
      this.ui.items = [...payload];
    },
    routeToBenefit(route) {
      if (this.$route.query.code) {
        this.$router.push({
          name: route,
          query: { code: this.$route.query.code },
          params: { productId: this.productId },
        });
      } else {
        this.$router.push({
          name: route,
          params: { productId: this.productId },
        });
      }
    },
    saveHandler() {
      this.$store.commit("SET_NEW_BENEFIT", {
        ...this.$store.getters.getBenefitConfig,
        duration: {
          code: this.code,
          label: this.label,
          ui: { ...this.ui },
        },
      });
      this.routeToBenefit("config-benefit");
    },
  },
};
</script>

<style>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.content {
  margin: 2rem auto;
  min-width: 90%;
  border: 1px solid #ddd;
  padding: 2rem;
}

.factor-config-modal {
  width: "500px";
}
</style>
