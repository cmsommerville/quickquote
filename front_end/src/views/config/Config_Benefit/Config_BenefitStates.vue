<template>
  <div v-if="loaded">
    <app-form-card :stages="stages" :title="title" :subtitle="subtitle">
      <template #content>
        <div class="grid grid-cols-6 xl:grid-cols-5 gap-8 relative h-96 my-12">
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

          <div
            class="flex flex-col justify-center col-span-3 col-start-4 xl:col-span-2"
          >
            <div
              class="flex items-center mb-2 p-2 rounded-md shadow-md border border-gray-200"
            >
              <shield-check-icon
                class="h-12 w-12 text-green-500 inline-block mr-8"
              />
              <p class="uppercase text-md font-light">
                Added:
                <span class="inline-block ml-2"
                  >{{ state_adds.length }} states</span
                >
              </p>
            </div>

            <div
              class="flex items-center mb-2 p-2 rounded-md shadow-md border border-gray-200"
            >
              <shield-exclamation-icon
                class="h-12 w-12 text-red-600 inline-block mr-8"
              />
              <p class="uppercase text-md font-light">
                Removed:
                <span class="inline-block ml-2"
                  >{{ state_deletes.length }} states</span
                >
              </p>
            </div>

            <div
              class="flex items-center mb-2 p-2 rounded-md shadow-md border border-gray-200"
            >
              <check-circle-icon
                class="h-12 w-12 text-green-500 inline-block mr-8"
              />
              <p class="uppercase text-md font-light">
                Unchanged:
                <span class="inline-block ml-2"
                  >{{ state_keeps.length }} states</span
                >
              </p>
            </div>

            <div class="flex justify-center mt-12">
              <app-button
                class="mx-3"
                :disabled="output.length === 0"
                @click="save"
                >Save</app-button
              >
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
        return cs.state;
      }),
    ];

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
      configured_states: [],
    };
  },
  computed: {
    selected_states() {
      return this.$store.getters.get_selected_states;
    },
    state_adds() {
      // find states that have been selected but not previously configured
      return this.selected_states.filter((sel) => {
        return (
          this.configured_states.findIndex((cfg) => {
            return cfg.state_code === sel.state_code;
          }) === -1
        );
      });
    },
    state_keeps() {
      // find states that have been selected and have been previously configured
      return this.selected_states.filter((sel) => {
        return (
          this.configured_states.findIndex((cfg) => {
            return cfg.state_code === sel.state_code;
          }) !== -1
        );
      });
    },
    state_deletes() {
      // find states that have been unselected but previously configured
      return this.configured_states.filter((cfg) => {
        return (
          this.selected_states.findIndex((sel) => {
            return cfg.state_code === sel.state_code;
          }) === -1
        );
      });
    },
    output() {
      const bnfts = this.selected_states.map((st) => {
        return this.applyModel({ ...this.parent_benefit, ...st });
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
