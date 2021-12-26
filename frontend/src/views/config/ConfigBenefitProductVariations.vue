<template>
  <div>
    <div class="mb-4 main-section" v-if="loaded">
      <v-switch
        v-for="variation in variations"
        :key="variation.product_variation_id"
        v-model="variation._selected"
        :label="variation.product_variation_label"
      />
    </div>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn color="primary" class="mx-4" @click="save" :disabled="!valid">
        Save
      </v-btn>
      <v-btn
        color="primary"
        class="mx-4"
        @click="routeTo('config-benefit', { benefit_id })"
      >
        Back
      </v-btn>
    </div>

    <v-snackbar
      v-model="snackbar"
      :timeout="5000"
      class="text-uppercase font-weight-black"
    >
      {{ snackbar_message }}

      <template v-slot:action="{ attrs }">
        <v-btn color="secondary" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import axios from "../../services/axios";

export default {
  name: "ConfigBenefitProductVariations",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    benefit_id: {
      required: true,
      type: [Number, String],
    },
  },
  async mounted() {
    this.loaded = false;

    const variations = await axios.get(
      `/qry-config/all-product-variations?product_id=${this.product_id}`
    );
    const benefit_product_variations = await axios.get(
      `/config/benefit-product-variations?benefit_id=${this.benefit_id}`
    );

    this.variations = [
      ...variations.data.map((variation) => {
        const ix = benefit_product_variations.data.find((bnft_var) => {
          return (
            bnft_var.product_variation_id === variation.product_variation_id
          );
        });
        return (ix ?? -1) < 0
          ? { ...variation, _selected: false }
          : { ...variation, _selected: true };
      }),
    ];

    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      snackbar: false,
      snackbar_message: "Saved to DB",
      variations: [],
    };
  },
  computed: {
    valid() {
      return true;
    },
    output() {
      return this.variations
        .filter((variation) => {
          return variation._selected ?? false;
        })
        .map((variation) => {
          return {
            benefit_id: this.benefit_id,
            product_variation_id: variation.product_variation_id,
          };
        });
    },
  },
  methods: {
    routeTo(name, params = {}) {
      this.$router.push({
        name: name,
        params: { product_id: this.product_id, benefit_id: this.benefit_id },
        query: { ...params },
      });
    },
    configure() {
      console.log("woot");
    },
    async save() {
      await axios.post("/config/benefit-product-variations", this.output);
      this.snackbar = true;
    },
  },
};
</script>

<style scoped></style>
