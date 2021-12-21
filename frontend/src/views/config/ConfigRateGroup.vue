<template>
  <div>
    <div class="mb-4 main-section" v-if="loaded">
      <v-form class="coverage-form">
        <v-text-field
          v-model="rate_group.rate_group_label"
          filled
          outlined
          label="Rate Group Name"
        />

        <v-text-field
          v-model="rate_group.rate_group_code"
          filled
          outlined
          label="Rate Group Code"
        />

        <v-text-field
          v-model="rate_group.rate_type_label"
          filled
          outlined
          label="Rate Type Name"
        />

        <v-text-field
          v-model="rate_group.rate_type_code"
          filled
          outlined
          label="Rate Type Code"
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
  name: "ConfigRateGroup",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
  },
  async mounted() {
    this.loaded = false;

    if (this.$route.query.rate_group_id) {
      this.editable = false;
      const res = await axios.get(
        `/config/rate-group/${this.$route.query.rate_group_id}`
      );
      this.rate_group_id = this.$route.query.rate_group_id;
      this.initializeData(res.data);
    } else {
      this.initializeData();
    }

    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      rate_group_id: null,
      rate_group: {},
    };
  },
  computed: {
    valid() {
      return (
        !!this.rate_group.rate_group_code &&
        !!this.rate_group.rate_group_label &&
        !!this.rate_group.rate_type_code &&
        !!this.rate_group.rate_type_label
      );
    },
    output() {
      return {
        rate_group_code: this.rate_group.rate_group_code,
        rate_type_code: this.rate_group.rate_type_code,
        rate_group: {
          rate_group_code: this.rate_group.rate_group_code,
          rate_group_label: this.rate_group.rate_group_label,
        },
        rate_type: {
          rate_type_code: this.rate_group.rate_type_code,
          rate_type_label: this.rate_group.rate_type_label,
        },
        product_id: this.product_id,
      };
    },
  },
  methods: {
    initializeData(config = {}) {
      const { rate_group, rate_type, rate_group_config } = config;
      this.rate_group = {
        rate_group_code: null,
        rate_group_label: null,
        rate_type_code: null,
        rate_type_label: null,
        product_id: this.product_id,
        ...rate_group_config,
        ...rate_group,
        ...rate_type,
      };
    },
    routeTo(name, params = {}) {
      this.$router.push({
        name: name,
        params: { product_id: this.product_id },
        query: { ...params },
      });
    },
    async save() {
      if (this.rate_group_id) {
        await axios.put(`/config/rate-group/${this.rate_group_id}`, {
          ...this.output,
          rate_group_id: this.rate_group_id,
        });
      } else {
        await axios.post("/config/rate-group", {
          ...this.output,
        });
      }
      this.routeTo("config-rate-group-list");
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
