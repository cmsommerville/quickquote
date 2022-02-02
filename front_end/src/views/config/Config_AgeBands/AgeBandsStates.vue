<template>
  <div class="w-full bg-white shadow-xl rounded-md min-h-96 p-8">
    <app-form-header :title="title" :subtitle="subtitle" />
    <age-bands-tabs :active_stage="active_stage" />
    <div class="my-12" v-if="loaded">
      <div class="grid grid-cols-6 xl:grid-cols-5 gap-8 relative h-96 my-12">
        <div class="col-span-3">
          <united-states-map class="h-full" />
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

        <div class="flex flex-col col-span-3 col-start-4 xl:col-span-2">
          <h2 class="pt-6 mr-4 mt-8 text-right">
            Your selection will make
            <span class="font-semibold text-theme-primary">{{
              selected_states.length === 1
                ? "1 state"
                : selected_states.length + " states"
            }}</span>
            effective
            {{ formatDateText(_selection.age_band_effective_date) }}
            through
            {{ formatDateText(_selection.age_band_expiration_date) }}
          </h2>
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
    </div>
  </div>
</template>

<script>
import { format } from "date-fns";
import axios from "@/services/axios.js";
import UnitedStatesMap from "@/components/USAMap/USAMap.vue";
import AgeBandsTabs from "./AgeBandsTabs.vue";
import AppFormHeader from "@/components/AppFormCard/AppFormHeader.vue";
import { Model_ConfigAgeBands } from "@/models/Model_ConfigAgeBands.js";

export default {
  name: "Config_ProductVariations",
  components: {
    AgeBandsTabs,
    AppFormHeader,
    UnitedStatesMap,
    AgeBandsTabs,
  },
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    age_band_set_id: {
      default: null,
      type: [Number, String, null],
    },
  },
  async mounted() {
    this.loaded = false;
    this._selection = { ...this.$store.getters.get_selections_object };
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      title: "Age Bands",
      subtitle: "Now let's select which states these age bands apply to...",
      active_stage: "states",
      age_band_states: [],
      _selection: {},
    };
  },
  methods: {
    routeTo(route_name, params = {}, query = {}) {
      this.$router.push({
        name: route_name,
        params: { product_id: this.product_id, ...params },
        query: { ...query },
      });
    },
    toggleHandler(stage) {
      if (!!stage.tab) {
        this.active_stage = stage.id;
      } else {
        this.routeTo(stage.to);
      }
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
        const res = await axios.post(`/config/age-band-set`, this.output);
        this.$store.dispatch(
          "SET_SNACKBAR_MESSAGE",
          `Created ${res.data.length} new age bands`
        );
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
  },
  computed: {
    ref_states() {
      return this.$store.getters.get_ref_states;
    },
    selected_states() {
      return this.$store.getters.get_selected_states;
    },
    output() {
      const age_band_set = new Model_ConfigAgeBands(
        this._selection.product_variation_id,
        this._selection.state_id,
        this._selection.age_band_effective_date,
        this._selection.age_band_expiration_date,
        this._selection.age_bands
      );

      if (this.age_band_set_id)
        age_band_set.set_age_band_set_id(this.age_band_set_id);

      return age_band_set;
    },
  },
};
</script>
