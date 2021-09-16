<template>
  <div class="container">
    <div class="form-rater" v-if="loaded">
      <v-form class="form" @submit="onSubmit" @reset="onReset" v-if="show">
        <v-switch
          v-for="benefit in benefits"
          :key="benefit.name"
          v-model="selections[benefit.name]"
          :label="benefit.text"
          :false-value="0"
          :true-value="100"
        >
        </v-switch>

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
  name: "Benefits",
  data() {
    return {
      loaded: false,
      plan_config_id: null,
      plan_id: null,
      plan_config: null,
      selections: {
        prex: null,
        reductionAt70: false,
      },
      show: true,
    };
  },
  computed: {
    benefits() {
      return this.plan_config.benefits;
    },
    selectionHandler() {
      return this.benefits
        .filter((bnft) => Object.keys(this.selections).includes(bnft.name))
        .map((item) => {
          return {
            plan_id: this.plan_id,
            coverage_code: item.coverage_code,
            benefit_code: item.name,
            benefit_uuid: item.uuid,
            benefit_value: this.selections[item.name],
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

    this.selections = [...res.data[0].benefits].reduce(
      (acc, curr) => ((acc[curr.name] = 0), acc),
      {}
    );
    this.loaded = true;
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      await axios.post(
        "http://localhost:5000/selections/benefits",
        this.selectionHandler,
        {
          withCredentials: true,
        }
      );
      this.$router.push({
        name: "age-bands",
        query: { plan_id: this.plan_id, plan_config_id: this.plan_config_id },
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
