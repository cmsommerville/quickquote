<template>
  <div class="container">
    <div class="form-rater my-6" v-if="loaded">
      <v-form class="form" @submit="onSubmit" @reset="onReset" v-if="show">
        <v-item-group v-model="selections.product_code">
          <v-container>
            <v-row>
              <v-col
                v-for="product in data"
                :key="product.name"
                cols="12"
                md="6"
              >
                <v-item v-slot="{ active, toggle }" :value="product.name">
                  <v-card
                    :color="active ? 'primary' : 'secondary'"
                    class="d-flex align-center"
                    height="200"
                    @click="toggle"
                  >
                    <div
                      :class="`text-h4 flex-grow-1 text-center ${
                        active ? 'white--text' : ''
                      }`"
                    >
                      {{ product.text }}
                    </div>
                  </v-card>
                </v-item>
              </v-col>
            </v-row>
          </v-container>
        </v-item-group>

        <v-select
          :disabled="variations.length === 0"
          :items="variations"
          v-model="selections.product_variation_code"
          label="Product Variation"
          class="my-3"
        ></v-select>

        <v-select
          :items="states"
          v-model="selections.rating_state"
          label="Rating State"
          class="my-3"
        >
        </v-select>

        <v-text-field
          v-model="selections.plan_effective_date"
          label="Plan Effective Date"
          type="date"
          class="my-3"
        ></v-text-field>

        <div class="d-flex justify-content my-3">
          <v-btn type="submit" color="primary" class="mx-3">Submit</v-btn>
          <v-btn type="reset" color="secondary" class="mx-3">Reset</v-btn>
        </div>
      </v-form>
    </div>
  </div>
</template>

<script>
import axios from "../services/axios.js";

export default {
  name: "Plan",
  data() {
    return {
      loaded: false,
      data: null,
      selections: {
        product_code: null,
        product_variation_code: null,
        rating_state: null,
        plan_effective_date: null,
      },
      show: true,
    };
  },
  async mounted() {
    const res = await axios.get("/config/plans");
    this.data = [...res.data];
    this.loaded = true;
  },
  computed: {
    variations() {
      if (this.selections.product_code) {
        const product = this.data.find(
          (product) => product.name === this.selections.product_code
        );
        if (product.variations) return product.variations;
        return [];
      }
      return [];
    },
    states() {
      if (this.selections.product_code) {
        const product = this.data.find(
          (product) => product.name === this.selections.product_code
        );
        return product.statesApproved.map((stateObj) => {
          return {
            value: stateObj.state,
            text: stateObj.state,
          };
        });
      }
      return ["AL", "AZ", "NC", "SC"];
    },
    config_id() {
      if (this.selections.product_code) {
        const product = this.data.find(
          (product) => product.name === this.selections.product_code
        );
        return product._id;
      }
      return null;
    },
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      const res = await axios.post("/selections/plan", this.selections, {
        params: { plan_config_id: this.config_id },
        // withCredentials: true,
      });
      this.$router.push({
        name: "benefits",
        query: { plan_id: res.data.plan_id, plan_config_id: this.config_id },
      });
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.selections.product_name = null;
      this.selections.plan_effective_date = null;
      this.selections.rating_state = null;
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
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

.form-rater {
  min-width: 60%;
  border: 1px solid #ddd;
  padding: 2rem;
}
</style>
