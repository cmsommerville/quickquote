<template>
  <div class="container">
    <div class="content">
      <v-row>
        <v-col></v-col>
        <v-col sm="6">
          <v-form>
            <v-text-field
              v-model.number="min"
              type="number"
              filled
              outlined
              label="Benefit Minimum"
            />

            <v-text-field
              v-model.number="max"
              type="number"
              filled
              outlined
              label="Benefit Maximum"
            />

            <v-text-field
              v-model.number="step"
              filled
              outlined
              type="number"
              label="Step"
            />

            <v-select
              v-model="unit"
              filled
              outlined
              :items="items"
              label="Unit"
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
              Save Benefit Amounts
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import { BENEFIT_UNITS } from "../../data/lookups.js";

export default {
  name: "ConfigBenefitAmounts",
  props: {
    productId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      min: null,
      max: null,
      step: null,
      unit: null,
      items: [...BENEFIT_UNITS],
    };
  },
  async mounted() {
    const bnft = this.$store.getters.getBenefitConfig;
    this.min = (bnft.amounts && bnft.amounts.min) ?? 0;
    this.max = (bnft.amounts && bnft.amounts.max) ?? null;
    this.step = (bnft.amounts && bnft.amounts.step) ?? 1;
    this.unit = (bnft.amounts && bnft.amounts.unit) ?? "$";
  },
  methods: {
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
        amounts: {
          min: this.min,
          max: this.max,
          step: this.step,
          unit: this.unit,
        },
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
