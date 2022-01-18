<template>
  <div class="w-full bg-gray-50 rounded-md min-h-96 p-8">
    <h2 class="font-bold text-3xl">Start a New Plan</h2>
    <h3 class="font-normal text-lg mb-6">Let's pick a product</h3>

    <div class="grid grid-cols-2">
      <router-link
        to="#"
        class="
          text-center
          bg-gray-200
          p-2
          border-r border-gray-300
          text-uppercase
          border-b-4 border-b-red-500
          text-red-500
          uppercase
          tracking-wide
          text-sm
        "
        >Product</router-link
      >
      <router-link
        to="#"
        class="
          text-center
          bg-gray-200
          p-2
          text-uppercase
          uppercase
          tracking-wide
          text-sm
        "
        >Configure</router-link
      >
    </div>

    <div class="grid grid-cols-3 gap-8">
      <div>
        <app-tile
          text="Accident"
          fromColor="from-red-500"
          toColor="to-orange-500"
          :selected="product_selection === 'AC'"
          @update:selection="productSelectionHandler('AC')"
        >
          <puzzle-icon class="opacity-20 text-black h-2/3 w-2/3" />
        </app-tile>
      </div>
      <div>
        <app-tile
          text="Critical Illness"
          :fromColor="'from-yellow-500'"
          toColor="to-green-500"
          :selected="product_selection === 'CI'"
          @update:selection="productSelectionHandler('CI')"
        >
          <sun-icon class="opacity-20 text-black h-2/3 w-2/3" />
        </app-tile>
      </div>
      <div>
        <app-tile
          text="Hospital Indemnity"
          :fromColor="'from-blue-500'"
          toColor="to-violet-500"
          :selected="product_selection === 'HI'"
          @update:selection="productSelectionHandler('HI')"
        >
          <plus-circle-icon class="opacity-20 text-black h-2/3 w-2/3" />
        </app-tile>
      </div>
    </div>

    <div class="flex justify-center my-3">
      <app-button
        type="submit"
        class="mx-3 border-red-500 bg-red-500 text-white"
        :disabled="!product_selection"
        >Next</app-button
      >
      <app-button type="reset" class="mx-3 border-red-500">Reset</app-button>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios.js";
import AppButton from "../../components/AppButton.vue";
import AppTile from "../../components/AppTile.vue";
import { PuzzleIcon, SunIcon, PlusCircleIcon } from "@heroicons/vue/outline";

export default {
  name: "SelectionPlan",
  components: { AppButton, AppTile, PuzzleIcon, SunIcon, PlusCircleIcon },
  data() {
    return {
      loaded: false,
      error: null,
      product_selection: null,
      selection_product: null,
      selection_product_variation: null,
      selection_rating_state: null,
      selection_plan_effective_date: null,
      selection_is_gender_distinct: false,
      selection_is_smoker_distinct: false,
      products: [],
      rules: {
        effective_date: (v) => {
          if (this.selection_rating_state) {
            const state_config = this.selection_product.states.find(
              (item) => item.state_id === this.selection_rating_state
            );
            const dt = new Date(v);
            const min_eff_dt = new Date(state_config.state_effective_date);
            return (
              dt >= min_eff_dt ||
              `Must be greater than ${state_config.state_effective_date}`
            );
          }
          return "Please enter an effective date";
        },
      },
      show: true,
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
      return {
        config_product_id: this.selection_product.product_id,
        config_product_variation_id:
          this.selection_product_variation.product_variation_id,
        config_state_id: this.selection_rating_state,
        plan_effective_date: this.selection_plan_effective_date,
        is_gender_distinct: this.selection_is_gender_distinct,
        is_smoker_distinct: this.selection_is_smoker_distinct,
      };
    },
  },
  methods: {
    productSelectionHandler(val) {
      this.product_selection = val;
    },
    tileSelectionHandler(selection) {
      this.selection_product = {
        ...selection,
        states: [
          ...selection.states.map((state) => {
            return {
              product_state_id: state.product_state_id,
              state_effective_date: state.state_effective_date,
              state_expiration_date: state.state_expiration_date,
              ...state.state,
            };
          }),
        ],
      };
    },

    async save(event) {
      event.preventDefault();
      const plan = await axios.post("/selections/plan", this.output);
      if (plan.status === 201) {
        this.$router.push({
          name: "selections-benefits",
          params: {
            plan_id: plan.data.selection_plan_id,
          },
        });
      }
    },
    onReset() {
      console.log("Reset");
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
