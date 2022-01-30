<template>
  <div v-if="loaded">
    <app-form-card
      :stages="stages"
      :title="title"
      :subtitle="subtitle"
      @toggle:stage="toggleHandler"
    >
      <template #content>
        <div class="grid grid-cols-2 gap-8">
          <app-input v-model="product.product_label">Product Name</app-input>
          <app-input v-model="product.product_code">Product Code</app-input>
          <app-input v-model="product.product_effective_date" type="date"
            >Effective Date</app-input
          >
          <app-input v-model="product.product_expiration_date" type="date"
            >Expiration Date</app-input
          >
        </div>
      </template>

      <template #actions>
        <div class="flex justify-center">
          <app-button
            class="mx-3 border-theme-primary bg-theme-primary text-white"
            @click="save"
            >Next</app-button
          >
        </div>
      </template>
    </app-form-card>
  </div>
</template>

<script>
import axios from "@/services/axios.js";

export default {
  name: "Config_ProductLanding",
  async mounted() {
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      title: "First things first!",
      subtitle: "Let's get some basic information...",
      stages: [
        { label: "Products", id: "products", to: "config-product-list" },
        {
          label: "Configure",
          id: "config",
          active: true,
          to: "config-product",
        },
      ],
      product: {
        product_effective_date: "1900-01-01",
        product_expiration_date: "9999-12-31",
      },
    };
  },
  methods: {
    routeTo(route_name, params = {}, query = {}) {
      this.$router.push({
        name: route_name,
        params: { ...params },
        query: { ...query },
      });
    },
    toggleHandler(id) {
      const stage = this.stages.find((stg) => stg.id === id);
      this.routeTo(stage.to);
    },
    async save() {
      const prod = await axios.post("/config/product", this.product);
      this.routeTo("config-product", { product_id: prod.data.product_id });
    },
  },
};
</script>
