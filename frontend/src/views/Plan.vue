<template>
  <div class="container">
    <div class="form-rater my-6" v-if="loaded">
      <v-form class="form" @submit="onSubmit" @reset="onReset" v-if="show">
        <v-item-group v-model="selected_config">
          <v-container>
            <v-row>
              <v-col
                v-for="product in all_config"
                :key="product.name"
                cols="12"
                md="6"
              >
                <v-item v-slot="{ active, toggle }" :value="product">
                  <v-card
                    :color="active ? 'accent' : 'secondary'"
                    class="d-flex align-center"
                    height="100"
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
          outlined
          rounded
          background-color="lightest"
          :disabled="!selected_config"
          :items="selected_config ? selected_config.variations : []"
          v-model="selections.product_variation_code"
          label="Product Variation"
          class="my-3"
        ></v-select>

        <v-select
          outlined
          rounded
          background-color="lightest"
          :items="select_states"
          v-model="selections.rating_state"
          label="Rating State"
          class="my-3"
        >
        </v-select>

        <v-text-field
          outlined
          rounded
          background-color="lightest"
          :disabled="!selections.rating_state"
          v-model="selections.plan_effective_date"
          label="Plan Effective Date"
          type="date"
          class="my-3"
          :rules="[rules.effective_date]"
        ></v-text-field>

        <div class="d-flex justify-center my-3">
          <v-btn type="submit" color="accent" class="mx-3">Submit</v-btn>
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
      all_config: null,
      selected_config: null,
      selections: {
        product_code: null,
        product_variation_code: null,
        rating_state: null,
        plan_effective_date: null,
      },
      rules: {
        effective_date: (v) => {
          if (this.selections.rating_state) {
            const dt = new Date(v);
            const min_eff_dt = new Date(
              this.selections.rating_state.effectiveDate
            );
            return (
              dt >= min_eff_dt ||
              `Must be greater than ${this.selections.rating_state.effectiveDate}`
            );
          }
          return "Please enter an effective date";
        },
      },
      show: true,
    };
  },
  async mounted() {
    this.plan_config_id = this.$route.query.plan_config_id;
    this.plan_id = +this.$route.query.plan_id;
    const res = await axios.get("/selections/plan", {
      params: { plan_config_id: this.plan_config_id, plan_id: this.plan_id },
    });
    this.data = { ...res.data };
    this.all_config = [...res.data.plan_config];
    if (this.plan_id) {
      this.selected_config = res.data.plan_config[0];
    }
    if (this.plan_id) {
      this.selections = {
        ...this.loadSelectionsHandler(this.selections, res.data),
      };
    }
    this.loaded = true;
  },
  computed: {
    selections_formatted() {
      return {
        ...this.selections,
        product_code: this.selected_config.name,
        rating_state: this.selections.rating_state.state,
        plan_config_id: this.selected_config._id,
      };
    },
    select_states() {
      if (this.selected_config) {
        return this.selected_config.statesApproved.map((stateObj) => {
          return {
            value: stateObj,
            text: stateObj.state,
          };
        });
      }
      return [];
    },
  },
  methods: {
    loadSelectionsHandler(inputSelections, data) {
      const selections = {};
      for (const key in inputSelections) {
        if (key === "rating_state") {
          selections[key] = data.plan_config[0].statesApproved.find(
            (item) => item.state === data.plan.rating_state
          );
        } else {
          selections[key] = data.plan[key] || null;
        }
      }
      return selections;
    },
    async onSubmit(event) {
      event.preventDefault();
      const res = await axios.post(
        "/selections/plan",
        this.selections_formatted,
        {
          params: { plan_config_id: this.selected_config._id },
        }
      );
      this.$router.push({
        name: "benefits",
        query: {
          plan_id: res.data.plan_id,
          plan_config_id: this.selected_config._id,
        },
      });
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
