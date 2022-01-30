<template>
  <div class="grid grid-cols-2">
    <div>
      <div class="my-8">
        <app-input
          v-model="selection.product_variation_label"
          :disabled="disableInputs"
          >Product Variation Name</app-input
        >
      </div>
      <div class="my-8">
        <app-input
          v-model="selection.product_variation_code"
          :disabled="disableInputs"
          >Product Variation Code</app-input
        >
      </div>
      <div class="my-8">
        <app-input
          v-model="selection.product_variation_effective_date"
          :disabled="disableInputs"
          type="date"
          >Effective Date</app-input
        >
      </div>
      <div class="my-8">
        <app-input
          v-model="selection.product_variation_expiration_date"
          :disabled="disableInputs"
          type="date"
          >Expiration Date</app-input
        >
      </div>
    </div>
    <div>
      <div
        class="shadow-xl rounded-lg w-auto h-20 m-8 overflow-hidden flex hover:cursor-pointer"
        v-for="(variation, ix) in product_variations"
        :key="variation.product_variation_id"
        @click="selection = variation"
      >
        <div
          class="w-1/5 h-full bg-gradient-to-br from-violet-500 to-indigo-500 flex justify-center items-center text-white"
        >
          <component :is="iconSelector(ix)" class="h-2/3 w-2/3" />
        </div>
        <div class="px-4 py-2">
          <p class="uppercase tracking-wide font-light text-lg mb-2">
            {{ variation.product_variation_label }}
          </p>
          <p class="text-sm text-gray-400">
            {{ formatDateText(variation.product_variation_effective_date) }}
            -
            {{ formatDateText(variation.product_variation_expiration_date) }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { format } from "date-fns";

export default {
  name: "ProductVariationsLanding",
  props: {
    product_variations: {
      required: true,
      type: Array,
    },
    setter: {
      default: () => true,
      type: Function,
    },
  },
  data() {
    return {
      loaded: false,
      selection: {
        product_variation_code: null,
        product_variation_label: null,
        product_variation_effective_date: "1900-01-01",
        product_variation_expiration_date: "9999-12-31",
      },
    };
  },
  watch: {
    selection(newVal) {
      this.setter(newVal);
    },
  },
  computed: {
    disableInputs() {
      return !!(this.selection && this.selection.product_variation_id);
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
    iconSelector(ix) {
      return ["sun-icon", "star-icon", "sparkles-icon", "moon-icon"][ix % 4];
    },
  },
};
</script>

<style></style>
