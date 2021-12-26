<template>
  <div>
    <div class="mb-4 main" v-if="loaded">
      <div class="main-form">
        <v-text-field
          v-model="product_variation_label"
          filled
          outlined
          :disabled="!editable"
          label="Product Variation Label"
        />
        <v-text-field
          v-model="product_variation_code"
          filled
          outlined
          :disabled="!editable"
          label="Product Variation Code"
        />
        <v-text-field
          v-model="product_variation_effective_date"
          type="date"
          filled
          outlined
          :disabled="!editable"
          label="Effective Date"
        />
        <v-text-field
          v-model="product_variation_expiration_date"
          type="date"
          filled
          outlined
          :disabled="!editable"
          label="Expiration Date"
        />

        <v-switch
          v-model="is_gender_rated"
          :disabled="!editable"
          label="Gender Rated"
        />
        <v-switch
          v-model="is_age_rated"
          :disabled="!editable"
          label="Age Rated"
        />
        <v-switch
          v-model="is_tobacco_rated"
          :disabled="!editable"
          label="Tobacco Rated"
        />
        <v-switch
          v-model="is_family_code_rated"
          :disabled="!editable"
          label="Family Code Rated"
        />

        <v-text-field
          v-if="is_family_code_rated"
          v-model="family_code_rating_algorithm_code"
          filled
          outlined
          :disabled="!editable"
          label="Family Code Rating Algorithm"
        />

        <v-text-field
          v-model.number="min_issue_age"
          type="number"
          filled
          outlined
          :disabled="!editable"
          label="Min Issue Age"
        />

        <v-text-field
          v-model.number="max_issue_age"
          type="number"
          filled
          outlined
          :disabled="!editable"
          label="Max Issue Age"
        />
      </div>
      <div class="section-configure">
        <app-dashboard-card
          title="Age Bands"
          img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
          @click:configure="configureAgeBands"
          :disabled="!is_age_rated"
        >
          Configure Age Bands
        </app-dashboard-card>
      </div>
    </div>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn color="primary" class="mx-4" :disabled="!valid" @click="save">
        Save
      </v-btn>
      <v-btn
        v-if="!!product_id"
        color="pink lighten-2"
        class="mx-4"
        outlined
        @click="editable = true"
      >
        Edit
      </v-btn>
      <v-btn
        color="primary"
        class="mx-4"
        outlined
        @click="
          routeTo('config-product-variation-list', { product_id: product_id })
        "
      >
        Back to Product Variations
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

import AppDashboardCard from "../../components/AppDashboardCard.vue";

export default {
  name: "ConfigProductVariation",
  components: { AppDashboardCard },
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
  },
  async mounted() {
    this.loaded = false;
    if (this.$route.query.product_variation_id) {
      const res = await axios.get(
        `/config/product-variations/${this.$route.query.product_variation_id}`
      );
      this.product_variation_id = this.$route.query.product_variation_id;
      this.initializeData(res.data);
    }
    this.loaded = true;
  },
  data() {
    return {
      snackbar: false,
      snackbar_message: null,
      editable: true,
      loaded: false,
      config: null,
      product_variation_id: null,
      product_variation_label: null,
      product_variation_code: null,
      product_variation_effective_date: "1900-01-01",
      product_variation_expiration_date: "9999-12-31",
      is_gender_rated: false,
      is_age_rated: false,
      is_tobacco_rated: false,
      is_family_code_rated: false,
      family_code_rating_algorithm_code: null,
      min_issue_age: 18,
      max_issue_age: 99,
    };
  },
  computed: {
    valid() {
      return (
        !!this.product_variation_label &&
        !!this.product_variation_code &&
        !!this.product_variation_effective_date &&
        !!this.product_variation_expiration_date &&
        !!this.min_issue_age &&
        !!this.max_issue_age &&
        (this.is_family_code_rated
          ? !!this.family_code_rating_algorithm_code
          : true)
      );
    },
    output() {
      return {
        product_id: this.product_id,
        product_variation_label: this.product_variation_label,
        product_variation_code: this.product_variation_code,
        product_variation_effective_date: this.product_variation_effective_date,
        product_variation_expiration_date:
          this.product_variation_expiration_date,
        is_gender_rated: this.is_gender_rated,
        is_age_rated: this.is_age_rated,
        is_tobacco_rated: this.is_tobacco_rated,
        is_family_code_rated: this.is_family_code_rated,
        min_issue_age: this.min_issue_age,
        max_issue_age: this.max_issue_age,
        family_code_rating_algorithm_code:
          this.family_code_rating_algorithm_code,
      };
    },
  },
  methods: {
    initializeData(config) {
      this.config = { ...config };
      this.product_variation_label = config.product_variation_label;
      this.product_variation_code = config.product_variation_code;
      this.product_variation_effective_date =
        config.product_variation_effective_date ?? "1900-01-01";
      this.product_variation_expiration_date =
        config.product_variation_expiration_date ?? "9999-12-31";

      this.is_gender_rated = config.is_gender_rated ?? false;
      this.is_age_rated = config.is_age_rated ?? false;
      this.is_tobacco_rated = config.is_tobacco_rated ?? false;
      this.is_family_code_rated = config.is_family_code_rated ?? false;
      this.family_code_rating_algorithm_code =
        config.family_code_rating_algorithm_code ?? null;
      this.min_issue_age = config.min_issue_age ?? 18;
      this.max_issue_age = config.max_issue_age ?? 99;
    },
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        params: {
          product_id: this.product_id,
          product_variation_id: this.product_variation_id,
        },
        query: {
          ...params,
        },
      });
    },
    async save() {
      let res;
      if (this.product_variation_id) {
        res = await axios.put(
          `/config/product-variations/${this.product_variation_id}`,
          {
            ...this.output,
            product_variation_id: this.product_variation_id,
          }
        );
      } else {
        res = await axios.post("/config/product-variations", {
          ...this.output,
        });
      }

      this.initializeData(res.data);
      this.snackbar_message = "Saved to DB";
      this.snackbar = true;
    },
    configureAgeBands() {
      this.save();
      this.routeTo("config-age-bands-list");
    },
  },
};
</script>

<style scoped>
.main {
  display: grid;
  grid-template-columns: 3fr 2fr;
  column-gap: 20px;
}

.main-form {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  column-gap: 10px;
}

.section-configure {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  column-gap: 10px;
  row-gap: 15px;
}

.btn-edit {
  position: absolute;
  top: -15px;
  right: -15px;
}
</style>
