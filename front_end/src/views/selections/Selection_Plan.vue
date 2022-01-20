<template>
  <div class="w-full bg-white shadow-xl rounded-md min-h-96 p-8">
    <h2 class="font-bold text-3xl">Start a New Plan</h2>
    <h3 class="font-normal text-md mb-6">Let's pick a product</h3>

    <div class="grid grid-cols-2">
      <span
        class="text-center bg-gray-200 p-2 border-r border-gray-300 text-uppercase border-b-4 border-b-red-500 text-red-500 uppercase tracking-wide text-sm"
        >Product</span
      >
      <span
        class="text-center bg-gray-200 p-2 text-uppercase uppercase tracking-wide text-sm"
        >Configure</span
      >
    </div>

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

    <div class="flex justify-center my-3">
      <app-button
        class="mx-3 border-red-500 bg-red-500 text-white"
        :disabled="!selection"
        @click="configure"
        >Next</app-button
      >
      <app-button type="reset" class="mx-3 border-red-500">Reset</app-button>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios.js";
import AppTile from "../../components/AppTile.vue";

export default {
  name: "SelectionPlan",
  components: { AppTile },
  data() {
    return {
      loaded: false,
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
