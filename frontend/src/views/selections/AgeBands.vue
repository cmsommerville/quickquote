<template>
  <div class="container">
    <div class="form-rater d-flex flex-column" v-if="loaded">
      <h2 class="mx-auto mb-12 font-weight-light text-h4">Age Bands</h2>
      <v-form class="form" @submit.prevent="save">
        <app-age-band-input
          :input_data="age_bands"
          @change:age-bands="handleAgeBands"
        />

        <div class="d-flex justify-center my-3">
          <v-btn depressed color="primary" type="submit" class="mx-3">
            Submit
          </v-btn>

          <v-btn depressed color="secondary" class="mx-3"> Reset </v-btn>
        </div>
      </v-form>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios.js";
import AppAgeBandInput from "../../components/AppAgeBandInput.vue";

export default {
  name: "AgeBands",
  components: { AppAgeBandInput },
  props: {
    plan_id: {
      required: true,
      type: [Number, String],
    },
  },
  data() {
    return {
      loaded: false,
      plan: null,
      plan_config: null,
      age_bands: [{ age_band_lower: 18, age_band_upper: 99 }],
    };
  },
  async mounted() {
    this.loaded = false;
    try {
      const res = await axios.get(`/selections/plan/${this.plan_id}/age-bands`);
      if (res.data.age_bands) {
        this.age_bands = [...res.data.age_bands];
      }
    } catch (err) {
      console.log(err.message);
    } finally {
      this.loaded = true;
    }
  },
  computed: {
    output() {
      return this.age_bands.map((band) => {
        /* eslint-disable no-unused-vars */
        const { config_age_band_id, ...selection } = band;
        /* eslint-enable no-unused-vars */
        return {
          ...selection,
          selection_plan_id: this.plan_id,
        };
      });
    },
  },
  methods: {
    handleAgeBands(data) {
      this.age_bands = [...data];
    },
    routeTo(name) {
      this.$router.push({
        name: name,
        params: { plan_id: this.plan_id },
      });
    },
    async save() {
      await axios.post(
        `/selections/plan/${this.plan_id}/age-bands`,
        this.output
      );
      this.routeTo("selections-provisions");
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-rater {
  min-width: 60%;
  border: 1px solid #ddd;
  padding: 2rem;
}
</style>
