<template>
  <div class="container">
    <div class="content">
      <v-row v-for="fctr in factors" :key="fctr.code">
        <v-col></v-col>
        <v-col sm="6">
          <v-form>
            <v-card class="d-flex justify-space-between">
              <div class="card-content">
                <v-card-title>{{ fctr.label }}</v-card-title>
                <v-switch v-model="fctr.selected" class="mx-3"></v-switch>
              </div>
            </v-card>
          </v-form>
        </v-col>

        <v-col></v-col>
      </v-row>
      <v-divider></v-divider>
      <v-row class="mt-4">
        <v-col sm="12">
          <div class="call-to-action d-flex justify-center align-center">
            <v-btn @click="saveHandler" color="primary" class="mx-4">
              Save Factor Applicability
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
export default {
  name: "ConfigBenefitFactors",
  props: {
    productId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      provisions: null,
      factors: null,
    };
  },
  async mounted() {
    const bnft = this.$store.getters.getBenefitConfig;
    const provisions = this.$store.getters.getProvisionConfigList;
    const factors = bnft.factors ?? [];

    this.factors = provisions.map((prov) => {
      const fctr = factors.find((factor) => factor.code === prov.code) ?? {};
      return {
        code: prov.code,
        label: prov.label,
        selected: fctr.selected ?? false,
      };
    });
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
        factors: [...this.factors],
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
