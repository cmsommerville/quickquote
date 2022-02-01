<template>
  <div class="w-full bg-white shadow-xl rounded-md min-h-96 p-8">
    <app-form-header :title="title" :subtitle="subtitle" />
    <age-bands-tabs
      :active_stage="active_stage"
      @toggle:stage="toggleHandler"
    />
    <div class="my-12">
      <landing-age-bands
        v-if="active_stage === 'landing'"
        :age_bands="age_bands"
        @click:edit="clickLandingHandler"
      />
      <age-bands-configure
        v-if="active_stage === 'configure'"
        :product_id="product_id"
        :selection="selection"
        @click:edit="clickEditHandler"
      />
      <age-bands-states
        v-if="active_stage === 'states'"
        :product_id="product_id"
        :selection="selection"
      />
    </div>
  </div>
</template>

<script>
import axios from "@/services/axios.js";
import AppFormHeader from "@/components/AppFormCard/AppFormHeader.vue";
import AgeBandsTabs from "./AgeBandsTabs.vue";
import LandingAgeBands from "./Landing_AgeBands.vue";
import AgeBandsConfigure from "./NewAgeBandsConfigure.vue";
import AgeBandsStates from "./NewAgeBandsStates.vue";

export default {
  name: "Config_ProductVariations",
  components: {
    AgeBandsTabs,
    LandingAgeBands,
    AgeBandsConfigure,
    AgeBandsStates,
    AppFormHeader,
  },
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
  },
  async mounted() {
    this.loaded = false;
    const res = await axios.get(
      `/qry-config/product/${this.product_id}/all-age-bands`
    );
    this.age_bands = [...res.data];
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      title: "Age Bands",
      subtitle: "These age bands have already been configured",
      active_stage: "landing",
      age_bands: [],
      selection: null,
    };
  },
  computed: {},
  methods: {
    clickLandingHandler(selection) {
      this.selection = selection;
      if (selection) {
        console.log(selection);
      } else {
        this.active_stage = "configure";
      }
    },
    clickEditHandler(selection) {
      this.selection = { ...selection };
      this.active_stage = "states";
    },
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
    async save() {
      console.log("Woot");
      //   await axios.post("/config/age-bands", this.output);
    },
  },
};
</script>
