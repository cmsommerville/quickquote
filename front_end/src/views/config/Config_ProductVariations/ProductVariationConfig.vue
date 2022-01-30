<template>
  <div class="grid grid-cols-6">
    <div class="col-span-3">
      <div class="my-8">
        <app-input v-model="selection.min_issue_age" type="number"
          >Min Issue Age</app-input
        >
      </div>
      <div class="my-8">
        <app-input v-model="selection.max_issue_age" type="number"
          >Max Issue Age</app-input
        >
      </div>
      <div class="my-4">
        <app-input
          v-if="selection.is_family_code_rated"
          v-model="selection.family_code_rating_algorithm_code"
          >Family Code Rating Algorithm</app-input
        >
      </div>
    </div>
    <div class="col-span-2">
      <div class="mt-8 mb-4">
        <app-checkbox v-model="selection.is_gender_rated"
          >Gender Rated</app-checkbox
        >
      </div>
      <div class="my-4">
        <app-checkbox v-model="selection.is_age_rated">Age Rated</app-checkbox>
      </div>
      <div class="my-4">
        <app-checkbox v-model="selection.is_smoker_rated"
          >Tobacco Rated</app-checkbox
        >
      </div>
      <div class="my-4">
        <app-checkbox v-model="selection.is_family_code_rated"
          >Family Code Rated</app-checkbox
        >
      </div>
    </div>
  </div>
</template>

<script>
import { format } from "date-fns";

export default {
  name: "ProductVariationConfig",
  props: {
    selection: {
      required: true,
      type: Object,
    },
  },
  data() {
    return {
      loaded: false,
    };
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
