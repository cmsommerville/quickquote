<template>
  <div>
    <div class="mb-4" v-if="loaded">
      <v-form class="main-form">
        <v-select
          :items="states"
          v-model="state_id"
          item-text="state_name"
          item-value="state_id"
          filled
          outlined
          label="State"
        />

        <v-text-field
          v-model="age_band_effective_date"
          type="date"
          filled
          outlined
          label="Effective Date"
        />
        <v-text-field
          v-model="age_band_expiration_date"
          type="date"
          filled
          outlined
          label="Expiration Date"
        />
      </v-form>
      <div class="age-bands">
        <app-age-band-input
          :min_age="product_variation.min_issue_age"
          :max_age="product_variation.max_issue_age"
          :input_data="age_bands"
          @change:age-bands="getAgeBands"
        />
      </div>
    </div>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn color="primary" class="mx-4" @click="save" :disabled="!valid">
        Save
      </v-btn>
      <v-btn
        color="primary"
        class="mx-4"
        @click="routeTo('config-age-bands-list')"
      >
        Back
      </v-btn>
    </div>

    <v-snackbar
      v-model="snackbar"
      :timeout="5000"
      class="text-uppercase font-weight-black"
    >
      {{ snackbar_message }}

      <template v-slot:action="{ attrs }">
        <v-btn color="secondary" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import axios from "../../services/axios";
import AppAgeBandInput from "../../components/AppAgeBandInput.vue";

export default {
  name: "ConfigAgeBandSet",
  components: { AppAgeBandInput },
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    product_variation_id: {
      required: true,
      type: [Number, String],
    },
  },
  async mounted() {
    this.loaded = false;
    this.age_band_set_id = this.$route.query.age_band_set_id ?? null;

    const promise_states = axios.get("/config/ref-states");
    const promise_variation = axios.get(
      `/config/product-variations/${this.product_variation_id}`
    );
    const promise_age_band_set = this.fetchAgeBandData();

    Promise.all([promise_states, promise_variation, promise_age_band_set]).then(
      ([res_states, res_variation, res_age_band_set]) => {
        this.product_variation = { ...res_variation.data };
        this.states = [...res_states.data];
        this.initializeData(res_age_band_set.data);

        this.loaded = true;
      }
    );
  },
  data() {
    return {
      loaded: false,
      snackbar: false,
      snackbar_message: "Saved to DB",
      age_band_set_id: null,
      state_id: null,
      age_band_effective_date: "1900-01-01",
      age_band_expiration_date: "9999-12-31",
      states: [],
      age_bands: [],
      product_variation: {},
    };
  },
  computed: {
    valid() {
      return true;
    },
    output() {
      return {
        product_variation_id: this.product_variation_id,
        state_id: this.state_id,
        age_band_effective_date: this.age_band_effective_date,
        age_band_expiration_date: this.age_band_expiration_date,
        age_bands: [...this.age_bands],
      };
    },
  },
  methods: {
    routeTo(name, params = {}) {
      this.$router.push({
        name: name,
        params: { product_id: this.product_id, benefit_id: this.benefit_id },
        query: { ...params },
      });
    },
    fetchAgeBandData() {
      if (this.$route.query.age_band_set_id) {
        return axios.get(
          `/config/age-band-set/${this.$route.query.age_band_set_id}`
        );
      }
      return new Promise((resolve) => {
        resolve({ data: {} });
      });
    },
    getAgeBands(age_bands) {
      this.age_bands = [...age_bands];
    },
    initializeData(data) {
      this.state_id = data.state_id ?? null;
      this.age_band_effective_date =
        data.age_band_effective_date ?? "1900-01-01";
      this.age_band_expiration_date =
        data.age_band_expiration_date ?? "9999-12-31";

      this.age_band_set_id = data.age_band_set_id ?? null;

      if (data.age_bands && data.age_bands.length) {
        this.age_bands = [...data.age_bands].sort((a, b) => {
          return a.age_band_lower < b.age_band_lower ? -1 : 1;
        });
      } else {
        this.age_bands = [
          {
            age_band_lower: this.product_variation.min_issue_age,
            age_band_upper: this.product_variation.max_issue_age,
          },
        ];
      }
    },
    async save() {
      let res;
      if (this.age_band_set_id) {
        res = await axios.put(`/config/age-band-set/${this.age_band_set_id}`, {
          ...this.output,
          age_band_set_id: this.age_band_set_id,
        });
      } else {
        res = await axios.post("/config/age-band-set", {
          ...this.output,
        });
      }
      this.initializeData(res.data);
      this.snackbar = true;
    },
  },
};
</script>

<style scoped>
.main-form {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  column-gap: 10px;
  row-gap: 10px;
}

.btn-edit {
  position: absolute;
  top: -15px;
  right: -15px;
}
</style>
