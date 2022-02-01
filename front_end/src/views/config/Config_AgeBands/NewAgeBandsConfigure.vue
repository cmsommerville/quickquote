<template>
  <div>
    <div class="flex justify-center flex-col">
      <div class="grid grid-cols-3 gap-8 my-4">
        <div class="col-span-2 p-2 border-l-8 border-gray-200">
          <app-age-band-selector
            :input_data="_selection.age_bands"
            @change:bands="ageBandHandler"
          />
        </div>
        <div class="flex flex-col">
          <div class="w-60 my-6">
            <app-select
              v-model="_selection.product_variation_id"
              :items="product_variations"
              item_text="product_variation_label"
              item_value="product_variation_id"
              :top="true"
              >Product Variation</app-select
            >
          </div>
          <div class="w-60 my-6">
            <app-input
              v-model="_selection.age_band_effective_date"
              type="date"
              :top="true"
              >Effective Date</app-input
            >
          </div>
          <div class="w-60 my-6">
            <app-input
              v-model="_selection.age_band_expiration_date"
              type="date"
              :top="true"
              >Expiration Date</app-input
            >
          </div>
        </div>
      </div>
      <div class="mx-auto mt-6">
        <app-button @click="clickHandler">States</app-button>
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
    selection: {
      required: true,
      type: [Object, null],
    },
  },
  async mounted() {
    const pv = await axios.get(
      `/qry-config/all-product-variations?product_id=${this.product_id}`
    );
    this.product_variations = [...pv.data];
    if (this.selection && this.selection.age_bands) {
      this._selection = {
        ...this.selection,
      };
    }
  },
  data() {
    return {
      product_variations: [],
      _selection: {
        age_band_effective_date: "1900-01-01",
        age_band_expiration_date: "9999-12-31",
        age_bands: [{ age_band_lower: 18, age_band_upper: 99 }],
      },
    };
  },
  watch: {
    _selection: {
      handler(val) {
        this.$emit("change:variation", val);
      },
      deep: true,
    },
  },
  methods: {
    clickHandler() {
      this.$emit("click:edit", this._selection);
    },
    ageBandHandler(age_bands) {
      this._selection.age_bands = [...age_bands];
    },
  },
};
</script>

<style></style>
