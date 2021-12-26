<template>
  <div>
    <div class="mb-4 main-section" v-if="loaded">
      <v-switch
        v-for="provision in provisions"
        :key="provision.provision_id"
        v-model="provision._selected"
        :label="provision.provision.provision_label"
      />
    </div>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn color="primary" class="mx-4" @click="save" :disabled="!valid">
        Save
      </v-btn>
      <v-btn
        color="primary"
        class="mx-4"
        @click="routeTo('config-benefit', { benefit_id })"
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

export default {
  name: "ConfigBenefitProvisions",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    benefit_id: {
      required: true,
      type: [Number, String],
    },
  },
  async mounted() {
    this.loaded = false;

    const provisions = await axios.get(
      `/qry-config/all-provisions?product_id=${this.product_id}`
    );
    const benefit_provisions = await axios.get(
      `/config/benefit-provisions?benefit_id=${this.benefit_id}`
    );
    this.provisions = [
      ...provisions.data.map((provision) => {
        const ix = benefit_provisions.data.find((bnft_prov) => {
          return bnft_prov.provision_id === provision.provision_id;
        });
        return (ix ?? -1) < 0
          ? { ...provision, _selected: false }
          : { ...provision, _selected: true };
      }),
    ];

    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      snackbar: false,
      snackbar_message: "Saved to DB",
      provisions: [],
    };
  },
  computed: {
    valid() {
      return true;
    },
    output() {
      return this.provisions
        .filter((provision) => {
          return provision._selected ?? false;
        })
        .map((provision) => {
          return {
            benefit_id: this.benefit_id,
            provision_id: provision.provision_id,
          };
        });
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
    configure() {
      console.log("woot");
    },
    async save() {
      await axios.post("/config/benefit-provisions", this.output);
      this.snackbar = true;
    },
  },
};
</script>

<style scoped></style>
