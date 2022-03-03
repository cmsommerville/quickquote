<template>
  <div v-if="loaded">
    <app-form-card
      :stages="stages"
      :title="title"
      :subtitle="subtitle"
      @toggle:stage="toggleHandler"
    >
      <template #content>
        <div class="grid grid-cols-4">
          <app-tile
            v-for="tile in tiles"
            :key="tile.id"
            :text="tile.text"
            class="bg-cover bg-center"
            background="bg-grad-violet-indigo"
            :disabled="!has_list(tile.prereq_ids)"
            :selected="checkedHandler(tile.id)"
            @update:selection="selectionHandler(tile)"
            @dblclick="routeHandler"
          >
            <component :is="tile.icon" class="h-1/2 w-1/2 text-white" />
          </app-tile>
        </div>
      </template>

      <template #actions>
        <div class="flex justify-center">
          <app-button class="mx-3" :disabled="!selection" @click="routeHandler"
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
  name: "Config_ExistingProduct",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
  },
  async mounted() {
    this.loaded = false;
    const prod = await axios.get(`/config/product/${this.product_id}`);
    this.product = { ...prod.data };
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      title: "Setup This Product",
      stages: [
        { label: "All Products", id: "products", to: "config-product-list" },
        {
          label: "Product",
          id: "product",
          active: true,
          to: "config-product",
        },
      ],
      tiles: [
        {
          text: "States",
          icon: "plus-circle-icon",
          id: "states",
          prereq_ids: [],
          route_name: "config-product-states",
        },
        {
          text: "Product Variations",
          icon: "plus-circle-icon",
          id: "product_variations",
          prereq_ids: ["states"],
          route_name: "config-product-variations",
        },
        {
          text: "Age Bands",
          icon: "plus-circle-icon",
          id: "age_bands",
          prereq_ids: ["product_variations"],
          route_name: "config-age-bands",
        },
        {
          text: "Coverages",
          icon: "plus-circle-icon",
          id: "coverages",
          prereq_ids: [],
          route_name: "config-coverages",
        },
        {
          text: "Benefits",
          icon: "plus-circle-icon",
          id: "benefits",
          prereq_ids: ["product_variations"],
          route_name: "config-benefits",
        },
        {
          text: "Provisions",
          icon: "plus-circle-icon",
          id: "provisions",
          prereq_ids: ["benefits"],
          route_name: "config-provision-list",
        },
      ],
      selection: null,
      product: {},
    };
  },
  computed: {
    subtitle() {
      const has_items = this.tiles.reduce(
        (a, v) => ({ ...a, [v.id]: v.prereq_ids }),
        {}
      );
      if (!this.has_list(has_items["states"]))
        return "First things first. Let's setup some states!";
      if (!this.has_list(has_items["product_variations"]))
        return "Now let's add some product variations!";
      if (!this.has_list(has_items["benefits"]))
        return "Great job so far! Let's add some benefits next!";
      if (!this.has_list(has_items["provisions"]))
        return "Let's tailor things even more with some provisions!";
      return "You've done most of the setup. What would you like to edit?";
    },
  },
  methods: {
    has_list(prereq_ids) {
      if (prereq_ids.length === 0) return true;

      return prereq_ids.reduce((prev, _id) => {
        return prev && this.product[_id] && this.product[_id].length > 0;
      }, true);
    },
    checkedHandler(key) {
      if (this.selection) {
        return this.selection.id === key;
      }
      return false;
    },
    selectionHandler(val) {
      this.selection = val;
    },
    routeHandler() {
      if (this.selection) {
        const disabled = !this.has_list(this.selection.prereq_ids);
        if (!disabled) {
          this.routeTo(this.selection.route_name);
        }
      }
    },
    routeTo(route_name, query = {}) {
      this.$router.push({
        name: route_name,
        params: { product_id: this.product_id },
        query: { ...query },
      });
    },
    toggleHandler(s) {
      const stage = this.stages.find((stg) => stg.id === s.id);
      this.routeTo(stage.to);
    },
  },
};
</script>
