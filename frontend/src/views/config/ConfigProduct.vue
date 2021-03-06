<template>
  <div>
    <div class="mb-4" v-if="loaded">
      <div class="main-form">
        <v-text-field
          v-model="product_label"
          filled
          outlined
          :disabled="!editable"
          label="Product Label"
        />
        <v-text-field
          v-model="product_code"
          filled
          outlined
          :disabled="!editable"
          label="Product Code"
        />
        <v-text-field
          v-model="product_effective_date"
          type="date"
          filled
          outlined
          :disabled="!editable"
          label="Effective Date"
        />
        <v-text-field
          v-model="product_expiration_date"
          type="date"
          filled
          outlined
          :disabled="!editable"
          label="Expiration Date"
        />
      </div>
      <div class="section-configure">
        <app-dashboard-card
          title="Variations"
          img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
          @click:configure="configureVariations"
        >
          {{
            config && config.variations
              ? `${config.variations.length} variations configured`
              : "Setup Variations!"
          }}
        </app-dashboard-card>

        <app-dashboard-card
          title="States"
          img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
          @click:configure="configureStates"
        >
          {{
            config && config.states
              ? `${config.states.length} states configured`
              : "Setup States!"
          }}
        </app-dashboard-card>

        <app-dashboard-card
          title="Coverages"
          img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
          @click:configure="configureCoverages"
        >
          {{
            config && config.coverages
              ? `${config.coverages.length} coverages configured`
              : "Setup Coverages!"
          }}
        </app-dashboard-card>
        <app-dashboard-card
          title="Benefits"
          img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
          @click:configure="configureBenefits"
        >
          {{
            config && config.benefits
              ? `${config.benefits.length} benefits configured`
              : "Setup Benefits!"
          }}
        </app-dashboard-card>

        <app-dashboard-card
          title="Provisions"
          img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
          @click:configure="configureProvisions"
        >
          {{
            config && config.provisions
              ? `${config.provisions.length} provisions`
              : "Setup Provisions!"
          }}
        </app-dashboard-card>

        <app-dashboard-card
          title="Rate Groups"
          img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
          @click:configure="configureRateGroups"
        >
          Setup Rate Groups!
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
        color="primary"
        class="mx-4"
        outlined
        @click="editable = true"
      >
        Edit
      </v-btn>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";

import AppDashboardCard from "../../components/AppDashboardCard.vue";

export default {
  name: "ConfigProduct",
  components: { AppDashboardCard },
  async mounted() {
    this.loaded = false;
    if (this.$route.query.product_id) {
      this.editable = false;
      const res = await axios.get(
        `/config/product/${this.$route.query.product_id}`
      );
      this.product_id = this.$route.query.product_id;
      this.initializeData(res.data);
    }
    this.loaded = true;
  },
  data() {
    return {
      editable: true,
      loaded: false,
      config: null,
      product_id: null,
      product_label: null,
      product_code: null,
      product_effective_date: "1900-01-01",
      product_expiration_date: "9999-12-31",
    };
  },
  computed: {
    valid() {
      return (
        !!this.product_label &&
        !!this.product_code &&
        !!this.product_effective_date &&
        !!this.product_expiration_date
      );
    },
    output() {
      return {
        product_label: this.product_label,
        product_code: this.product_code,
        product_effective_date: this.product_effective_date,
        product_expiration_date: this.product_expiration_date,
      };
    },
  },
  methods: {
    initializeData(config) {
      this.config = { ...config };
      this.product_label = config.product_label;
      this.product_code = config.product_code;
      this.product_effective_date = config.product_effective_date;
      this.product_expiration_date = config.product_expiration_date;
      if (config.product_id) {
        this.product_id = config.product_id;
      }
    },
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        params: {
          product_id: this.product_id,
        },
        query: {
          ...params,
        },
      });
    },
    async save() {
      if (!this.valid) {
        return;
      }
      let res;
      try {
        if (this.product_id) {
          res = await axios.put(`/config/product/${this.product_id}`, {
            ...this.output,
            product_id: this.product_id,
          });
        } else {
          res = await axios.post("/config/product", { ...this.output });
        }
        this.$store.commit("SHOW_SNACKBAR", "Saved to DB");
        this.initializeData(res.data);
        this.editable = false;
      } catch (err) {
        this.$store.commit("SHOW_SNACKBAR", err.message);
      }
    },
    configureProvisions() {
      this.routeTo("config-provision-list");
    },
    configureRateGroups() {
      this.save();
      this.routeTo("config-rate-group-list");
    },
    configureCoverages() {
      this.save();
      this.routeTo("config-coverage-list");
    },
    configureBenefits() {
      this.routeTo("config-benefit-list");
    },
    configureStates() {
      this.save();
      this.routeTo("config-product-states");
    },
    configureVariations() {
      this.save();
      this.routeTo("config-product-variation-list");
    },
  },
};
</script>

<style scoped>
.main-form {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  column-gap: 10px;
  row-gap: 15px;
}

.section-configure {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  column-gap: 10px;
  row-gap: 15px;
}

.btn-edit {
  position: absolute;
  top: -15px;
  right: -15px;
}
</style>
