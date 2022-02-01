<template>
  <div class="grid grid-cols-6 xl:grid-cols-5 gap-8 relative h-96">
    <div class="col-span-3">
      <united-states-map class="h-full" :configured_states="age_band_states" />
      <div class="flex justify-end">
        <app-button class="h-10 text-xs" @click="toggleAllStates">{{
          this.selected_states.length ? "Unselect All" : "Select All"
        }}</app-button>
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
        {{ formatDateText(selection.age_band_effective_date) }}
        through
        {{ formatDateText(selection.age_band_expiration_date) }}
      </h2>
      <div class="flex justify-center mt-12">
        <app-button
          class="mx-3 border-theme-primary bg-theme-primary text-white"
          @click="save"
          >Save</app-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import { format } from "date-fns";
import axios from "@/services/axios.js";
import UnitedStatesMap from "@/components/USAMap/USAMap.vue";

export default {
  name: "New_AgeBandsStates",
  components: {
    UnitedStatesMap,
  },
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    selection: {
      required: true,
      type: Object,
    },
  },
  mounted() {
    if (
      this.selection &&
      this.selection.state &&
      this.selection.state.state_code
    ) {
      this.state = [this.selection.state.state_code];
    }
  },
  data() {
    return {
      age_band_states: [],
    };
  },
  computed: {
    ref_states() {
      return this.$store.getters.get_ref_states;
    },
    selected_states() {
      return this.$store.getters.get_selected_states;
    },
    output() {
      return this.selected_states.map((state) => {
        return {
          ...this.selection,
          state_id: state.state_id,
        };
      });
    },
  },
  methods: {
    toggleAllStates() {
      this.$store.commit("toggle_all_states");
    },
    routeTo(route_name, query = {}) {
      this.$router.push({
        name: route_name,
        params: { product_id: this.product_id },
        query: { ...query },
      });
    },
    async save() {
      const res = await axios.post("/config/age-band-sets", this.output);
    },
    formatDateText(input_dt) {
      const dt = new Date(input_dt);
      const dtDateOnly = new Date(
        dt.valueOf() + dt.getTimezoneOffset() * 60 * 1000
      );
      return format(dtDateOnly, "M/d/yyyy");
    },
  },
};
</script>
