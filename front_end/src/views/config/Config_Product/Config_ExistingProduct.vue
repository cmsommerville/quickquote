<template>
  <div v-if="loaded">
    <app-form-card
      :stages="stages"
      :title="title"
      :subtitle="recommended_route.recommendation_text"
      :tabbed="true"
      @toggle:stage="toggleHandler"
    >
      <template #content>
        <div class="grid grid-cols-3 gap-8 relative h-96">
          <united-states-map
            class="h-full col-span-2"
            :product_states="[{ state_code: 'SC' }]"
            @select:state="selectStateHandler"
          />
          <p v-if="selected_state">
            You selected <strong>{{ selected_state }}</strong>
          </p>
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
import AppFormCard from "@/components/AppFormCard/AppFormCard.vue";
import AppButton from "@/components/AppButton.vue";
import AppTile from "@/components/AppTile.vue";
import UnitedStatesMap from "@/components/USAMap/USAMap.vue";

import { PlusCircleIcon } from "@heroicons/vue/outline";

export default {
  name: "Config_ExistingProduct",
  components: {
    AppFormCard,
    AppButton,
    AppTile,
    PlusCircleIcon,
    UnitedStatesMap,
  },
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
      title: "What Should We Do First?",
      stages: [
        { label: "Products", id: "products", to: "config-product-list" },
        {
          label: "Configure",
          id: "config",
          active: true,
          to: "config-product",
        },
      ],
      product: {},
      selected_state: null,
    };
  },
  computed: {
    has_product_variations() {
      return (
        this.product.product_variations &&
        this.product.product_variations.length > 0
      );
    },
    has_benefits() {
      return this.product.benefits && this.product.benefits.length > 0;
    },
    has_provisions() {
      return this.product.provisions && this.product.provisions.length > 0;
    },
    has_states() {
      return this.product.states && this.product.states.length > 0;
    },
    recommended_route() {
      if (!this.has_states) {
        return {
          recommendation_code: "STATES",
          recommendation_text: "Let's start by enabling some states...",
          route_name: "config-product-states",
        };
      }

      if (!this.has_product_variations) {
        return {
          recommendation_code: "PRODUCT_VARIATIONS",
          recommendation_text:
            "Let's start by setting up some product variations...",
          route_name: "config-product-variation-list",
        };
      }

      if (!this.has_benefits) {
        return {
          recommendation_code: "BENEFITS",
          recommendation_text:
            "You've done well so far! Now let's add some benefits...",
          route_name: "config-benefit-list",
        };
      }

      if (!this.has_provisions) {
        return {
          recommendation_code: "PROVISIONS",
          recommendation_text:
            "You're almost done! Now let's add some provisions...",
          route_name: "config-provision-list",
        };
      }

      return {
        recommendation_code: "NO_PREFERENCE",
        recommendation_text:
          "You've setup all the basics! What would you like to edit?",
      };
    },
  },
  methods: {
    selectStateHandler(st) {
      this.selected_state = st;
    },
    routeTo(route_name, query = {}) {
      this.$router.push({
        name: route_name,
        params: { product_id: this.product_id },
        query: { ...query },
      });
    },
    toggleHandler(id) {
      const stage = this.stages.find((stg) => stg.id === id);
      this.routeTo(stage.to);
    },
    save() {
      console.log("Woot!");
    },
  },
};
</script>
