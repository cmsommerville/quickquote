<template>
  <div v-if="loaded">
    <app-form-card :stages="stages" :title="title" :subtitle="subtitle">
      <template #content>
        <div class="my-4 flex justify-center">
          <div class="mx-16">
            <app-input type="date" v-model="state_effective_date"
              >Effective Date</app-input
            >
          </div>
          <div class="mx-16">
            <app-input type="date" v-model="state_expiration_date"
              >Expiration Date</app-input
            >
          </div>
        </div>
        <div
          class="grid grid-cols-6 xl:grid-cols-5 gap-8 relative min-h-96 my-12"
        >
          <div class="col-span-3">
            <united-states-map
              class="h-full"
              :configured_states="configured_states"
            />
            <div class="flex justify-end">
              <app-button
                class="h-10 text-xs"
                @click="toggleAllStates"
                :transparent="true"
                >{{
                  this.selected_states.length ? "Unselect All" : "Select All"
                }}</app-button
              >
            </div>
          </div>

          <div class="grid grid-cols-1 col-span-3 col-start-4 xl:col-span-2">
            <div
              class="relative flex flex-col items-center w-1/2 mx-auto my-6 p-2 rounded-lg shadow-md border border-gray-200"
            >
              <div
                class="absolute h-10 w-10 -top-3 -right-3 bg-green-600 rounded-full flex justify-center items-center"
              >
                <span class="text-white text-center">{{
                  state_adds.length
                }}</span>
              </div>
              <div class="w-1/3 flex justify-center mt-4">
                <shield-check-icon class="h-16 w-16 text-green-600" />
              </div>
              <div class="w-full m-4 flex justify-center">
                <app-button
                  @click="addHandler"
                  :flat="true"
                  class="text-green-600 hover:border-green-600"
                  >Add States</app-button
                >
              </div>
            </div>
            <div
              class="relative flex flex-col items-center w-1/2 mx-auto my-6 p-2 rounded-lg shadow-md border border-gray-200"
            >
              <div
                class="absolute h-10 w-10 -top-3 -right-3 bg-red-500 rounded-full flex justify-center items-center"
              >
                <span class="text-white text-center">{{
                  state_deletes.length
                }}</span>
              </div>
              <div class="w-1/3 flex justify-center mt-4">
                <shield-exclamation-icon class="h-16 w-16 text-red-500" />
              </div>
              <div class="w-full m-4 flex justify-center">
                <app-button
                  @click="deleteHandler"
                  :flat="true"
                  class="text-red-500 hover:border-red-500"
                  >Delete States</app-button
                >
              </div>
            </div>
          </div>
        </div>
      </template>
    </app-form-card>
  </div>
</template>

<script>
import { format } from "date-fns";
import axios from "@/services/axios.js";
import UnitedStatesMap from "@/components/USAMap/USAMap.vue";
import AppFormCard from "@/components/AppFormCard/AppFormCard.vue";
import { Model_ConfigBenefitState } from "@/models/Model_ConfigBenefit.js";

export default {
  name: "Config_BenefitStates",
  components: {
    AppFormCard,
    UnitedStatesMap,
  },
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    benefit_id: {
      default: null,
      type: [Number, String, null],
    },
  },
  async mounted() {
    this.loaded = false;
    const store_bnft = this.$store.getters.get_selections_object;
    if (!store_bnft || !store_bnft.benefit_code) {
      const benefit = await axios.get(`/config/benefit/${this.benefit_id}`);
      this.$store.commit("SET_SELECTIONS_OBJECT", benefit.data);
    }
    this.parent_benefit = { ...this.$store.getters.get_selections_object };
    this.configured_states = [
      ...this.parent_benefit.child_states.map((cs) => {
        return { ...cs.state, benefit_id: cs.benefit_id };
      }),
    ];
    this.state_effective_date = this.parent_benefit.benefit_effective_date;
    this.state_expiration_date = this.parent_benefit.benefit_expiration_date;
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      title: "Benefit States",
      subtitle: "Now let's select which states this benefit is available in...",
      active_stage: "states",
      _stages: [
        {
          label: "All Benefits",
          id: "landing",
          to: "config-benefits",
        },
        {
          label: "Configure",
          id: "configure",
          disabled: true,
        },
        {
          label: "States",
          id: "states",
          disabled: true,
        },
      ],
      parent_benefit: {},
      state_effective_date: "1900-01-01",
      state_expiration_date: "9999-12-31",
      configured_states: [],
    };
  },
  computed: {
    selected_states() {
      return this.$store.getters.get_selected_states;
    },
    state_adds() {
      // find states that have been selected but not previously configured
      const adds = this.selected_states.filter((sel) => {
        return (
          this.configured_states.findIndex((cfg) => {
            return cfg.state_code === sel.state_code;
          }) === -1
        );
      });

      const bnfts = adds.map((st) => {
        return this.applyModel({
          ...this.parent_benefit,
          ...st,
          benefit_effective_date: this.state_effective_date,
          benefit_expiration_date: this.state_expiration_date,
        });
      });
      return bnfts;
    },
    state_deletes() {
      // find states that have been unselected but previously configured
      const dels = this.configured_states.filter((cfg) => {
        return (
          this.selected_states.findIndex((sel) => {
            return cfg.state_code === sel.state_code;
          }) === -1
        );
      });
      const bnfts = dels.map((st) => {
        return this.applyModel({
          ...this.parent_benefit,
          ...st,
          benefit_effective_date: this.state_effective_date,
          benefit_expiration_date: this.state_expiration_date,
        });
      });
      return bnfts;
    },
    stages() {
      return this._stages.map((item) => ({
        ...item,
        active: item.id === this.active_stage,
      }));
    },
  },
  methods: {
    applyModel(data) {
      return new Model_ConfigBenefitState(
        this.benefit_id,
        data.product_id,
        data.state_id,
        data.benefit_code,
        data.benefit_effective_date,
        data.benefit_expiration_date
      );
    },
    async addHandler() {
      try {
        const res = await axios.post(`/config/benefits`, this.state_adds);
        this.$store.dispatch(
          "SET_SNACKBAR_MESSAGE",
          `Added ${res.data.length} new states to benefit '${this.parent_benefit.benefit_code}'`
        );
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
    deleteHandler() {
      console.log("Delete");
    },
    routeTo(route_name, params = {}, query = {}) {
      this.$router.push({
        name: route_name,
        params: { product_id: this.product_id, ...params },
        query: { ...query },
      });
    },
    formatDateText(input_dt) {
      const dt = new Date(input_dt);
      const dtDateOnly = new Date(
        dt.valueOf() + dt.getTimezoneOffset() * 60 * 1000
      );
      return format(dtDateOnly, "M/d/yyyy");
    },
    toggleAllStates() {
      this.$store.commit("toggle_all_states");
    },
    async save() {
      try {
        const res = await axios.post(`/config/benefits`, this.output);
        this.$store.dispatch(
          "SET_SNACKBAR_MESSAGE",
          `Added ${res.data.length} new states to benefit '${this.parent_benefit.benefit_code}'`
        );
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
  },
};
</script>
