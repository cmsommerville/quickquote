<template>
  <div>
    <v-form>
      <div class="mb-4 main-form" v-if="loaded">
        <v-text-field
          v-model="provision_label"
          filled
          outlined
          label="Provision Name"
        />

        <v-text-field
          v-model="provision_code"
          filled
          outlined
          label="Provision Code"
        />

        <v-text-field
          v-model="provision_effective_date"
          filled
          outlined
          type="date"
          label="Effective Date"
        />

        <v-text-field
          v-model="provision_expiration_date"
          filled
          outlined
          type="date"
          label="Expiration Date"
        />
      </div>
    </v-form>

    <div class="section-configure">
      <app-dashboard-card
        title="User Interface"
        img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
        @click:configure="configureUI"
      >
        {{ "Setup UI!" }}
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
        title="Factors"
        img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
        @click:configure="configureFactors"
      >
        {{
          config && config.factors
            ? `${config.factors.length} factors configured`
            : "Setup Factors!"
        }}
      </app-dashboard-card>
    </div>

    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn
        color="primary"
        class="mx-4"
        @click="saveProvision"
        :disabled="!valid"
      >
        Save
      </v-btn>
      <v-btn
        color="primary"
        class="mx-4"
        outlined
        @click="routeTo('config-provision-list')"
      >
        Back to Provision List
      </v-btn>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";
import AppDashboardCard from "../../components/AppDashboardCard.vue";

export default {
  name: "ConfigProvision",
  props: {
    product_id: {
      type: [Number, String],
      required: true,
    },
  },
  components: { AppDashboardCard },

  async mounted() {
    this.loaded = false;
    if (this.$route.query.provision_id) {
      this.editable = false;
      const res = await axios.get(
        `/config/provision/${this.$route.query.provision_id}`
      );
      this.provision_id = this.$route.query.provision_id;
      this.initializeData(res.data);
    }
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      editable: true,
      modal: false,
      config: null,
      provision_id: null,
      provision_code: null,
      provision_label: null,
      provision_effective_date: "1900-01-01",
      provision_expiration_date: "9999-12-31",
    };
  },
  computed: {
    valid() {
      return (
        !!this.provision_label &&
        !!this.provision_code &&
        !!this.provision_effective_date &&
        !!this.provision_expiration_date
      );
    },
    output() {
      return {
        product_id: this.product_id,
        provision_code: this.provision_code,
        provision: {
          provision_code: this.provision_code,
          provision_label: this.provision_label,
        },
        provision_effective_date: this.provision_effective_date,
        provision_expiration_date: this.provision_expiration_date,
      };
    },
  },
  methods: {
    initializeData(config) {
      this.config = { ...config };
      this.provision_label = config.provision.provision_label;
      this.provision_code = config.provision_code;
      this.provision_effective_date = config.provision_effective_date;
      this.provision_expiration_date = config.provision_expiration_date;
    },
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        params: {
          product_id: this.product_id,
          provision_id: this.provision_id,
        },
        query: { ...params },
      });
    },
    async saveProvision() {
      const output = { ...this.output };
      if (this.provision_id) {
        output.provision_id = this.provision_id;
      }
      const res = await axios.post("/config/provision", { ...output });
      this.provision_id = res.data.provision_id;
    },
    configureUI() {
      this.saveProvision();
      this.routeTo("config-provision-ui");
    },
    configureStates() {
      this.saveProvision();
      this.routeTo("config-provision-states");
    },
    configureFactors() {
      this.saveProvision();
      this.routeTo("config-provision-factors");
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
