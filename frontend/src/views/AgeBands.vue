<template>
  <div class="container">
    <div class="form-rater d-flex flex-column" v-if="loaded">
      <h2 class="mx-auto mb-12 font-weight-light text-h4">Age Bands</h2>
      <v-form class="form" @submit.prevent="onSubmit" @reset="onReset">
        <div
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
const axios = require("axios");

export default {
  name: "AgeBands",
  data() {
    return {
      loaded: false,
      plan_id: null,
      plan_config_id: null,
      age_bands: [{ lower_age: 18, upper_age: 99 }],
    };
  },
  async mounted() {
    this.plan_config_id = this.$route.query.plan_config_id;
    this.plan_id = +this.$route.query.plan_id;
    this.loaded = true;
  },
  computed: {},
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      await axios.post(
        "http://localhost:5000/selections/age-bands",
        {
          age_bands: this.age_bands,
          plan_id: this.plan_id,
          plan_config_id: this.plan_config_id,
        },
        {
          withCredentials: true,
        }
      );
      this.$router.push({
        name: "provisions",
        query: { plan_id: this.plan_id, plan_config_id: this.plan_config_id },
      });
    },
    onReset() {
      this.age_bands = [{ lower_age: 18, upper_age: 99 }];
    },
    ageBandCalculator() {
      for (let i = 0; i < this.age_bands.length; i++) {
        if (i === 0) {
          this.age_bands[i].lower_age = 18;
        } else if (
          this.age_bands[i].lower_age <= this.age_bands[i - 1].lower_age
        ) {
          this.age_bands[i].lower_age = null;
          this.age_bands[i - 1].upper_age = null;
        }

        if (i === this.age_bands.length - 1) {
          this.age_bands[i].upper_age = 99;
        } else if (!this.age_bands[i + 1].lower_age) {
          this.age_bands[i].upper_age = null;
        } else {
          this.age_bands[i].upper_age = this.age_bands[i + 1].lower_age - 1;
        }
      }
    },
    addAgeBandHandler(index) {
      this.age_bands.splice(index + 1, 0, { lower_age: null, upper_age: null });
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
