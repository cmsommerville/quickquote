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
              v-model="selection_provision"
              :items="options_provisions"
              item_text="provision_label"
              item_value="provision_id"
              @update:modelValue="fetchBenefitProvisions"
            >
              Provision
            </app-select>

            <div class="w-48">
              <app-switch
                v-model="toggle"
                :disabled="!selection_provision"
                @update:modelValue="toggleSwitchHandler"
                >{{ toggle ? "Unselect All" : "Select All" }}</app-switch
              >
            </div>
          </div>
          <div class="grid grid-cols-3 gap-y-4">
            <app-switch
              v-for="bnft in options_benefits"
              :key="bnft.benefit_id"
              :disabled="!selection_provision"
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
  name: "Config_BenefitProvision",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    provision_id: {
      default: null,
      type: [Number, String],
    },
  },
  mounted() {
    this.loaded = false;
    const p_provisions = axios.get(
      `qry-config/all-provisions?product_id=${this.product_id}`
    );
    const p_benefits = axios.get(
      `qry-config/all-benefits?product_id=${this.product_id}`
    );
    Promise.all([p_provisions, p_benefits]).then(([provisions, benefits]) => {
      this.options_provisions = [...provisions.data];
      this.options_benefits = [...benefits.data];
      if (this.provision_id) {
        this.selection_provision = this.provision_id;
        this.fetchBenefitProvisions();
      }
    });
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      toggle: false,
      title: "Benefit to Provision Mapping",
      subtitle: "",
      active_stage: "benefit_provision",
      _stages: [
        {
          label: "Applicabilities",
          id: "applicabilities-landing",
          to: "config-applicabilities",
        },
        {
          label: "Benefit to Provision",
          id: "benefit_provision",
          disabled: true,
        },
      ],
      options_provisions: [],
      options_benefits: [],
      selection_provision: null,
      selection_benefits: [],
      selection_bps: [],
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
        // get the benefit provision object if it exists
        const bp =
          this.selection_bps.find((b) => b.benefit_id === item.benefit_id) ??
          {};
        // get the PK if exists
        const { benefit_provision_id } = bp;
        // merge it with the local data to make sure updates apply correctly
        if (benefit_provision_id) return { benefit_provision_id, ...item };
        else return { ...item };
      });
    },
  },
  methods: {
    cancel() {
      console.log("Cancel");
    },
    async fetchBenefitProvisions() {
      if (this.selection_provision) {
        const bpv = await axios.get(
          `/config/benefit-provisions?provision_id=${this.selection_provision}`
        );
        this.selection_bps = [...bpv.data];
        this.selection_benefits = this.selection_bps.map((bnft) => {
          return {
            benefit_id: bnft.benefit_id,
            benefit_provision_id: bnft.benefit_provision_id,
            provision_id: bnft.provision_id,
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
        const bps = await axios.post(`/config/benefit-provisions`, this.output);
        this.selection_bps = [...bps.data];
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
          { benefit_id: id, provision_id: this.selection_provision },
        ];
      }
    },
    toggleSwitchHandler() {
      if (this.toggle) {
        this.selection_benefits = [
          ...this.options_benefits.map((item) => {
            return {
              benefit_id: item.benefit_id,
              provision_id: this.selection_provision,
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
