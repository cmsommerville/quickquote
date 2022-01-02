<template>
  <div class="container">
    <div class="form-rater my-6" v-if="loaded">
      <v-form class="form" @submit="save" @reset="onReset" v-if="show">
        <tile-list-group
          :config="products"
          @tile:selected="tileSelectionHandler"
        />

        <v-select
          outlined
          rounded
          background-color="lightest"
          :disabled="!selection_product"
          :items="selection_product ? selection_product.product_variations : []"
          v-model="selection_product_variation"
          item-text="product_variation_label"
          item-value="product_variation_id"
          label="Product Variation"
          class="my-3"
        ></v-select>

        <v-select
          outlined
          rounded
          background-color="lightest"
          :items="selection_product ? selection_product.states : []"
          v-model="selection_rating_state"
          label="Rating State"
          item-text="state_name"
          item-value="state_id"
          class="my-3"
        >
        </v-select>

        <v-text-field
          outlined
          rounded
          background-color="lightest"
          :disabled="!selection_rating_state"
          v-model="selection_plan_effective_date"
          label="Plan Effective Date"
          type="date"
          class="my-3"
          :rules="[rules.effective_date]"
        ></v-text-field>

        <div class="d-flex justify-center my-3">
          <v-btn type="submit" color="primary" class="mx-3">Submit</v-btn>
          <v-btn type="reset" color="secondary" class="mx-3">Reset</v-btn>
        </div>
      </v-form>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios.js";
import TileListGroup from "../../components/TileListGroup.vue";

export default {
  name: "Plan",
  components: { TileListGroup },
  data() {
    return {
      loaded: false,
      error: null,
      selection_product: null,
      selection_product_variation: null,
      selection_rating_state: null,
      selection_plan_effective_date: null,
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
        config_product_variation_id: this.selection_product_variation,
        config_state_id: this.selection_rating_state,
        plan_effective_date: this.selection_plan_effective_date,
      };
    },
  },
  methods: {
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
      const res = await axios.post("/selections/plan", this.output, {
        query: {
          product_id: this.selection_product.product_id,
        },
      });
      if (res.status === 201) {
        this.$router.push({
          name: "selections-benefits",
          params: {
            plan_id: res.data.selection_plan_id,
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

.form-rater {
  min-width: 60%;
  border: 1px solid #ddd;
  padding: 2rem;
}
</style>
