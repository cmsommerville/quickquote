<template>
  <div v-if="loaded">
    <app-form-card :stages="stages" :title="title" :subtitle="subtitle">
      <template #content>
        <div class="grid grid-cols-3 xl:grid-cols-5 gap-8">
          <app-tile
            text="New Product"
            class="bg-cover bg-center"
            background="bg-grad-violet-indigo"
            :selected="product_id === -1"
            @update:selection="productSelectionHandler(-1)"
            @dblclick="configure"
          >
            <plus-circle-icon class="h-1/2 w-1/2 text-white" />
          </app-tile>

          <app-tile
            v-for="product in products"
            :text="product.product_label"
            class="bg-cover bg-center"
            background="bg-grad-violet-indigo"
            :selected="product_id === product.product_id"
            @update:selection="productSelectionHandler(product.product_id)"
            @dblclick="configure"
          >
            <plus-circle-icon class="h-1/2 w-1/2 text-white" />
          </app-tile>
        </div>
      </template>

      <template #actions>
        <div class="flex justify-center">
          <app-button
            class="mx-3"
            @click="configure"
            :disabled="product_id == null"
            >Next</app-button
          >
        </div>
      </template>
    </app-form-card>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import AppFormCard from "@/components/AppFormCard/AppFormCard.vue";
import AppButton from "@/components/AppButton.vue";
import AppTile from "@/components/AppTile.vue";

import { PlusCircleIcon } from "@heroicons/vue/outline";

export default {
  name: "Config_ProductList",
  components: { AppFormCard, AppButton, AppTile, PlusCircleIcon },
  async mounted() {
    this.loaded = false;
    const prods = await axios.get("/qry-config/all-products");
    this.products = [...prods.data];
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      title: "Setup a new product!",
      subtitle: "Or edit an existing one...",
      stages: [
        { label: "Products", id: "products", active: true },
        { label: "Configure", id: "config" },
      ],
      products: [],
      product_id: null,
    };
  },
  methods: {
    routeTo(route_name, query = {}) {
      this.$router.push({
        name: route_name,
        params: { product_id: this.product_id > 0 ? this.product_id : null },
        query: { ...query },
      });
    },
    productSelectionHandler(val) {
      this.product_id = val;
    },
    configure() {
      this.routeTo("config-product");
    },
  },
};
</script>
