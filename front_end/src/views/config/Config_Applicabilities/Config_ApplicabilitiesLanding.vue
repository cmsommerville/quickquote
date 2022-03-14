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
  name: "Config_ApplicabilitiesLanding",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
  },
  async mounted() {
    this.loaded = false;
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      title: "Configure Benefit Applicabilities",
      subtitle: "Assign benefits to provisions and product variations...",
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
          text: "Benefit - Provision",
          icon: "plus-circle-icon",
          id: "benefit_provision",
          route_name: "config-benefit-provision",
        },
        {
          text: "Benefit - Variation",
          icon: "plus-circle-icon",
          id: "benefit_variation",
          route_name: "config-benefit-variation",
        },
      ],
      selection: {},
    };
  },
  methods: {
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
      this.routeTo(this.selection.route_name);
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
