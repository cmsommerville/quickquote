<template>
  <div v-if="loaded">
    <app-form-card
      :stages="stages"
      :title="title"
      :subtitle="subtitle"
      @toggle:stage="toggleHandler"
    >
      <template #content>
        <div>
          <div class="flex justify-evenly pb-8 mb-8 border-b border-gray-200">
            <app-select
              class="w-72"
              v-model="selection_variation"
              :items="options_variations"
              item_text="product_variation_label"
              item_value="product_variation_id"
              @update:modelValue="fetchBenefitVariations"
            >
              Product Variation
            </app-select>

            <div class="w-48">
              <app-switch
                v-model="toggle"
                :disabled="!selection_variation"
                @update:modelValue="toggleSwitchHandler"
                >{{ toggle ? "Unselect All" : "Select All" }}</app-switch
              >
            </div>
          </div>
          <div class="grid grid-cols-3 gap-y-4">
            <app-switch
              v-for="bnft in options_benefits"
              :key="bnft.benefit_id"
              :disabled="!selection_variation"
              :modelValue="selectedValue(bnft.benefit_id)"
              @update:modelValue="selectionHandler(bnft.benefit_id)"
              >{{ bnft.benefit_label }}</app-switch
            >
          </div>
        </div>
      </template>

      <template #actions>
        <div class="flex justify-center">
          <app-button class="mx-3" @click="save">Save</app-button>
          <app-button class="mx-3" :transparent="true" @click="cancel"
            >Cancel</app-button
          >
        </div>
      </template>
    </app-form-card>
  </div>
</template>

<script>
import axios from "@/services/axios.js";

export default {
  name: "Config_BenefitProductVariation",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    product_variation_id: {
      default: null,
      type: [Number, String],
    },
  },
  mounted() {
    this.loaded = false;
    const p_variations = axios.get(
      `qry-config/all-product-variations?product_id=${this.product_id}`
    );
    const p_benefits = axios.get(
      `qry-config/all-benefits?product_id=${this.product_id}`
    );
    Promise.all([p_variations, p_benefits]).then(([variations, benefits]) => {
      this.options_variations = [...variations.data];
      this.options_benefits = [...benefits.data];
      if (this.product_variation_id) {
        this.selection_variation = this.product_variation_id;
        this.fetchBenefitVariations();
      }
    });
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      toggle: false,
      title: "Benefit to Product Variation Mapping",
      subtitle: "",
      active_stage: "benefit_product_variation",
      _stages: [
        {
          label: "Applicabilities",
          id: "applicabilities-landing",
          to: "config-applicabilities",
        },
        {
          label: "Benefit to Variation",
          id: "benefit_product_variation",
          disabled: true,
        },
      ],
      options_variations: [],
      options_benefits: [],
      selection_variation: null,
      selection_benefits: [],
      selection_bpv: [],
    };
  },
  computed: {
    stages() {
      return this._stages.map((item) => ({
        ...item,
        active: item.id === this.active_stage,
      }));
    },
    output() {
      return this.selection_benefits.map((item) => {
        // get the benefit product variation object if it exists
        const bpv =
          this.selection_bpv.find((b) => b.benefit_id === item.benefit_id) ??
          {};
        // get the PK if exists
        const { benefit_product_variation_id } = bpv;
        // merge it with the local data to make sure updates apply correctly
        if (benefit_product_variation_id)
          return { benefit_product_variation_id, ...item };
        else return { ...item };
      });
    },
  },
  methods: {
    cancel() {
      console.log("Cancel");
    },
    async fetchBenefitVariations() {
      if (this.selection_variation) {
        const bpv = await axios.get(
          `/config/benefit-product-variations?product_variation_id=${this.selection_variation}`
        );
        this.selection_bpv = [...bpv.data];
        this.selection_benefits = this.selection_bpv.map((bnft) => {
          return {
            benefit_id: bnft.benefit_id,
            benefit_product_variation_id: bnft.benefit_product_variation_id,
            product_variation_id: bnft.product_variation_id,
          };
        });
      }
    },
    routeTo(route_name, params = {}, query = {}) {
      this.$router.push({
        name: route_name,
        params: {
          product_id: this.product_id,
          ...params,
        },
        query: { ...query },
      });
    },
    async save() {
      try {
        const bpvs = await axios.post(
          `/config/benefit-product-variations`,
          this.output
        );
        this.selection_bpv = [...bpvs.data];
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", "Written to DB");
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
    selectedValue(id) {
      return (
        this.selection_benefits.findIndex((item) => item.benefit_id === id) !==
        -1
      );
    },
    selectionHandler(id) {
      if (
        this.selection_benefits.findIndex((item) => item.benefit_id === id) !==
        -1
      ) {
        this.selection_benefits = this.selection_benefits.filter(
          (item) => item.benefit_id !== id
        );
      } else {
        this.selection_benefits = [
          ...this.selection_benefits,
          { benefit_id: id, product_variation_id: this.selection_variation },
        ];
      }
    },
    toggleSwitchHandler() {
      if (this.toggle) {
        this.selection_benefits = [
          ...this.options_benefits.map((item) => {
            return {
              benefit_id: item.benefit_id,
              product_variation_id: this.selection_variation,
            };
          }),
        ];
      } else {
        this.selection_benefits = [];
      }
    },
    toggleHandler(stage) {
      this.routeTo(stage.to);
    },
  },
};
</script>
