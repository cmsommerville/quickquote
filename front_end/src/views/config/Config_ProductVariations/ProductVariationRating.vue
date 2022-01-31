<template>
  <div v-if="loaded">
    <div class="grid grid-cols-6">
      <div class="col-span-3">
        <div class="my-8">
          <app-input v-model="_selection.min_issue_age" type="number"
            >Min Issue Age</app-input
          >
        </div>
        <div class="my-8">
          <app-input v-model="_selection.max_issue_age" type="number"
            >Max Issue Age</app-input
          >
        </div>
        <div class="my-4">
          <app-input
            :disabled="!_selection.is_family_code_rated"
            v-model="_selection.family_code_rating_algorithm_code"
            >Family Code Rating Algorithm</app-input
          >
        </div>
      </div>
      <div class="col-span-2">
        <div class="mt-8 mb-4">
          <app-checkbox v-model="_selection.is_gender_rated"
            >Gender Rated</app-checkbox
          >
        </div>
        <div class="my-4">
          <app-checkbox v-model="_selection.is_age_rated"
            >Age Rated</app-checkbox
          >
        </div>
        <div class="my-4">
          <app-checkbox v-model="_selection.is_tobacco_rated"
            >Tobacco Rated</app-checkbox
          >
        </div>
        <div class="my-4">
          <app-checkbox v-model="_selection.is_family_code_rated"
            >Family Code Rated</app-checkbox
          >
        </div>
      </div>
    </div>
    <div class="border-t border-gray-200 my-8 flex flex-col items-center">
      <div class="my-8">
        <app-select
          v-model="_selection.age_distribution_set_id"
          :items="age_dist"
          item_text="age_distribution_set_label"
          item_value="age_distribution_set_id"
          class="w-80 text-right my-2"
          >Age Distribution</app-select
        >
        <app-select
          v-model="_selection.unismoker_distribution_set_id"
          :items="smoker_dist"
          item_text="attr_distribution_set_label"
          item_value="attr_distribution_set_id"
          class="w-80 text-right my-2"
          >Unismoker Distribution</app-select
        >
        <app-select
          v-model="_selection.unisex_distribution_set_id"
          :items="gender_dist"
          item_text="attr_distribution_set_label"
          item_value="attr_distribution_set_id"
          class="w-80 text-right my-2"
          >Unisex Distribution</app-select
        >
      </div>
    </div>
  </div>
</template>

<script>
import { format } from "date-fns";
import axios from "@/services/axios.js";

export default {
  name: "ProductVariationConfig",
  props: {
    selection: {
      required: true,
      type: Object,
    },
  },
  mounted() {
    this.loaded = false;
    const p_age_dist = axios.get("/qry-config/age-distribution-sets");
    const p_gender_dist = axios.get(
      "/qry-config/attr-distribution-sets?attr_code=gender"
    );
    const p_smoker_dist = axios.get(
      "/qry-config/attr-distribution-sets?attr_code=smoker_status"
    );

    this._selection = { ...this.selection };
    Promise.all([p_age_dist, p_gender_dist, p_smoker_dist]).then(
      ([age, gender, smoker]) => {
        this.age_dist = [...age.data];
        this.gender_dist = [...gender.data];
        this.smoker_dist = [...smoker.data];
        this.loaded = true;
      }
    );
  },
  data() {
    return {
      loaded: false,
      _selection: {},
      age_dist: [],
      gender_dist: [],
      smoker_dist: [],
    };
  },
  watch: {
    _selection: {
      handler() {
        this.$emit("input:data", this._selection);
      },
      deep: true,
    },
  },
  methods: {
    formatDateText(input_dt) {
      const dt = new Date(input_dt);
      const dtDateOnly = new Date(
        dt.valueOf() + dt.getTimezoneOffset() * 60 * 1000
      );
      return format(dtDateOnly, "M/d/yyyy");
    },
  },
};
</script>
