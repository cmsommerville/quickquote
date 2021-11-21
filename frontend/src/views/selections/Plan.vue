<template>
  <div class="container">
    <div class="form-rater my-6" v-if="loaded">
      <v-form class="form" @submit="onSubmit" @reset="onReset" v-if="show">
        <tile-list-group
          v-if="!existingQuote"
          :config="all_config"
          @tile:selected="tileSelectionHandler"
        />

        <v-text-field
          v-if="existingQuote"
          outlined
          rounded
          background-color="lightest"
          disabled
          v-model="selected_config.label"
          label="Product"
          class="my-3"
        ></v-text-field>

        <v-select
          outlined
          rounded
          background-color="lightest"
          :disabled="!selected_config"
          :items="selected_config ? selected_config.variations : []"
          v-model="selections.product_variation_code"
          item-text="label"
          item-value="code"
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
          item-text="label"
          item-value="code"
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
      existingQuote: false,
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
      this.existingQuote = true;
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
        product_code: this.selected_config.code,
        rating_state: this.selections.rating_state.code,
        plan_config_id: this.selected_config._id,
      };
    },
    select_states() {
      if (this.selected_config) {
        return this.selected_config.states.map((stateObj) => {
          return {
            value: stateObj,
            label: stateObj.state,
          };
        });
      }
      return [];
    },
  },
  methods: {
    tileSelectionHandler(selection) {
      this.selected_config = selection;
    },

    loadSelectionsHandler(inputSelections, data) {
      const selections = {};
      for (const key in inputSelections) {
        if (key === "rating_state") {
          selections[key] = data.plan_config[0].states.find(
            (item) => item.code === data.plan.rating_state
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
      if (res.status === 201) {
        this.$router.push({
          name: "benefits",
          query: {
            plan_id: res.data.plan_id,
            plan_config_id: this.selected_config._id,
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
