<template>
  <div class="content" v-if="benefits">
    <v-row v-for="bnft in benefits" :key="bnft.benefit_id">
      <v-col cols="12" xs="12">
        <v-card class="d-flex justify-space-between">
          <div class="card-content">
            <v-card-title>{{ bnft.benefit.benefit_label }}</v-card-title>
            <v-card-subtitle>{{ bnft.state.state_name }}</v-card-subtitle>
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
                  @click="edit(bnft.benefit_id)"
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
        @click="routeTo('config-benefit')"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-fab-transition>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn
        color="primary"
        class="mx-4"
        @click="routeTo('config-product', { product_id })"
      >
        Back to Product
      </v-btn>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios.js";
export default {
  name: "ConfigBenefitList",
  props: {
    product_id: {
      required: true,
      type: Number,
    },
  },
  data() {
    return {
      benefits: [],
    };
  },
  async mounted() {
    this.loaded = false;
    const res = await axios.get(
      `/qry-config/all-benefits?product_id=${this.product_id}`
    );
    this.benefits = [...res.data];
    this.loaded = true;
  },
  methods: {
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        params: { product_id: this.product_id },
        query: { ...params },
      });
    },
    edit(id) {
      this.routeTo("config-benefit", { benefit_id: id });
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
