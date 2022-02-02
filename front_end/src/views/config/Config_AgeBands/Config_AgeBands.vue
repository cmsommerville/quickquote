<template>
  <div class="w-full bg-white shadow-xl rounded-md min-h-96 p-8">
    <app-form-header :title="title" :subtitle="subtitle" />
    <age-bands-tabs
      :active_stage="active_stage"
      @toggle:stage="toggleHandler"
    />
    <div class="my-12" v-if="loaded">
      <router-view
        :age_bands="age_bands"
        :product_id="product_id"
        :product_variations="product_variations"
        v-model="selection"
      ></router-view>
    </div>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import AppFormHeader from "@/components/AppFormCard/AppFormHeader.vue";
import AgeBandsTabs from "./AgeBandsTabs.vue";

export default {
  name: "Config_ProductVariations",
  components: {
    AgeBandsTabs,
    AppFormHeader,
  },
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
  },
  mounted() {
    this.loaded = false;
    const p_age_bands = axios.get(
      `/qry-config/product/${this.product_id}/all-age-bands`
    );
    const p_variations = axios.get(
      `/qry-config/all-product-variations?product_id=${this.product_id}`
    );

    Promise.all([p_age_bands, p_variations])
      .then(([ab, vars]) => {
        this.age_bands = [...ab.data];
        this.product_variations = [...vars.data];

        this.loaded = true;
      })
      .catch((err) => {
        this.loaded = true;
      });
  },
  data() {
    return {
      loaded: false,
      title: "Age Bands",
      subtitle: "These age bands have already been configured",
      active_stage: "landing",
      age_bands: [],
      product_variations: [],
      selection: {
        age_band_effective_date: "1900-01-01",
        age_band_expiration_date: "9999-12-31",
        age_bands: [
          {
            age_band_lower: 18,
            age_band_upper: 99,
          },
        ],
      },
    };
  },
  methods: {
    routeTo(route_name, params = {}, query = {}) {
      this.$router.push({
        name: route_name,
        params: { product_id: this.product_id, ...params },
        query: { ...query },
      });
    },
    toggleHandler(stage) {
      if (!!stage.tab) {
        this.active_stage = stage.id;
      } else {
        this.routeTo(stage.to);
      }
    },
  },
};
</script>
