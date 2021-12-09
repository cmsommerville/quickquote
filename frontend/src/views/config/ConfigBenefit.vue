<template>
  <div>
    <div class="mb-4 main-section" v-if="loaded">
      <v-form class="benefit-form">
        <v-text-field
          v-model="benefit_label"
          filled
          outlined
          label="Benefit Name"
        />

        <v-text-field
          v-model="benefit.benefit_code"
          filled
          outlined
          label="Benefit Code"
        />

        <v-text-field
          v-model="benefit.benefit_effective_date"
          type="date"
          filled
          outlined
          label="Effective Date"
        />
        <v-text-field
          v-model="benefit.benefit_expiration_date"
          type="date"
          filled
          outlined
          label="Expiration Date"
        />

        <v-select
          v-model="benefit.coverage_id"
          :items="coverages"
          item-text="coverage_label"
          item-value="coverage_id"
          filled
          outlined
          label="Coverage"
        />

        <v-spacer></v-spacer>

        <v-text-field
          v-model="benefit.min_value"
          type="number"
          filled
          outlined
          label="Benefit Minimum"
        />
        <v-text-field
          v-model="benefit.max_value"
          type="number"
          filled
          outlined
          label="Benefit Maximum"
        />
        <v-text-field
          v-model="benefit.step_value"
          type="number"
          filled
          outlined
          label="Step Size"
        />
        <v-select
          v-model="benefit.unit_code"
          :items="unit_code_types"
          filled
          outlined
          label="Unit Type"
        />
      </v-form>
      <div class="config-cards">
        <app-dashboard-card
          title="Amounts"
          img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
          @click:configure="configure"
        >
          Setup Benefit Amounts!
        </app-dashboard-card>

        <app-dashboard-card
          title="Duration"
          img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
          @click:configure="configure"
        >
          Vary by duration!
        </app-dashboard-card>

        <app-dashboard-card
          title="States"
          img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
          @click:configure="configure"
        >
          Setup States!
        </app-dashboard-card>

        <app-dashboard-card
          title="Factors"
          img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
          @click:configure="configure"
        >
          Setup Factors
        </app-dashboard-card>
      </div>
    </div>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn color="primary" class="mx-4" @click="save" :disabled="!valid">
        Save
      </v-btn>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";

import AppDashboardCard from "../../components/AppDashboardCard.vue";

export default {
  name: "ConfigBenefit",
  components: { AppDashboardCard },
  async mounted() {
    this.loaded = false;
    this.product_id = this.$route.query.product_id;

    const res_covg = await axios.get(
      `/qry-config/all-coverages?product_id=${this.$route.query.product_id}`
    );

    this.coverages = [...res_covg.data];

    if (this.$route.query.benefit_id) {
      this.editable = false;
      const res = await axios.get(
        `/config/benefit/${this.$route.query.benefit_id}`
      );
      this.benefit_id = this.$route.query.benefit_id;
      this.initializeData(res.data);
    } else {
      this.initializeData();
    }

    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      config: {},
      coverages: [],
      product_id: null,
      benefit_id: null,
      benefit_label: null,
      benefit: {
        benefit_code: null,
        benefit_effective_date: "1900-01-01",
        benefit_expiration_date: "9999-12-31",
        coverage_id: null,
        min_value: null,
        max_value: null,
        step_value: null,
        unit_code: null,
      },
      unit_code_types: ["Dollars", "Percent"],
    };
  },
  computed: {
    valid() {
      return (
        !!this.benefit_label &&
        !!this.benefit.benefit_code &&
        !!this.benefit.benefit_effective_date &&
        !!this.benefit.benefit_expiration_date &&
        !!this.benefit.coverage_id &&
        this.benefit.min_value !== null &&
        !!this.benefit.max_value &&
        !!this.benefit.step_value &&
        !!this.benefit.unit_code
      );
    },
    output() {
      return {
        ...this.benefit,
        product_id: this.product_id,
        benefit: {
          benefit_code: this.benefit.benefit_code,
          benefit_label: this.benefit_label,
        },
      };
    },
  },
  methods: {
    initializeData(config = {}) {
      this.config = { ...config };
      this.benefit_label = config.benefit.benefit_label ?? null;
      this.benefit.benefit_code = config.benefit_code ?? null;
      this.benefit.benefit_effective_date =
        config.benefit_effective_date ?? "1900-01-01";
      this.benefit.benefit_expiration_date =
        config.benefit_expiration_date ?? "9999-12-31";
      this.benefit.coverage_id = config.coverage_id ?? null;
      this.benefit.min_value = config.min_value ?? 0;
      this.benefit.max_value = config.max_value ?? null;
      this.benefit.step_value = config.step_value ?? null;
      this.benefit.unit_code = config.unit_code ?? null;

      if (config.benefit_id) {
        this.benefit_id = config.benefit_id;
      }
      if (config.coverage_id) {
        this.coverage_id = config.coverage_id;
      }
    },
    routeTo(name, params = {}) {
      this.$router.push({
        name: name,
        query: { product_id: this.product_id, ...params },
      });
    },
    configure() {
      console.log("woot woot");
    },
    async save() {
      if (this.benefit_id) {
        await axios.put(`/config/benefit/${this.benefit_id}`, {
          ...this.output,
          benefit_id: this.benefit_id,
        });
      } else {
        await axios.post("/config/benefit", {
          ...this.output,
        });
      }

      this.routeTo("config-benefit-list");
    },
  },
};
</script>

<style scoped>
.main-section {
  display: grid;
  grid-template-columns: 3fr 2fr;
  column-gap: 30px;
  row-gap: 15px;
}

.benefit-form {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  column-gap: 10px;
  row-gap: 10px;
}

.config-cards {
  display: grid;
  grid-template-columns: 1fr;
  row-gap: 15px;
}

.btn-edit {
  position: absolute;
  top: -15px;
  right: -15px;
}
</style>
