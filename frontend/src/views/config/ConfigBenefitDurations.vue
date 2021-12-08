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
            <div class="d-flex justify-center">
              <app-modal-list-form
                v-if="component === 'v-select'"
                title="Select Options"
                :schema="[
                  { code: 'label', label: 'Label' },
                  { code: 'value', label: 'Value' },
                  { code: 'factor', label: 'Factor' },
                ]"
                :inputData="items"
                @submit:list-data="selectListItemsHandler"
              >
                Add Durations
              </app-modal-list-form>
            </div>
            <v-select
              v-model="defaultValue"
              :disabled="items.length === 0"
              :items="items"
              item-text="label"
              item-value="value"
              class="mt-6"
              filled
              outlined
              label="Duration Default"
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
      defaultValue: null,
      items: null,
      component: "v-select",
      componentTypes: [...COMPONENT_TYPES],
      inputTypes: [...INPUT_TYPES],
    };
  },
  async mounted() {
    this.loaded = false;
    const bnft = this.$store.getters.getBenefitConfig;
    const dur = bnft.durations[0];
    if (dur) {
      this.label = dur.label ?? null;
      this.code = dur.code ?? null;
      this.default = dur.default ?? null;
      this.items = [...dur.items] ?? [];
    }
    this.loaded = true;
  },
  methods: {
    selectListItemsHandler(payload) {
      this.items = [...payload];
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
        durations: [
          {
            code: this.code,
            label: this.label,
            default: this.defaultValue,
            items: this.items,
            component: this.component,
          },
        ],
      });
      this.routeToBenefit("config-benefit");
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
  margin: 2rem auto;
  min-width: 90%;
  border: 1px solid #ddd;
  padding: 2rem;
}

.factor-config-modal {
  width: "500px";
}
</style>
