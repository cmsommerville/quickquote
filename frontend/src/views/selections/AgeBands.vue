<template>
  <div class="container">
    <div class="form-rater d-flex flex-column" v-if="loaded">
      <h2 class="mx-auto mb-12 font-weight-light text-h4">Age Bands</h2>
      <v-form class="form" @submit.prevent="save">
        <!-- <div
          class="age-bands d-flex justify-space-around align-center"
          v-for="(band, index) in age_bands"
          :key="index"
        >
          <v-text-field
            class="mx-3"
            v-model.number="age_bands[index].lower_age"
            label="Enter Lower Age"
            outlined
            dense
            :readonly="index === 0"
            @blur="ageBandCalculator"
            tabindex="1"
          ></v-text-field>
          <v-text-field
            class="mx-3"
            :value="age_bands[index].upper_age"
            label="Upper Age"
            outlined
            dense
            disabled
            tabindex="0"
          ></v-text-field>

          <div class="add-subtract d-flex align-self-start">
            <v-fab-transition>
              <v-btn
                class="mr-1"
                tabindex="2"
                color="teal"
                fab
                dark
                small
                @click="addAgeBandHandler(index)"
              >
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-fab-transition>
            <v-fab-transition>
              <v-btn
                tabindex="2"
                color="red lighten-3"
                fab
                dark
                small
                @click="removeAgeBandHandler(index)"
              >
                <v-icon>mdi-minus</v-icon>
              </v-btn>
            </v-fab-transition>
          </div>
        </div> -->

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
      age_bands: [{ lower_age: 18, upper_age: 99 }],
    };
  },
  async mounted() {
    this.loaded = false;
    try {
      const res = await axios.get(`/selections/plan/${this.plan_id}/age-bands`);
      this.age_bands = [...res.data.age_bands];
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
      this.routeTo("provisions");
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
