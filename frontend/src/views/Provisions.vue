<template>
  <div class="container">
    <div class="content" v-if="loaded">
      <b-form class="form" @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group
          class="form-item"
          :label="provisions_object.prex.text"
          label-for="input-prex"
        >
          <b-form-select
            id="input-prex"
            v-model="selections.prex"
            :options="provisions_object.prex.options"
          ></b-form-select>
        </b-form-group>

        <b-form-checkbox
          id="checkbox-reductionAt70"
          v-model="selections.reductionAt70"
          name="checkbox-reductionAt70"
        >
          {{ provisions_object.reductionAt70.text }}
        </b-form-checkbox>

        <div class="form-item buttons">
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </div>
      </b-form>
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
      plan_id: null,
      provisions: [],
      selections: {
        prex: null,
        reductionAt70: false,
      },
      show: true,
    };
  },
  computed: {
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
            provision_name: item.text,
            provision_value: String(this.selections[item.name]),
            provision_data_type: typeof this.selections[item.name],
          };
        });
    },
  },
  async mounted() {
    const res = await axios.get("http://localhost:5000/workflow/provisions");
    this.provisions = [...res.data];
    this.plan_id = +this.$route.query.plan_id || null;
    this.loaded = true;
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      await axios.post(
        "http://localhost:5000/workflow/provisions",
        this.selectionHandler,
        {
          withCredentials: true,
        }
      );
      this.$router.push({
        name: "plan-rate",
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

.content {
  width: 60%;
  border: 1px solid #ddd;
  padding: 2rem;
}

.form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.form-item {
  margin: 0.5rem;
}

.tile-wrapper {
  width: 200px;
  height: 200px;
  border: 1px solid #ddd;
  border-radius: 20px;
  cursor: pointer;
  position: relative;
  background: rgb(243, 222, 249);

  display: flex;
  justify-content: center;
  align-items: center;
}

.tile-wrapper input {
  cursor: pointer;
  position: absolute;
  height: 100%;
  width: 100%;
  opacity: 0;
}

.tile-wrapper label {
  font-size: 2.2rem;
}
</style>
