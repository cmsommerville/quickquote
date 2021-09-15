<template>
  <div class="container">
    <div class="form-rater d-flex flex-column" v-if="loaded">
      <h2 class="mx-auto mb-12 font-weight-light text-h4">Age Bands</h2>
      <v-form class="form" @submit.prevent="onSubmit" @reset="onReset">
        <div
          class="age-bands d-flex justify-space-around align-center"
          v-for="(band, index) in age_bands"
          :key="band.key"
        >
          <v-text-field
            class="mx-3"
            v-model.number="age_bands[index].lower"
            label="Enter Lower Age"
            outlined
            dense
            :readonly="index === 0"
            @blur="ageBandCalculator"
            tabindex="1"
          ></v-text-field>
          <v-text-field
            class="mx-3"
            :value="age_bands[index].upper"
            label="Upper Age"
            outlined
            dense
            disabled
            tabindex="0"
          ></v-text-field>

          <v-fab-transition v-if="index === age_bands.length - 1">
            <v-btn
              tabindex="2"
              color="teal"
              fab
              dark
              small
              @click="addAgeBandHandler"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-fab-transition>
          <v-fab-transition v-if="index !== age_bands.length - 1">
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
// const axios = require("axios");

export default {
  name: "AgeBands",
  data() {
    return {
      loaded: false,
      text: { plan_rates: null, factors: null },
      age_bands: [{ key: 0, lower: 18, upper: 99 }],
    };
  },
  async mounted() {
    this.loaded = true;
  },
  computed: {},
  methods: {
    onSubmit() {
      console.log(this.age_bands);
    },
    onReset() {
      this.age_bands = [{ key: 0, lower: 18, upper: 99 }];
    },
    ageBandCalculator() {
      for (let i = 0; i < this.age_bands.length; i++) {
        if (i === 0) {
          this.age_bands[i].lower = 18;
        } else if (this.age_bands[i].lower <= this.age_bands[i - 1].lower) {
          this.age_bands[i].lower = null;
          this.age_bands[i - 1].upper = null;
        }

        if (i === this.age_bands.length - 1) {
          this.age_bands[i].upper = 99;
        } else if (!this.age_bands[i + 1].lower) {
          this.age_bands[i].upper = null;
        } else {
          this.age_bands[i].upper = this.age_bands[i + 1].lower - 1;
        }
      }
    },
    addAgeBandHandler() {
      this.age_bands = [
        ...this.age_bands,
        { key: this.age_bands.length, lower: null, upper: 99 },
      ];
      this.ageBandCalculator();
    },
    removeAgeBandHandler(index) {
      this.age_bands.splice(index, 1);
      this.ageBandCalculator();
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
