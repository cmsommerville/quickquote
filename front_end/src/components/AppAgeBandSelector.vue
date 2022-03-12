<template>
  <div>
    <div
      class="flex justify-around items-center my-1 px-2 py-3"
      v-for="(band, index) in age_bands"
      :key="index"
    >
      <app-input
        class="mx-3"
        v-model="age_bands[index].age_band_lower"
        @blur="ageBandCalculator"
        tabindex="1"
        :top="true"
        >Enter Lower Age</app-input
      >
      <app-input
        class="mx-3"
        v-model="age_bands[index].age_band_upper"
        :disabled="true"
        tabindex="0"
        :top="true"
        >Upper Age</app-input
      >

      <div class="flex items-start">
        <app-button
          class="mr-1 w-8 h-8 flex items-center justify-center text-center"
          tabindex="2"
          :fab="true"
          @click="addAgeBandHandler(index)"
        >
          <plus-icon class="w-2/3 h-2/3" />
        </app-button>

        <app-button
          class="mr-1 w-8 h-8 flex items-center justify-center text-center bg-transparent"
          tabindex="2"
          :fab="true"
          :transparent="true"
          @click="removeAgeBandHandler(index)"
        >
          <minus-icon class="w-2/3 h-2/3" />
        </app-button>
      </div>
    </div>
  </div>
</template>

<script>
import AppButton from "./AppButton.vue";
export default {
  components: { AppButton },
  name: "AppAgeBandSelector",
  emits: ["change:bands"],
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
    age_bands: {
      handler(val) {
        this.$emit("change:bands", val);
      },
      deep: true,
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
