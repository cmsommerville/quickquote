<template>
  <div class="wrapper">
    <div
      class="age-bands d-flex justify-space-around align-center"
      v-for="(band, index) in age_bands"
      :key="index"
    >
      <v-text-field
        class="mx-3"
        v-model.number="age_bands[index].age_band_lower"
        label="Enter Lower Age"
        outlined
        dense
        :readonly="index === 0"
        @blur="ageBandCalculator"
        tabindex="1"
      ></v-text-field>
      <v-text-field
        class="mx-3"
        :value="age_bands[index].age_band_upper"
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
  </div>
</template>

<script>
export default {
  name: "AppAgeBandInput",
  props: {
    min_age: {
      default: 18,
      type: Number,
    },
    max_age: {
      default: 99,
      type: Number,
    },
    input_data: {
      required: true,
      type: Array,
    },
  },
  data() {
    return {
      age_bands: [],
    };
  },
  watch: {
    age_bands: function (newVal) {
      this.$emit("change:age-bands", newVal);
    },
  },
  mounted() {
    this.age_bands = [...this.input_data];
  },
  methods: {
    ageBandCalculator() {
      for (let i = 0; i < this.age_bands.length; i++) {
        if (i === 0) {
          this.age_bands[i].age_band_lower = this.min_age;
        } else if (
          this.age_bands[i].age_band_lower <=
          this.age_bands[i - 1].age_band_lower
        ) {
          this.age_bands[i].age_band_lower = null;
          this.age_bands[i - 1].age_band_upper = null;
        }

        if (i === this.age_bands.length - 1) {
          this.age_bands[i].age_band_upper = this.max_age;
        } else if (!this.age_bands[i + 1].age_band_lower) {
          this.age_bands[i].age_band_upper = null;
        } else {
          this.age_bands[i].age_band_upper =
            this.age_bands[i + 1].age_band_lower - 1;
        }
      }
    },
    addAgeBandHandler(index) {
      this.age_bands.splice(index + 1, 0, {
        age_band_lower: null,
        age_band_upper: null,
      });
      this.ageBandCalculator();
    },
    removeAgeBandHandler(index) {
      this.age_bands.splice(index, 1);
      this.ageBandCalculator();
    },
  },
};
</script>

<style></style>
