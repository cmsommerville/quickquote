<template>
  <div v-if="loaded">
    <app-form-card
      :stages="stages"
      :title="title"
      :subtitle="subtitle"
      @toggle:stage="toggleHandler"
    >
      <template #content>
        <div class="grid grid-cols-2 gap-6">
          <div class="mb-8">
            <app-input v-model="provision.provision_code"
              >Provision Code</app-input
            >
          </div>
          <div class="mb-8">
            <app-input v-model="provision.provision_label"
              >Provision Name</app-input
            >
          </div>
          <div class="mb-8">
            <app-input v-model="provision.provision_effective_date" type="date"
              >Effective Date</app-input
            >
          </div>
          <div class="mb-8">
            <app-input v-model="provision.provision_expiration_date" type="date"
              >Expiration Date</app-input
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
import { Model_ConfigProvision } from "@/models/Model_ConfigProvision.js";

export default {
  name: "Config_Provision",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    provision_id: {
      required: false,
      type: [Number, String],
    },
  },
  mounted() {
    this.loaded = false;
    let p_provision;
    if (this.provision_id) {
      p_provision = axios.get(`/config/provision/${this.provision_id}`);
    } else {
      p_provision = new Promise((resolve, reject) => {
        resolve({ data: {} });
      });
    }

    Promise.all([p_provision])
      .then(([provision]) => {
        const prov = { ...provision.data };
        this.provision = this.modelSetter(this.product_id, prov);
        this.loaded = true;
      })
      .catch((err) => {
        this.loaded = true;
      });
  },
  data() {
    return {
      loaded: false,
      title: "Setup This Provision",
      subtitle: "",
      active_stage: "basic_info",
      _stages: [
        {
          label: "All Provisions",
          id: "provisions",
          to: "config-provision-list",
        },
        {
          label: "Back to Provision",
          id: "provision",
          to: "config-provision-landing",
        },
        {
          label: "Basic Info",
          id: "basic_info",
          disabled: true,
        },
      ],
      provision: {},
    };
  },
  computed: {
    stages() {
      return this._stages
        .filter((item) => {
          if (this.$route.params.provision_id) {
            return item.id !== "provisions";
          } else {
            return item.id !== "provision";
          }
        })
        .map((item) => ({
          ...item,
          active: item.id === this.active_stage,
        }));
    },
    output() {
      const prov = this.modelSetter(this.product_id, this.provision);
      return prov;
    },
  },
  methods: {
    modelSetter(product_id, data) {
      return new Model_ConfigProvision(
        data.provision_id,
        product_id,
        data.provision_code,
        data.provision_label,
        data.provision_effective_date,
        data.provision_expiration_date
      );
    },
    cancel() {
      if (this.$route.params.provision_id) {
        this.routeTo("config-provision-landing");
      } else {
        this.routeTo("config-provision-list");
      }
    },
    routeTo(route_name, params = {}, query = {}) {
      this.$router.push({
        name: route_name,
        params: {
          product_id: this.product_id,
          provision_id: this.provision_id,
          ...params,
        },
        query: { ...query },
      });
    },
    async save() {
      try {
        const prov = await axios.post("/config/provision", this.output);
        this.provision = { ...prov.data };
        this.$store.commit("SET_SELECTIONS_OBJECT", this.provision);
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", "Saved to database!");

        this.routeTo("config-provision-landing", {
          provision_id: this.provision.provision_id,
        });
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
    sortOrderHandler() {
      console.log("Sort order handler!");
    },
    toggleHandler(stage) {
      this.routeTo(stage.to);
    },
  },
};
</script>
