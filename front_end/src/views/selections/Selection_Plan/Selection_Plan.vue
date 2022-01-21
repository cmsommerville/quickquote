<template>
  <div v-if="loaded">
    <app-form-card :stages="stages" :title="title" :subtitle="subtitle">
      <template #content>
        <div class="grid grid-cols-3 xl:grid-cols-4 gap-8 mt-8">
          <app-tile
            text="Accident"
            background="bg-accident-sm"
            :selected="selection === 'AC'"
            @update:selection="productSelectionHandler('AC')"
          >
          </app-tile>
          <app-tile
            text="Critical Illness"
            background="bg-pulse-sm"
            :selected="selection === 'CI'"
            @update:selection="productSelectionHandler('CI')"
          >
          </app-tile>
          <app-tile
            text="Hospital Indemnity"
            background="bg-stethoscope-sm"
            :selected="selection === 'HI'"
            @update:selection="productSelectionHandler('HI')"
          >
          </app-tile>

          <app-tile
            text="Short Term Disability"
            background="bg-accident-sm"
            :selected="selection === 'ST'"
            @update:selection="productSelectionHandler('ST')"
          >
          </app-tile>
        </div>
      </template>

      <template #actions>
        <div class="flex justify-center">
          <app-button
            class="mx-3 border-theme-primary bg-theme-primary text-white"
            :disabled="!selection"
            @click="configure"
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
import AppTile from "@/components/AppTile.vue";

export default {
  name: "SelectionPlan",
  components: { AppFormCard, AppTile },
  data() {
    return {
      loaded: false,
      title: "Start a New Plan",
      subtitle: "Let's pick a product!",
      stages: [
        { label: "Product", id: "product", active: true },
        { label: "Configure", id: "config" },
      ],
      error: null,
      selection: null,
      products: [],
    };
  },
  async mounted() {
    this.loaded = false;
    const prods = await axios.get("/qry-config/all-products");
    this.products = [...prods.data];
    this.loaded = true;
  },
  computed: {
    output() {
      return this.products.find((item) => item.product_code === this.selection);
    },
  },
  methods: {
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        query: {
          ...params,
        },
      });
    },
    productSelectionHandler(val) {
      this.selection = val;
    },
    configure() {
      this.routeTo("selections-plan-config", {
        product_id: this.output.product_id,
      });
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
</style>
