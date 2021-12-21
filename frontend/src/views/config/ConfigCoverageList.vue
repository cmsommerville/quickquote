<template>
  <div class="content" v-if="loaded">
    <v-row v-for="coverage in coverages" :key="coverage.coverage_id">
      <v-col cols="12" xs="12">
        <v-card class="d-flex justify-space-between">
          <div class="card-content">
            <v-card-title>{{ coverage.coverage_label }}</v-card-title>
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
                  @click="edit(coverage.coverage_id)"
                  ><v-icon color="primary">mdi-pencil</v-icon></v-btn
                >
              </template>
              <span>Edit Coverage</span>
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
        @click="routeTo('config-coverage')"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-fab-transition>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn
        color="primary"
        class="mx-4"
        @click="routeTo('config-product', { product_id: product_id })"
      >
        Back to Product
      </v-btn>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";

export default {
  name: "ConfigCoverageList",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
  },
  data() {
    return {
      loaded: false,
      product_variation_id: null,
      coverages: [],
    };
  },
  async mounted() {
    this.loaded = false;
    const res = await axios.get(
      `/qry-config/all-coverages?product_id=${this.product_id}`
    );
    this.coverages = [...res.data];
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
      this.routeTo("config-coverage", { coverage_id: id });
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
