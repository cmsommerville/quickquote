<template>
  <div>
    <div class="flex justify-center flex-col">
      <div class="grid grid-cols-3 gap-8 my-4">
        <div class="col-span-2 p-2 border-l-8 border-gray-200">
          <app-age-band-selector
            :input_data="modelValue.age_bands"
            @change:bands="ageBandHandler"
          />
        </div>
        <div class="flex flex-col">
          <div class="w-60 my-6">
            <app-select
              v-model="modelValue.product_variation_id"
              :items="product_variations"
              item_text="product_variation_label"
              item_value="product_variation_id"
              :top="true"
              >Product Variation</app-select
            >
          </div>
          <div class="w-60 my-6">
            <app-input
              v-model="modelValue.age_band_effective_date"
              type="date"
              :top="true"
              >Effective Date</app-input
            >
          </div>
          <div class="w-60 my-6">
            <app-input
              v-model="modelValue.age_band_expiration_date"
              type="date"
              :top="true"
              >Expiration Date</app-input
            >
          </div>
        </div>
      </div>
      <div class="mx-auto mt-6">
        <app-button @click="routeTo('config-age-bands-states')"
          >States</app-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import AppAgeBandSelector from "@/components/AppAgeBandSelector.vue";

export default {
  name: "New_AgeBandsLanding",
  components: { AppAgeBandSelector },
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    product_variations: {
      required: true,
      type: Array,
    },
    modelValue: {
      required: true,
    },
  },
  watch: {
    modelValue: {
      handler(val) {
        this.$emit("update:modelValue", val);
      },
      deep: true,
    },
  },
  methods: {
    routeTo(route_name) {
      this.$router.push({
        name: route_name,
      });
    },
    ageBandHandler(age_bands) {
      this.modelValue.age_bands = [...age_bands];
    },
  },
};
</script>

<style></style>
