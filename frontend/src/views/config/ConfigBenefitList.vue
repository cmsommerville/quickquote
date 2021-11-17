<template>
  <div class="content" v-if="benefits">
    <v-row v-for="bnft in benefits" :key="bnft.name">
      <v-col cols="12" xs="12">
        <v-card class="d-flex justify-space-between">
          <div class="card-content">
            <v-card-title>{{ bnft.text }}</v-card-title>
            <v-card-subtitle
              >Component Type: {{ bnft.ui.component }}</v-card-subtitle
            >
          </div>
          <div class="card-edit-buttons ma-2">
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  elevation="2"
                  fab
                  x-small
                  class="mr-2"
                  v-bind="attrs"
                  v-on="on"
                  @click="editBenefit(bnft.name)"
                  ><v-icon color="primary">mdi-pencil</v-icon></v-btn
                >
              </template>
              <span>Edit Benefit</span>
            </v-tooltip>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-fab-transition>
      <v-btn
        color="pink"
        dark
        absolute
        bottom
        fab
        right
        @click="routeToBenefit(null)"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-fab-transition>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn color="primary" class="mx-4" @click="saveBenefits">
        Save Changes
      </v-btn>
    </div>
  </div>
</template>

<script>
export default {
  name: "ConfigBenefitList",
  props: {
    productId: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      benefits: null,
    };
  },
  mounted() {
    this.benefits = [...this.$store.getters.getBenefitConfigList];
  },
  methods: {
    routeToProduct() {
      this.$router.push({
        name: "config-product",
        params: { productId: this.productId },
      });
    },
    routeToBenefit(code) {
      if (code) {
        this.$router.push({
          name: "config-benefit",
          query: { code },
          params: { productId: this.productId },
        });
      } else {
        this.$router.push({
          name: "config-benefit",
          params: { productId: this.productId },
        });
      }
    },
    saveBenefits() {
      this.$store.commit("APPEND_ALL_BENEFITS");
      this.routeToProduct();
    },
    editBenefit(code) {
      this.$store.commit(
        "SET_NEW_BENEFIT",
        this.benefits.find((item) => item.name === code)
      );
      this.routeToBenefit(code);
    },
  },
};
</script>

<style scoped>
.content {
  width: 60%;
  border: 1px solid #ddd;
  margin: 2rem auto;
  position: relative;
}
</style>
