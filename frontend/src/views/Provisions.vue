<template>
  <div class="container">
    <div class="form-rater" v-if="loaded">
      <v-form class="form" @submit="onSubmit" @reset="onReset" v-if="show">
        <v-select
          :items="provisions_object.prex.options"
          v-model="selections.prex"
          :label="provisions_object.prex.text"
          class="my-3"
        ></v-select>
        <v-switch
          v-model="selections.reductionAt70"
          :label="provisions_object.reductionAt70.text"
          color="primary"
          hide-details
          class="my-3"
        ></v-switch>

        <v-text-field
          v-model.number="selections.group_size"
          label="Group Size"
          type="number"
          class="my-3"
        ></v-text-field>

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
  name: "Provisions",
  data() {
    return {
      loaded: false,
      plan_config_id: null,
      plan_id: null,
      plan_config: null,
      selections: {
        // prex: null,
        // reductionAt70: false,
      },
      show: true,
    };
  },
  computed: {
    provisions() {
      return this.plan_config.provisions;
    },
    provisions_object() {
      return this.provisions.reduce(
        (obj, item) => Object.assign(obj, { [item.name]: item }),
        {}
      );
    },
    selectionHandler() {
      return this.provisions
        .filter((prov) => Object.keys(this.selections).includes(prov.name))
        .map((item) => {
          return {
            plan_id: this.plan_id,
            provision_code: item.name,
            provision_value: String(this.selections[item.name]),
            provision_data_type: typeof this.selections[item.name],
          };
        });
    },
  },
  async mounted() {
    this.plan_config_id = this.$route.query.plan_config_id;
    const res = await axios.get(
      `http://localhost:5000/config/plan/${this.plan_config_id}`
    );
    this.plan_id = +this.$route.query.plan_id;
    this.plan_config = { ...res.data[0] };
    this.selections = [...res.data[0].provisions].reduce(
      (acc, curr) => ((acc[curr.name] = null), acc),
      {}
    );
    this.loaded = true;
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      await axios.post(
        "http://localhost:5000/selections/provisions",
        this.selectionHandler,
        {
          withCredentials: true,
        }
      );
      this.$router.push({
        name: "premium",
        query: { plan_id: this.plan_id },
      });
    },
    onReset(event) {
      event.preventDefault();
      console.log(this.selectionSubmissionHandler());
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
