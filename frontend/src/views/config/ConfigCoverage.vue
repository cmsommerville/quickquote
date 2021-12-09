<template>
  <div>
    <div class="mb-4 main-section" v-if="loaded">
      <v-form class="coverage-form">
        <v-text-field
          v-model="coverage_label"
          filled
          outlined
          label="Coverage Name"
        />

        <v-text-field
          v-model="coverage_code"
          filled
          outlined
          label="Coverage Code"
        />

        <v-text-field
          v-model="section_code"
          filled
          outlined
          label="UI Section Code"
        />
      </v-form>
    </div>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn color="primary" class="mx-4" @click="save" :disabled="!valid">
        Save
      </v-btn>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";

export default {
  name: "ConfigCoverage",
  async mounted() {
    this.loaded = false;
    this.product_id = this.$route.query.product_id;

    if (this.$route.query.coverage_id) {
      this.editable = false;
      const res = await axios.get(
        `/config/coverage/${this.$route.query.coverage_id}`
      );
      this.coverage_id = this.$route.query.coverage_id;
      this.initializeData(res.data);
    } else {
      this.initializeData();
    }

    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      config: {},
      coverage_id: null,
      product_id: null,
      coverage_code: null,
      coverage_label: null,
      section_code: null,
    };
  },
  computed: {
    valid() {
      return (
        !!this.coverage_code && !!this.coverage_label && !!this.section_code
      );
    },
    output() {
      return {
        coverage_code: this.coverage_code,
        coverage_label: this.coverage_label,
        section_code: this.section_code,
        product_id: this.product_id,
      };
    },
  },
  methods: {
    initializeData(config = {}) {
      this.config = { ...config };
      this.coverage_code = config.coverage_code ?? null;
      this.coverage_label = config.coverage_label ?? null;
      this.section_code = config.section_code ?? null;

      if (config.coverage_id) {
        this.coverage_id = config.coverage_id;
      }
    },
    routeTo(name, params = {}) {
      this.$router.push({
        name: name,
        query: { product_id: this.product_id, ...params },
      });
    },
    configure() {
      console.log("woot woot");
    },
    async save() {
      if (this.coverage_id) {
        await axios.put(`/config/coverage/${this.coverage_id}`, {
          ...this.output,
          coverage_id: this.coverage_id,
        });
      } else {
        await axios.post("/config/coverage", {
          ...this.output,
        });
      }
      this.routeTo("config-coverage-list");
    },
  },
};
</script>

<style scoped>
.main-section {
  display: grid;
  grid-template-columns: 3fr 2fr;
  column-gap: 30px;
  row-gap: 15px;
}

.benefit-form {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  column-gap: 10px;
  row-gap: 10px;
}

.config-cards {
  display: grid;
  grid-template-columns: 1fr;
  row-gap: 15px;
}

.btn-edit {
  position: absolute;
  top: -15px;
  right: -15px;
}
</style>
