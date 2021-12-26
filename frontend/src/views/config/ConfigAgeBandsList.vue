<template>
  <div class="content" v-if="loaded">
    <v-row v-for="age_band in age_band_sets" :key="age_band.age_band_set_id">
      <v-col cols="12" xs="12">
        <v-card class="d-flex justify-space-between">
          <div class="card-content">
            <v-card-title>{{ age_band.state.state_name }}</v-card-title>
            <v-card-subtitle class="grey--text text--darken-1">{{
              displayAgeBands(age_band.age_bands)
            }}</v-card-subtitle>
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
                  @click="edit(age_band.age_band_set_id)"
                  ><v-icon color="primary">mdi-pencil</v-icon></v-btn
                >
              </template>
              <span>Edit Age Band</span>
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
        @click="routeTo('config-age-bands')"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-fab-transition>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn
        color="primary"
        class="mx-4"
        @click="routeTo('config-product-variation', { product_variation_id })"
      >
        Back to Product Variation
      </v-btn>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";

export default {
  name: "ConfigAgeBandsList",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    product_variation_id: {
      required: true,
      type: [Number, String],
    },
  },
  data() {
    return {
      loaded: false,
      age_band_sets: [],
    };
  },
  async mounted() {
    this.loaded = false;
    const res = await axios.get(
      `/qry-config/all-age-bands?product_variation_id=${this.product_variation_id}`
    );
    this.age_band_sets = [...res.data].map((set) => {
      return {
        ...set,
        age_bands: set.age_bands.sort((a, b) => {
          return a.age_band_lower < b.age_band_lower ? -1 : 1;
        }),
      };
    });
    this.loaded = true;
  },
  methods: {
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        params: {
          product_id: this.product_id,
          product_variation_id: this.product_variation_id,
        },
        query: { ...params },
      });
    },
    displayAgeBands(age_bands) {
      return age_bands
        .map((band) => {
          return `${band.age_band_lower}-${band.age_band_upper}`;
        })
        .join(", ");
    },
    edit(id) {
      this.routeTo("config-age-bands", { age_band_set_id: id });
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
