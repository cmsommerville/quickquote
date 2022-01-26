<template>
  <div v-if="loaded">
    <app-form-card
      :stages="stages"
      :title="title"
      :subtitle="subtitle"
      :tabbed="true"
      @toggle:stage="toggleHandler"
    >
      <template #content>
        <div>
          <div class="grid grid-cols-6 xl:grid-cols-5 gap-8 relative h-96">
            <div class="col-span-3">
              <united-states-map
                class="h-full"
                :product_states="product_states"
              />
              <div class="flex justify-end">
                <app-button class="h-10 text-xs" @click="toggleAllStates">{{
                  this.selected_states.length ? "Unselect All" : "Select All"
                }}</app-button>
              </div>
            </div>

            <div
              class="flex flex-col justify-evenly col-span-3 col-start-4 xl:col-span-2"
            >
              <app-input type="date" v-model="state_effective_date"
                >Effective Date</app-input
              >

              <app-input type="date" v-model="state_expiration_date"
                >Expiration Date</app-input
              >

              <h2 class="border-t-2 pt-6 mr-4 mt-8 text-right">
                Your selection will make
                <span class="font-semibold text-theme-primary">{{
                  selected_states.length === 1
                    ? "1 state"
                    : selected_states.length + " states"
                }}</span>
                effective
                {{ new Date(state_effective_date).toLocaleDateString() }}
                through
                {{ new Date(state_expiration_date).toLocaleDateString() }}.
              </h2>
              <div class="flex justify-center mt-4">
                <app-button
                  class="mx-3 border-theme-primary bg-theme-primary text-white"
                  @click="save"
                  >Next</app-button
                >
              </div>
            </div>
          </div>
        </div>
      </template>
    </app-form-card>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import AppFormCard from "@/components/AppFormCard/AppFormCard.vue";
import AppButton from "@/components/AppButton.vue";
import AppInput from "@/components/AppInput.vue";
import AppTile from "@/components/AppTile.vue";
import UnitedStatesMap from "@/components/USAMap/USAMap.vue";

import { PlusCircleIcon } from "@heroicons/vue/outline";

export default {
  name: "Config_ExistingProduct",
  components: {
    AppFormCard,
    AppButton,
    AppInput,
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
    this.product_states = [
      ...prod.data.states.map((state) => {
        return {
          product_state_id: state.product_state_id,
          state_id: state.state_id,
          state_code: state.state.state_code,
          state_name: state.state.state_name,
          state_effective_date: state.state_effective_date,
          state_expiration_date: state.state_expiration_date,
        };
      }),
    ];
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      stages: [
        { label: "Products", id: "products", to: "config-product-list" },
        {
          label: "States",
          id: "states",
          active: true,
          to: "config-product",
        },
      ],
      product: {},
      product_states: [],
      state_effective_date: "1900-01-01",
      state_expiration_date: "9999-12-31",
    };
  },
  computed: {
    title() {
      if (this.product_states.length > 10) {
        return `${this.product_states.length} States Activated So Far!`;
      }
      return "Let's Activate Some States!";
    },
    subtitle() {
      if (this.product_states.length > 10) {
        return "Great job!";
      }
      return `${this.product_states.length} states activated so far...`;
    },
    ref_states() {
      return this.$store.getters.get_ref_states;
    },
    selected_states() {
      return this.$store.getters.get_selected_states;
    },
    output() {
      if (!this.selected_states) return [];
      return this.selected_states.map((state) => {
        const state_obj = this.ref_states.find((s) => s.state_code === state);
        const prod_state = this.product_states.find(
          (s) => s.state_code === state
        );

        const output_state = {
          product_id: this.product_id,
          state_id: state_obj.state_id,
          state_effective_date: this.state_effective_date,
          state_expiration_date: this.state_expiration_date,
        };

        if (prod_state && prod_state.product_state_id) {
          output_state.product_state_id = prod_state.product_state_id;
        }

        return output_state;
      });
    },
  },
  methods: {
    toggleAllStates() {
      this.$store.commit("toggle_all_states");
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
    async save() {
      await axios.post("/config/product/states", this.output);
      this.$store.commit("initialize_selected_states");
    },
  },
};
</script>
