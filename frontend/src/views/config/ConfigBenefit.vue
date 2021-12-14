<template>
  <div>
    <div class="mb-4 main-section" v-if="loaded">
      <v-form class="benefit-form">
        <v-text-field
          v-model="benefit.benefit_label"
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

        <v-select
          v-model="benefit.rate_group_id"
          :items="rate_groups"
          item-text="rate_group_label"
          item-value="rate_group_id"
          filled
          outlined
          label="Rate Group"
        />

        <v-switch v-model="vary_by_state" label="Vary by State" />
        <v-select
          v-model="benefit.state_id"
          :items="states"
          item-text="state_name"
          item-value="state_id"
          :disabled="!vary_by_state"
          filled
          outlined
          label="State"
        />

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
          title="Duration"
          img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
          @click:configure="configureDurations"
        >
          Setup Durations!
        </app-dashboard-card>

        <app-dashboard-card
          title="Provisions"
          img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
          @click:configure="configure"
        >
          Attach Provisions!
        </app-dashboard-card>
      </div>
    </div>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn color="primary" class="mx-4" @click="save" :disabled="!valid">
        Save
      </v-btn>
      <v-btn
        color="primary"
        class="mx-4"
        @click="routeTo('config-benefit-list')"
      >
        Back
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
  props: {
    product_id: {
      required: true,
      type: Number,
    },
  },
  async mounted() {
    this.loaded = false;

    const promise_covg = axios.get(
      `/qry-config/all-coverages?product_id=${this.product_id}`
    );
    const promise_states = axios.get("/config/ref-states");
    const promise_rg = axios.get(
      `/qry-config/all-rate-groups?product_id=${this.product_id}`
    );
    const promise_bnft = this.fetchBenefitData;

    Promise.all([promise_covg, promise_states, promise_bnft, promise_rg]).then(
      ([res_covg, res_states, res_bnft, res_rate_group]) => {
        this.coverages = [...res_covg.data];
        this.states = [...res_states.data];
        this.rate_groups = [
          ...res_rate_group.data.map((item) => {
            return {
              ...item,
              ...item.rate_group,
            };
          }),
        ];
        this.initializeData(res_bnft.data);

        this.loaded = true;
      }
    );

    if (this.$route.query.benefit_id) {
      this.editable = false;
      this.benefit_id = this.$route.query.benefit_id;
    }
  },
  data() {
    return {
      loaded: false,
      coverages: [],
      rate_groups: [],
      states: [],
      benefit_id: null,
      benefit: {},
      vary_by_state: false,
      unit_code_types: ["Dollars", "Percent"],
    };
  },
  computed: {
    valid() {
      return (
        this.benefit.state_id !== null &&
        !!this.benefit.benefit_label &&
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
      const { benefit_label, benefit_code, ...benefit } = this.benefit;
      return {
        ...benefit,
        benefit_code,
        benefit: {
          benefit_code,
          benefit_label,
        },
        product_id: this.product_id,
      };
    },
  },
  methods: {
    initializeData(config = {}) {
      this.benefit = {
        state_id: 0,
        benefit_code: null,
        benefit_effective_date: "1900-01-01",
        benefit_expiration_date: "9999-12-31",
        coverage_id: null,
        rate_group_id: null,
        min_value: null,
        max_value: null,
        step_value: null,
        unit_code: null,
        benefit_label: null,
        ...(config.benefit ? config.benefit : {}),
        ...config,
      };

      if (config.benefit_id) {
        this.benefit_id = config.benefit_id;
      }
      if (config.coverage_id) {
        this.coverage_id = config.coverage_id;
      }
    },
    fetchBenefitData() {
      if (this.$route.query.benefit_id) {
        return axios.get(`/config/benefit/${this.$route.query.benefit_id}`);
      }
      return new Promise((resolve) => {
        resolve({ data: [] });
      });
    },
    routeTo(name, params = {}) {
      this.$router.push({
        name: name,
        params: { product_id: this.product_id, benefit_id: this.benefit_id },
        query: { ...params },
      });
    },
    configureDurations() {
      this.save();
      this.routeTo("config-benefit-duration-list");
    },
    configure() {
      console.log("woot woot");
    },
    async save() {
      let res;
      if (this.benefit_id) {
        res = await axios.put(`/config/benefit/${this.benefit_id}`, {
          ...this.output,
          benefit_id: this.benefit_id,
        });
      } else {
        res = await axios.post("/config/benefit", {
          ...this.output,
        });
      }

      this.initializeData(res.data);
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
