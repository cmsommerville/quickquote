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
            :disabled="tile.disabled"
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
  name: "Config_ProductVariationLanding",
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
  async mounted() {
    this.loaded = false;
    const variation = await axios.get(
      `/config/product-variations/${this.product_variation_id}`
    );
    this.product_variation = { ...variation.data };

    this.tiles = [
      ...[
        {
          text: "Basic Info",
          icon: "plus-circle-icon",
          id: "basic_info",
          route_name: "config-product-variation",
        },
        {
          text: "Age Bands",
          icon: "plus-circle-icon",
          id: "age_bands",
          route_name: "config-age-bands-list",
        },
        {
          text: "Benefit Applicability",
          icon: "plus-circle-icon",
          id: "benefit_applicability",
          route_name: "config-benefit-variation",
          query_params: {
            key: "product_variation_id",
            val: this.product_variation_id ?? null,
          },
        },
      ],
    ];
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      stages: [
        {
          label: "Back to Variations",
          id: "product_variations",
          to: "config-product-variations",
        },
        {
          label: "Configure",
          id: "configure",
          active: true,
          disabled: true,
        },
      ],
      tiles: [],
      selection: null,
      product_variation: {},
    };
  },
  computed: {
    title() {
      return `Configure ${this.product_variation.product_variation_label}`;
    },
    subtitle() {
      return "Let's edit this product variation!";
    },
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
      if (!this.selection) return;

      if (this.selection.query_params) {
        this.routeTo(this.selection.route_name, {
          [this.selection.query_params.key]: this.selection.query_params.val,
        });
      } else {
        this.routeTo(this.selection.route_name);
      }
    },
    routeTo(route_name, query = {}) {
      this.$router.push({
        name: route_name,
        params: {
          product_id: this.product_id,
          product_variation_id: this.product_variation_id,
        },
        query: { ...query },
      });
    },
    toggleHandler(stg) {
      const stage = this.stages.find((s) => s.id === stg.id);
      this.routeTo(stage.to);
    },
  },
};
</script>
